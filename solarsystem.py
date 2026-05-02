from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

angle = 0

# spaceship camera
shipX, shipY, shipZ = 0, 1, 5

planets = [
    ["Mercury", 0.03, 0.35, (0.55, 0.54, 0.52), 4.7],
    ["Venus",   0.05, 0.50, (0.90, 0.78, 0.55), 3.5],
    ["Earth",   0.055,0.65, (0.20, 0.45, 1.00), 2.8],
    ["Mars",    0.045,0.80, (0.85, 0.35, 0.22), 2.3],
    ["Jupiter", 0.11, 1.05, (0.85, 0.72, 0.55), 1.3],
    ["Saturn",  0.09, 1.30, (0.95, 0.85, 0.65), 1.0],
    ["Uranus",  0.07, 1.50, (0.60, 0.88, 0.86), 0.8],
    ["Neptune", 0.07, 1.70, (0.35, 0.50, 0.95), 0.6]
]

stars = []
asteroids = []

def init():
    glClearColor(0, 0, 0.05, 1)
    glEnable(GL_DEPTH_TEST)

    # lighting (sun light)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
    
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])

    glEnable(GL_COLOR_MATERIAL)

    for _ in range(2000):  
        stars.append((
            random.uniform(-25, 25), 
            random.uniform(-15, 15),   
            random.uniform(-30, 15)   
        ))

    # asteroid belt
    for _ in range(200):
        r = random.uniform(0.85, 1.0)
        ang = random.uniform(0, 360)
        asteroids.append((r, ang))

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h if h != 0 else 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)

def drawStars():
    glDisable(GL_LIGHTING)
    glPointSize(1.5) 
    glBegin(GL_POINTS)
    for s in stars:
        brightness = random.uniform(0.4, 1.0)
        glColor3f(brightness, brightness, brightness)
        glVertex3f(s[0], s[1], s[2])
    glEnd()
    glEnable(GL_LIGHTING)

def drawSun():
    glDisable(GL_LIGHTING)

    glColor3f(1.0, 0.8, 0.2)
    glutSolidSphere(0.13, 50, 50)

    glColor4f(1.0, 0.7, 0.2, 0.3)
    glutSolidSphere(0.18, 30, 30)

    glEnable(GL_LIGHTING)

def drawPlanet(size, color):
    glColor3f(*color)
    glutSolidSphere(size, 30, 30)

def drawOrbit(r):
    glDisable(GL_LIGHTING)
    glColor3f(0.3, 0.3, 0.4)
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        rad = math.radians(i)
        glVertex3f(r*math.cos(rad), r*math.sin(rad), 0)
    glEnd()
    glEnable(GL_LIGHTING)

def drawRing():
    glDisable(GL_LIGHTING)
    glColor3f(0.9, 0.85, 0.7)
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        rad = math.radians(i)
        glVertex3f(0.18*math.cos(rad), 0.08*math.sin(rad), 0)
    glEnd()
    glEnable(GL_LIGHTING)

def drawAsteroids():
    glColor3f(0.6, 0.6, 0.6)
    for a in asteroids:
        glPushMatrix()
        glRotatef(a[1] + angle, 0, 0, 1)
        glTranslatef(a[0], 0, 0)
        glutSolidSphere(0.012, 10, 10)
        glPopMatrix()

def display():
    global angle, shipX, shipY, shipZ

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(shipX, shipY, shipZ, 0, 0, 0, 0, 1, 0)

    drawStars()
    drawSun()
    drawAsteroids()

    for p in planets:
        orbit = p[2]

        drawOrbit(orbit)

        glPushMatrix()
        glRotatef(angle * p[4], 0, 0, 1)
        glTranslatef(orbit, 0, 0)

        # self rotation
        glRotatef(angle * 5, 0, 1, 0)
        drawPlanet(p[1], p[3])

        if p[0] == "Saturn":
            drawRing()

        if p[0] == "Earth":
            glPushMatrix()
            glRotatef(angle * 6, 0, 0, 1)
            glTranslatef(0.12, 0, 0)
            drawPlanet(0.015, (0.8, 0.8, 0.8))
            glPopMatrix()

        glPopMatrix()

    glutSwapBuffers()

def update(v):
    global angle
    angle += 0.4
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global shipX, shipY, shipZ
    
    step = 0.5
    
    if key == b'w':
        shipZ -= step
    elif key == b's':
        shipZ += step
    elif key == b'a':
        shipX -= step
    elif key == b'd':
        shipX += step
    elif key == b'q':
        shipY += step
    elif key == b'e':
        shipY -= step
    elif key == b'r':
        shipX, shipY, shipZ = 0, 1, 5
    
    glutPostRedisplay()

def special_keys(key, x, y):
    global shipX, shipY, shipZ
    
    step = 0.5
    
    if key == GLUT_KEY_UP:
        shipZ -= step
    elif key == GLUT_KEY_DOWN:
        shipZ += step
    elif key == GLUT_KEY_LEFT:
        shipX -= step
    elif key == GLUT_KEY_RIGHT:
        shipX += step
    elif key == GLUT_KEY_PAGE_UP:
        shipY += step
    elif key == GLUT_KEY_PAGE_DOWN:
        shipY -= step
    
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(900, 900)
    glutCreateWindow(b"Solar System Ultimate - Full Stars")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, update, 0)

    glutMainLoop()

main()
