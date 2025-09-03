from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Game state variables
game_state = {
    'score': 0,
    'lives': 3,
    'speed': 1.0,
    'boost_timer': 0,
    'game_over': False,
    'level': 1,
    'time': 0,
    'enemy_collision_count': 0,
    'cheat_mode': False,
    'cheat_fire_timer': 0
}

# Airplane variables
airplane = {
    'x': 0, 'y': 0, 'z': 50,
    'roll': 0, 'pitch': 0, 'yaw': 0,
    'velocity': 1.0,
    'horizontal_velocity': 0.0,  # For left/right movement
    'vertical_velocity': 0.0,    # For up/down movement
    'propeller_angle': 0
}

# Camera variables
camera = {
    'mode': 0,  # 0: third-person back, 1: first-person front, 2: side view
    'x': 0, 'y': -200, 'z': 150
}

# Game objects (will be imported from other modules)
rings = []
obstacles = []
enemies = []
bullets = []
powerups = []
explosions = []

# Constants
GRID_SIZE = 2000
GRID_LINES = 40
fovY = 60

# Endless spawn parameters
RECYCLE_DISTANCE_BEHIND = 400
SPAWN_DISTANCE_AHEAD = 1800

def update_airplane():
    """Update airplane physics and movement"""
    if game_state['game_over']:
        return
    
    # Update propeller
    airplane['propeller_angle'] += 20
    
    # Fix the heading so the plane always points forward
    airplane['yaw'] = 0

    # Forward flight always in +y direction
    if game_state['boost_timer'] > 0:
        # Much faster forward movement during boost
        airplane['y'] += game_state['speed'] * 5
    else:
        # Normal forward movement
        airplane['y'] += game_state['speed']
    
    # Apply horizontal movement using horizontal velocity
    airplane['x'] += airplane['horizontal_velocity']
    
    # Apply vertical movement using vertical velocity
    airplane['z'] += airplane['vertical_velocity']
    
    # Add roll-based movement for realistic physics (but less dominant)
    rad_roll = math.radians(airplane['roll'])
    airplane['x'] += airplane['velocity'] * math.sin(rad_roll) * 0.3  # Reduced effect
    
    # Add pitch-based movement for realistic physics (but less dominant)
    rad_pitch = math.radians(airplane['pitch'])
    airplane['z'] += airplane['velocity'] * math.sin(rad_pitch) * 0.5  # Reduced effect
    
    # Gradually reduce velocities (friction/air resistance)
    airplane['horizontal_velocity'] *= 0.85  # Horizontal friction
    airplane['vertical_velocity'] *= 0.90    # Vertical friction
    
    # Gradually return roll to center when not actively rolling
    if abs(airplane['roll']) > 1:
        airplane['roll'] *= 0.95  # Gradual return to center
    else:
        airplane['roll'] = 0
    
    # Gradually return pitch to center when not actively pitching
    if abs(airplane['pitch']) > 1:
        airplane['pitch'] *= 0.98  # Slower return for pitch
    else:
        airplane['pitch'] = 0
    
    # Keep airplane above ground
    if airplane['z'] < 20:
        airplane['z'] = 20
        airplane['pitch'] = max(airplane['pitch'], 0)
    
    # Ceiling limit
    if airplane['z'] > 500:
        airplane['z'] = 500
        airplane['pitch'] = min(airplane['pitch'], 0)
    
    # Horizontal boundaries
    if airplane['x'] < -1000:
        airplane['x'] = -1000
        airplane['roll'] = max(airplane['roll'], 0)
    elif airplane['x'] > 1000:
        airplane['x'] = 1000
        airplane['roll'] = min(airplane['roll'], 0)
    
    # Boost timer
    if game_state['boost_timer'] > 0:
        game_state['boost_timer'] -= 1
        if game_state['boost_timer'] == 0:
            airplane['velocity'] = game_state['speed']

def setupCamera():
    """Configure camera based on current mode"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 5000)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera['mode'] == 0:  # Third-person view from behind the plane
        cam_distance = 300
        cam_height = 150
        
        # Position camera behind the airplane (negative Y direction)
        cam_x = airplane['x'] + 50  # Slightly to the side for better view
        cam_y = airplane['y'] - cam_distance  # Behind the airplane
        cam_z = airplane['z'] + cam_height  # Above the airplane
        
        gluLookAt(cam_x, cam_y, cam_z,
                 airplane['x'], airplane['y'], airplane['z'],
                 0, 0, 1)
    
    elif camera['mode'] == 1:  # First-person view from cockpit
        # Position camera at the cockpit, looking forward
        cam_x = airplane['x']
        cam_y = airplane['y'] - 20  # Slightly behind the cockpit center
        cam_z = airplane['z'] + 15  # At pilot eye level
        
        # Look ahead in the direction of flight with airplane orientation
        pitch_rad = math.radians(airplane['pitch'])
        yaw_rad = math.radians(airplane['yaw'])
        
        # Calculate forward direction
        look_distance = 500
        look_x = airplane['x'] + look_distance * math.sin(yaw_rad) * math.cos(pitch_rad)
        look_y = airplane['y'] + look_distance * math.cos(yaw_rad) * math.cos(pitch_rad)
        look_z = airplane['z'] + look_distance * math.sin(pitch_rad)
        
        # Up vector adjusted for roll
        roll_rad = math.radians(airplane['roll'])
        up_x = math.sin(roll_rad)
        up_y = 0
        up_z = math.cos(roll_rad)
        
        gluLookAt(cam_x, cam_y, cam_z,
                 look_x, look_y, look_z,
                 up_x, up_y, up_z)
    
    elif camera['mode'] == 2:  # Side view
        # Side view camera for better airplane visibility
        cam_distance = 400
        
        cam_x = airplane['x'] + cam_distance  # To the side
        cam_y = airplane['y'] - 100  # Slightly behind
        cam_z = airplane['z'] + 200  # Above
        
        gluLookAt(cam_x, cam_y, cam_z,
                 airplane['x'], airplane['y'], airplane['z'],
                 0, 0, 1)

def handle_crash():
    """Handle airplane crash"""
    game_state['lives'] -= 1
    if game_state['lives'] <= 0:
        game_state['game_over'] = True
    else:
        # Reset airplane position
        airplane['x'] = 0
        airplane['y'] = 0
        airplane['z'] = 50
        airplane['pitch'] = 0
        airplane['roll'] = 0
        airplane['yaw'] = 0

def update_level():
    """Update game difficulty based on time/score"""
    new_level = 1 + game_state['score'] // 500
    if new_level > game_state['level']:
        game_state['level'] = new_level
        game_state['speed'] += 0.5
        airplane['velocity'] = game_state['speed']
        
        # Add fewer enemies
        for i in range(1):  # Reduced from 2 to 1
            enemies.append({
                'x': random.uniform(-400, 400),
                'y': random.uniform(500, 1500),
                'z': random.uniform(150, 350),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'active': True
            })

def restart_game():
    """Restart the game"""
    global game_state, airplane, rings, obstacles, enemies, bullets, powerups
    
    game_state = {
        'score': 0,
        'lives': 3,
        'speed': 1.0,
        'boost_timer': 0,
        'game_over': False,
        'level': 1,
        'time': 0,
        'enemy_collision_count': 0,
        'cheat_mode': False,
        'cheat_fire_timer': 0
    }
    
    airplane = {
        'x': 0, 'y': 0, 'z': 50,
        'roll': 0, 'pitch': 0, 'yaw': 0,
        'velocity': 1.0,
        'horizontal_velocity': 0.0,
        'vertical_velocity': 0.0,
        'propeller_angle': 0
    }
    
    rings = []
    obstacles = []
    enemies = []
    bullets = []
    powerups = []
    
    # This will need to call init_game_objects from game_objects module
    # init_game_objects()

# Input handling functions
def keyboardListener(key, x, y):
    """Handle keyboard input"""
    global camera
    
    if game_state['game_over']:
        if key == b'r':
            restart_game()
        return
    
    # Flight controls
    if key == b'w':       # Ascend
        airplane['pitch'] = min(airplane['pitch'] + 5, 25)
        airplane['vertical_velocity'] += 3  # Add upward velocity
    elif key == b's':     # Descend
        airplane['pitch'] = max(airplane['pitch'] - 5, -25)
        airplane['vertical_velocity'] -= 3  # Add downward velocity
    elif key == b'a':     # Move left
        airplane['roll'] = min(airplane['roll'] + 8, 35)
        airplane['horizontal_velocity'] -= 4  # Add leftward velocity
    elif key == b'd':     # Move right
        airplane['roll'] = max(airplane['roll'] - 8, -35)
        airplane['horizontal_velocity'] += 4  # Add rightward velocity
    elif key == b'q':     # Move left directly (immediate)
        airplane['horizontal_velocity'] -= 8
    elif key == b'e':     # Move right directly (immediate)
        airplane['horizontal_velocity'] += 8
    
    if key == b' ':  # Spacebar to shoot
        from game_objects import fire_bullet
        fire_bullet()
        print("Bullet fired forward!")  # Audio feedback
    elif key == b'c':  # Change camera
        camera['mode'] = (camera['mode'] + 1) % 3  # Cycle through 3 camera modes
    elif key == b'x':  # Toggle cheat mode
        game_state['cheat_mode'] = not game_state['cheat_mode']
        if game_state['cheat_mode']:
            print("CHEAT MODE ACTIVATED - Invincible and auto-firing!")
        else:
            print("Cheat mode deactivated")
    elif key == b'r':
        restart_game()

def specialKeyListener(key, x, y):
    """Handle arrow keys"""
    if game_state['game_over']:
        return
    
    # Precise airplane controls with arrow keys
    if key == GLUT_KEY_UP:
        airplane['pitch'] = min(airplane['pitch'] + 4, 25)
        airplane['vertical_velocity'] += 2  # Add upward velocity
    elif key == GLUT_KEY_DOWN:
        airplane['pitch'] = max(airplane['pitch'] - 4, -25)
        airplane['vertical_velocity'] -= 2  # Add downward velocity
    elif key == GLUT_KEY_LEFT:
        airplane['roll'] = min(airplane['roll'] + 6, 35)
        airplane['horizontal_velocity'] -= 3  # Add leftward velocity
    elif key == GLUT_KEY_RIGHT:
        airplane['roll'] = max(airplane['roll'] - 6, -35)
        airplane['horizontal_velocity'] += 3  # Add rightward velocity

def mouseListener(button, state, x, y):
    """Handle mouse input"""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_state['game_over']:
            bullets.append({
                'x': airplane['x'],
                'y': airplane['y'] + 50,
                'z': airplane['z']
            })
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera['mode'] = (camera['mode'] + 1) % 3  # Cycle through 3 camera modes