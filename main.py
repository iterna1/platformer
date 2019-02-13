from objects import *
from interactions import *


def game_level():
    try:
        return next(levels)
    except Exception as e:
        print(e)


def event_checker():
    global ingame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ingame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            if event.key == pygame.K_HOME:
                level.spawn_player()

    keys = pygame.key.get_pressed()
    right, left, space = False, False, False
    if keys[pygame.K_RIGHT]:
        right = True
    elif keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_SPACE]:
        space = True
    return right, left, space


def movements(k_right, k_left, k_space):
    action, right = level.player.sprite

    if floor_collision(level):
        level.player.vy = 0
        if k_space:
            level.player.vy = -5
            action = 'jump'
        if k_right:
            level.player.vx = 2
            action = 'run'
            right = True
        if k_left:
            level.player.vx = -2
            action = 'run'
            right = False
    elif wall_collision(level):
        self.vy = 1

    elif trap_collision(level):
        pass

    else:
        level.player.vy += 1
        action = 'jump'
        if k_right:
            level.player.vx = 2
            right = True
        elif k_left:
            level.player.vx = -2
            right = False
    level.update(action, right)


def drawing():
    # Отрисовка уровня
    level.draw(screen)


def esc_menu():
    global ingame
    ingame = False


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('game')

levels = iter((DayLevel(), EveningLevel(), NightLevel()))
level = game_level()
level.spawn_player()

# main loop
ingame = True
while ingame:
    # updating level
    movements(*event_checker())  # event checker returns buttons which are pressed
    # drawing
    drawing()
    # updating frame
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
