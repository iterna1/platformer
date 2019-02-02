import pygame
from objects import *


def variables():
    global fps, g, right, left, jump, idle, level, levels, clock, size, width, height
    clock = pygame.time.Clock()
    size = width, height = 1280, 424
    fps = 30
    g = 10
    levels = iter((EveningLevel(), DayLevel(), EveningLevel(), NightLevel()))
    right, left, jump, idle = False, False, False, False
    level = None


def game_level():
    global level
    if level is None or level.passed:
        level = next(levels)


def event_checker():
    global running, right, left, jump, idle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            if event.key == pygame.K_HOME:
                level.spawn_player()

    player = level.player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        right, left, idle = True, False, False
    elif keys[pygame.K_LEFT]:
        right, left, idle = False, True, False
    else:
        right, left = False, False
    if keys[pygame.K_SPACE] and not jump:
        jump, idle = True, False
        level.player.jump_time = 0
    if not any((right, left, jump)) or (jump and level.player.jump_time > 20):
        right, left, jump, idle = False, False, False, True

    if not jump:
        if right:
            level.player.change_action('run_r')
            level.player.x += level.player.vx
        elif left:
            level.player.change_action('run_l')
            level.player.x -= level.player.vx
        elif idle:
            level.player.change_action('idle_%s' % level.player.last_action[-1])
    else:
        if right:
            level.player.change_action('jump_r')
            level.player.vy += 1
            if level.player.vy > 10:
                level.player.vy = -11
                jump = False
            else:
                level.player.y += level.player.vy
                level.player.x += level.player.vx
                level.player.change_action('jump_r')
            level.player.jump_time += 1
        elif left:
            level.player.vy += 1
            if level.player.vy > 10:
                level.player.vy = -11
                jump = False
            else:
                level.player.y += level.player.vy
                level.player.x -= level.player.vx
                level.player.change_action('jump_l')
            level.player.jump_time += 1
        else:
            level.player.vy += 1
            if level.player.vy > 10:
                level.player.vy = -11
                jump = False
            else:
                level.player.y += level.player.vy
                level.player.change_action('jump_%s' % level.player.last_action[-1])
            level.player.jump_time += 1
    if level.collision(level.player.get_rect()):
        level.player = player


def drawing():
    # Отрисовка уровня
    screen.blit(pygame.transform.scale(level.background, (1280, 424)), (0, 0))
    for block in level.blocks:
        screen.blit(block.image, block.pos)
    # Отрисовка игрока
    screen.blit(pygame.transform.scale(level.player.update(),
                                       (level.player.get_rect()[2] * 2, level.player.get_rect()[3] * 2)),
                (level.player.x, level.player.y))


def esc_menu():
    global running
    running = False


pygame.init()

variables()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')

# main loop
running = True
while running:
    game_level()
    event_checker()
    drawing()
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
