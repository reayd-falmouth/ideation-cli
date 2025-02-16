import struct
import pygame
from pygame.locals import *

import moderngl

pygame.init()

FPS = 30
clock = pygame.time.Clock()

VIRTUAL_RES = (160, 120)
REAL_RES = (800, 600)

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
pygame.display.set_mode(REAL_RES, DOUBLEBUF | OPENGL)

ctx = moderngl.create_context()

texture_coordinates = [0, 1, 1, 1, 0, 0, 1, 0]

world_coordinates = [-1, -1, 1, -1, -1, 1, 1, 1]

render_indices = [0, 1, 2, 1, 2, 3]

prog = ctx.program(
    vertex_shader=open("shaders/vertex.glsl").read(),
    fragment_shader=open("shaders/fragment.glsl").read(),
)

screen_texture = ctx.texture(VIRTUAL_RES, 3, pygame.image.tostring(screen, "RGB", 1))

screen_texture.repeat_x = False
screen_texture.repeat_y = False

vbo = ctx.buffer(struct.pack("8f", *world_coordinates))
uvmap = ctx.buffer(struct.pack("8f", *texture_coordinates))
ibo = ctx.buffer(struct.pack("6I", *render_indices))

vao_content = [(vbo, "2f", "vert"), (uvmap, "2f", "in_text")]

vao = ctx.vertex_array(prog, vao_content, ibo)


def render():
    texture_data = screen.get_view("1")
    screen_texture.write(texture_data)
    ctx.clear(14 / 255, 40 / 255, 66 / 255)
    screen_texture.use()
    vao.render()
    pygame.display.flip()


# MAIN LOOP

done = False

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    screen.fill((255, 0, 255))
    pygame.draw.circle(screen, (0, 0, 0), (100, 100), 20)
    pygame.draw.circle(screen, (0, 0, 200), (0, 0), 10)
    pygame.draw.circle(screen, (200, 0, 0), (160, 120), 30)
    pygame.draw.line(screen, (250, 250, 0), (0, 120), (160, 0))

    render()
    clock.tick(FPS)
