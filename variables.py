import pygame
import sys
from itertools import cycle

FPS = 30
GRAVITY = 0.7
ANIMATION_SPEED = FPS // 4  # lower == faster | FPS // N -> N animation cycles in 60 frames
SIZE = WIDTH, HEIGHT = 1280, 424  # screen size
volumes = cycle((100, 0))  # music volumes when you switch between "off" and "on"

pygame.init()
clock = pygame.time.Clock()
ingame = True

screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN | pygame.DOUBLEBUF)
pygame.display.set_caption("The Walkthrough")
