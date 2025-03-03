import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

rotation_angle = 0

num_sectors = 8

start_colors = [(random.random(), random.random(), random.random()) for _ in range(num_sectors)]
target_colors = [(random.random(), random.random(), random.random()) for _ in range(num_sectors)]

color_change_duration = 1

last_color_change_time = pygame.time.get_ticks()

def draw_dial():
    global rotation_angle, start_colors, target_colors, last_color_change_time

    glRotatef(1, 0, 0, 1)
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0

    current_time = pygame.time.get_ticks()

    elapsed_time = (current_time - last_color_change_time) / 1000  # 转换为秒
    progress = min(elapsed_time / color_change_duration, 1)

    if elapsed_time >= color_change_duration:
        start_colors = target_colors
        target_colors = [(random.random(), random.random(), random.random()) for _ in range(num_sectors)]
        last_color_change_time = current_time

    for i in range(num_sectors):
        start_angle = 2 * math.pi * i / num_sectors
        end_angle = 2 * math.pi * (i + 1) / num_sectors

        current_color = [
            start_colors[i][j] + (target_colors[i][j] - start_colors[i][j]) * progress
            for j in range(3)
        ]

        glBegin(GL_TRIANGLES)
        glColor3fv(current_color)
        glVertex3f(0, 0, 0)
        for j in range(2):
            angle = start_angle if j == 0 else end_angle
            x = 0.8 * math.cos(angle)
            y = 0.8 * math.sin(angle)
            glVertex3f(x, y, 0)
        glEnd()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_dial()
    pygame.display.flip()
    pygame.time.wait(10)