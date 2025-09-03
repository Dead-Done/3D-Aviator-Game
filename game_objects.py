from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Import from core module
from game_core import (
    game_state, airplane, rings, obstacles, enemies, bullets, powerups, explosions,
    RECYCLE_DISTANCE_BEHIND, SPAWN_DISTANCE_AHEAD, handle_crash
)

def recycle_objects():
    """Recycle objects that are far behind the airplane to create infinite gameplay"""
    # Rings
    for ring in rings:
        if ring['y'] < airplane['y'] - RECYCLE_DISTANCE_BEHIND:
            ring['y'] = airplane['y'] + SPAWN_DISTANCE_AHEAD
            ring['x'] = random.uniform(-500, 500)
            ring['z'] = random.uniform(100, 300)
            ring['collected'] = False
    # Obstacles
    for obs in obstacles:
        if obs['y'] < airplane['y'] - RECYCLE_DISTANCE_BEHIND:
            obs['y'] = airplane['y'] + SPAWN_DISTANCE_AHEAD
            obs['x'] = random.uniform(-600, 600)
            obs['z'] = random.uniform(50, 400)
            obs['type'] = random.choice(['cloud', 'rock', 'balloon'])
    # Enemies - spawn them in front of the airplane
    for enemy in enemies:
        if enemy['y'] < airplane['y'] + 200 or not enemy['active']:  # More aggressive recycling
            # Spawn enemies far in front of the airplane (positive Y direction)
            enemy['x'] = airplane['x'] + random.uniform(-400, 400)  # Wider spread left/right
            enemy['y'] = airplane['y'] + random.uniform(1500, 3000)  # Much further ahead
            enemy['z'] = airplane['z'] + random.uniform(-150, 150)  # Wider altitude range
            enemy['active'] = True
    # Powerups
    for pu in powerups:
        if pu['y'] < airplane['y'] - RECYCLE_DISTANCE_BEHIND or pu['collected']:
            pu['y'] = airplane['y'] + SPAWN_DISTANCE_AHEAD
            pu['x'] = random.uniform(-300, 300)
            pu['z'] = random.uniform(100, 250)
            pu['collected'] = False

def init_game_objects():
    """Initialize game objects like rings, obstacles, enemies"""
    global rings, obstacles, enemies, powerups
    
    # Create rings to fly through
    for i in range(5):
        rings.append({
            'x': random.uniform(-500, 500),
            'y': 200 + i * 300,
            'z': random.uniform(100, 300),
            'collected': False
        })
    
    # Create obstacles
    for i in range(8):
        obstacles.append({
            'x': random.uniform(-600, 600),
            'y': random.uniform(100, 1500),
            'z': random.uniform(50, 400),
            'type': random.choice(['cloud', 'rock', 'balloon'])
        })
    
    # Create enemy planes far in front of the airplane
    for i in range(3):
        # Spawn enemies far in front of the airplane (positive Y direction)
        enemies.append({
            'x': airplane['x'] + random.uniform(-400, 400),  # Wider spread left/right
            'y': airplane['y'] + 1500 + (i * 600),  # Much further and more staggered
            'z': airplane['z'] + random.uniform(-150, 150),  # Wider altitude range
            'active': True
        })
    
    # Create power-ups
    for i in range(3):
        powerups.append({
            'x': random.uniform(-300, 300),
            'y': random.uniform(200, 1000),
            'z': random.uniform(100, 250),
            'collected': False
        })

def create_explosion(x, y, z):
    """Create explosion effect at given position"""
    explosions.append({
        'x': x, 'y': y, 'z': z,
        'timer': 30,  # Explosion duration
        'size': 10
    })

def update_explosions():
    """Update explosion effects"""
    for explosion in explosions[:]:
        explosion['timer'] -= 1
        if explosion['timer'] <= 0:
            explosions.remove(explosion)

def update_enemies():
    """Update enemy AI movement"""
    for enemy in enemies:
        if not enemy['active']:
            continue
        
        # Calculate direction towards player
        dx = airplane['x'] - enemy['x']
        dy = airplane['y'] - enemy['y']
        dz = airplane['z'] - enemy['z']
        
        # Calculate distance to player
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # CRITICAL: Ensure enemy never goes behind the airplane
        # If enemy is behind or at same Y position, move it forward
        if enemy['y'] <= airplane['y']:
            enemy['y'] = airplane['y'] + 200  # Push enemy forward
        
        if distance > 0:
            # Only move towards player if enemy is in front
            if enemy['y'] > airplane['y']:
                # Normalize direction vector
                dx /= distance
                dy /= distance
                dz /= distance
                
                # Move towards player at slower, more predictable speed
                enemy_speed = 0.2 + (game_state['level'] * 0.05)  # Reduced from 0.4 and 0.1
                
                # Only allow movement that keeps enemy in front
                new_x = enemy['x'] + dx * enemy_speed
                new_y = enemy['y'] + dy * enemy_speed
                new_z = enemy['z'] + dz * enemy_speed
                
                # Ensure new Y position is always ahead of airplane
                if new_y > airplane['y']:
                    enemy['x'] = new_x
                    enemy['y'] = new_y
                    enemy['z'] = new_z
                else:
                    # If movement would put enemy behind, only move sideways and down
                    enemy['x'] += dx * enemy_speed * 0.3  # Even slower sideways movement
                    enemy['z'] += dz * enemy_speed
                    # Keep enemy ahead
                    enemy['y'] = max(enemy['y'], airplane['y'] + 100)
                
                # Minimal evasive movement to keep them predictable for shooting
                evasion_factor = math.sin(game_state['time'] * 0.05 + enemy['y'] * 0.005) * 5
                enemy['x'] += evasion_factor * 0.05
                enemy['z'] += math.cos(game_state['time'] * 0.04 + enemy['x'] * 0.005) * 3 * 0.05
        
        # Deactivate enemies that get too close or too far, but NEVER if they're behind
        if distance < 50 or distance > 2000:
            enemy['active'] = False
        
        # Extra safety: if somehow enemy gets behind, deactivate and respawn
        if enemy['y'] < airplane['y'] - 50:
            enemy['active'] = False

def fire_bullet():
    """Fire a bullet from the airplane"""
    # Airplane always moves forward in +Y direction
    # Calculate pitch-based trajectory (up/down based on airplane pitch)
    pitch_rad = math.radians(airplane['pitch'])
    
    # Forward direction: +Y with pitch adjustment
    forward_x = 0  # No left/right movement
    forward_y = math.cos(pitch_rad)  # Forward (always positive Y)
    forward_z = math.sin(pitch_rad)  # Up/down based on pitch
    
    # Create bullet at airplane's nose position
    bullets.append({
        'x': airplane['x'],  # Same X as airplane
        'y': airplane['y'] + 50,  # Start ahead of plane
        'z': airplane['z'] + 20,  # Slightly above airplane center
        'dir_x': forward_x,  # Direction vector
        'dir_y': forward_y,
        'dir_z': forward_z,
        'speed': 30  # Faster bullets
    })

def update_bullets():
    """Update bullet positions"""
    for bullet in bullets[:]:
        # Move bullets in their forward direction
        speed = bullet.get('speed', 20)
        
        # Use direction vector if available, otherwise default to +Y (forward)
        dir_x = bullet.get('dir_x', 0)
        dir_y = bullet.get('dir_y', 1)
        dir_z = bullet.get('dir_z', 0)
        
        bullet['x'] += dir_x * speed
        bullet['y'] += dir_y * speed
        bullet['z'] += dir_z * speed
        
        # Remove bullets that go too far from airplane
        dist_from_plane = math.sqrt((bullet['x'] - airplane['x'])**2 + 
                                   (bullet['y'] - airplane['y'])**2 + 
                                   (bullet['z'] - airplane['z'])**2)
        if dist_from_plane > 1000:
            bullets.remove(bullet)
            continue
        
        # Check collision with enemies
        for enemy in enemies:
            if not enemy['active']:
                continue
            
            dist = math.sqrt((bullet['x']-enemy['x'])**2 + 
                           (bullet['y']-enemy['y'])**2 + 
                           (bullet['z']-enemy['z'])**2)
            if dist < 30:
                # Create explosion effect
                create_explosion(enemy['x'], enemy['y'], enemy['z'])
                enemy['active'] = False
                bullets.remove(bullet)
                game_state['score'] += 100  # Increased score for shooting enemies
                print(f"Enemy destroyed! Score: {game_state['score']}")  # Audio feedback
                break

def check_collisions():
    """Check collisions between airplane and objects"""
    if game_state['game_over']:
        return
    
    # Check ring collection
    for ring in rings:
        if ring['collected']:
            continue
        
        dist = math.sqrt((airplane['x']-ring['x'])**2 + 
                        (airplane['y']-ring['y'])**2 + 
                        (airplane['z']-ring['z'])**2)
        if dist < 80:
            ring['collected'] = True
            game_state['score'] += 100
    
    # Check obstacle collision
    for obs in obstacles[:]:  # Use slice copy to safely remove items
        dist = math.sqrt((airplane['x']-obs['x'])**2 + 
                        (airplane['y']-obs['y'])**2 + 
                        (airplane['z']-obs['z'])**2)
        
        # Clouds are non-collidable - plane passes through them
        if obs['type'] == 'cloud':
            continue
            
        # Other obstacles (rocks, balloons)
        threshold = 40
        if dist < threshold:
            if game_state['boost_timer'] > 0:
                # During boost: break through obstacles without damage
                obstacles.remove(obs)
                # Create explosion effect for breaking through
                create_explosion(obs['x'], obs['y'], obs['z'])
                game_state['score'] += 50  # Bonus points for breaking obstacles
            else:
                # Normal behavior: crash and lose life
                handle_crash()
                obstacles.remove(obs)
            break
    
    # Check enemy collision - count collisions instead of immediate crash
    for enemy in enemies:
        if not enemy['active']:
            continue
        
        dist = math.sqrt((airplane['x']-enemy['x'])**2 + 
                        (airplane['y']-enemy['y'])**2 + 
                        (airplane['z']-enemy['z'])**2)
        if dist < 35:
            if game_state['boost_timer'] > 0 or game_state['cheat_mode']:
                # During boost or cheat mode: destroy enemies without damage
                enemy['active'] = False
                create_explosion(enemy['x'], enemy['y'], enemy['z'])
                game_state['score'] += 150  # Bonus points for ramming enemies
            else:
                # Normal behavior: count collision
                game_state['enemy_collision_count'] += 1
                enemy['active'] = False
                
                # Check if player should lose a life after 5 enemy collisions
                if game_state['enemy_collision_count'] >= 5:
                    handle_crash()
                    game_state['enemy_collision_count'] = 0  # Reset counter
            break
    
    # Check powerup collection
    for powerup in powerups:
        if powerup['collected']:
            continue
        
        dist = math.sqrt((airplane['x']-powerup['x'])**2 + 
                        (airplane['y']-powerup['y'])**2 + 
                        (airplane['z']-powerup['z'])**2)
        if dist < 35:  # Slightly larger collection radius
            powerup['collected'] = True
            game_state['boost_timer'] = 420  # 7 seconds at 60 FPS
            airplane['velocity'] = game_state['speed'] * 5  # Much faster boost speed
            
            # Create explosion effect at powerup location for visual feedback
            create_explosion(powerup['x'], powerup['y'], powerup['z'])
            
            # Bonus score for collecting powerup
            game_state['score'] += 200
            
            print("BOOST POWERUP COLLECTED! 7 seconds of invulnerability and super speed!")  # Console feedback