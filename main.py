import pygame
from random import randrange
from objects import *


def game_level():
    screen.blit(pygame.transform.scale(DayLevel.background, (1280, 424)), (0, 0))
    level = DayLevel()
    for block in level.blocks:
        screen.blit(block.image, block.pos)


def event_checker():
    global running, background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            elif event.key == pygame.K_DELETE:
                background = backgrounds[randrange(3)]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and 'jump' not in player.last_action:
        player.change_action('run_r')
        player.x += 5
    elif keys[pygame.K_LEFT] and 'jump' not in player.last_action:
        player.x -= 5
        player.change_action('run_l')
    elif keys[pygame.K_SPACE]:
        player.change_action('jump_%s' % player.last_action[-1])
        player.y -= 10
    else:
        player.change_action('idle_%s' % player.last_action[-1])


def drawing():
    # Отрисовка уровня
    game_level()

    # Отрисовка игрока
    screen.blit(pygame.transform.scale(player.update(), (player.get_rect()[2] * 2, player.get_rect()[3] * 2)),
                (player.x, player.y))


def esc_menu():
    global running
    running = False


pygame.init()

clock = pygame.time.Clock()
info = pygame.display.Info()
size = width, height = 1280, 424
screen = pygame.display.set_mode(size)
backgrounds = ('data/background/daybackground.png', 'data/background/eveningbackground.png',
               'data/background/nightbackground.png')
background = backgrounds[0]
pygame.display.set_caption('')
fps = 30

player = Player(30, 314)
# main loop
running = True
while running:
    event_checker()
    drawing()
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
