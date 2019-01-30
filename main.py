import pygame
from random import randrange
from objects import Player


def drawing():
    screen.blit(pygame.transform.scale(pygame.image.load(background), (1280, 424)), (0, 0))
    screen.blit(pygame.transform.scale(player.update(), (player.get_rect()[2] * 2, player.get_rect()[3] * 2)),
                (player.x, player.y))


def esc_menu():
    global running
    running = False


pygame.init()

clock = pygame.time.Clock()
info = pygame.display.Info()
size = width, height = 1280, 424
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
backgrounds = ('data/background/daybackground.png', 'data/background/eveningbackground.png',
               'data/background/nightbackground.png')
background = backgrounds[0]
pygame.display.set_caption('THE GAME')
fps = 30

player = Player(25, 3)
# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            elif event.key == pygame.K_F11:
                pygame.display.iconify()
            elif event.key == pygame.K_SPACE:
                background = backgrounds[randrange(3)]
    drawing()
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
