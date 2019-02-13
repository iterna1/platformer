import pygame
from objects import *


def wall_collision(level):
    object = pygame.sprite.spritecollideany(level.player, level.walls)
    return False if object is None else False


def floor_collision(level):
    object = pygame.sprite.spritecollideany(level.player, level.floors)
    return False if object is None else False


def trap_collision(level):
    object = pygame.sprite.spritecollideany(level.player, level.traps)
    return False if object is None else False
