from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Import from other modules
from game_core import (
    game_state, airplane, camera, GRID_SIZE, GRID_LINES,
    update_airplane, setupCamera, keyboardListener, 
    specialKeyListener, mouseListener, restart_game
)
from game_objects import (
    rings, obstacles, enemies, bullets, powerups, explosions,
    init_game_objects, recycle_objects, update_enemies, 
    update_bullets, update_explosions, check_collisions, fire_bullet
)

def draw_airplane():
    """Draw the airplane model using basic shapes"""
    glPushMatrix()
    
    # Apply airplane transformations
    glTranslatef(airplane['x'], airplane['y'], airplane['z'])
    glRotatef(airplane['yaw'], 0, 0, 1)
    glRotatef(airplane['pitch'], 1, 0, 0)
    glRotatef(airplane['roll'], 0, 1, 0)
    
    # Fuselage (body)
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glScalef(1, 3, 0.5)
    glutSolidCube(30)
    glPopMatrix()
    
    # Wings
    glPushMatrix()
    glColor3f(0.8, 0.8, 0.8)
    glScalef(5, 0.3, 0.2)
    glutSolidCube(30)
    glPopMatrix()
    
    # Tail vertical
    glPushMatrix()
    glTranslatef(0, -35, 10)
    glColor3f(0.6, 0.6, 0.6)
    glScalef(0.2, 0.5, 1.5)
    glutSolidCube(30)
    glPopMatrix()
    
    # Tail horizontal
    glPushMatrix()
    glTranslatef(0, -35, 5)
    glColor3f(0.6, 0.6, 0.6)
    glScalef(2, 0.3, 0.2)
    glutSolidCube(20)
    glPopMatrix()
    
    # Propeller
    glPushMatrix()
    glTranslatef(0, 45, 0)
    glRotatef(airplane['propeller_angle'], 0, 1, 0)
    glColor3f(0.3, 0.3, 0.3)
    glScalef(2, 0.1, 0.3)
    glutSolidCube(25)
    glPopMatrix()
    
    # Cockpit
    glPushMatrix()
    glTranslatef(0, 10, 8)
    glColor3f(0.2, 0.2, 0.5)
    glutSolidCube(15)
    glPopMatrix()
    
    glPopMatrix()

def draw_ring(ring):
    """Draw a ring to fly through"""
    if ring['collected']:
        return
    
    glPushMatrix()
    glTranslatef(ring['x'], ring['y'], ring['z'])
    glRotatef(90, 1, 0, 0)
    
    # Outer ring
    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 80, 80, 20, 20, 5)
    
    # Inner hole (visual representation)
    glColor3f(0.5,