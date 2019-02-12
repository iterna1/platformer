from objects import *


def variables():
    global fps, levels, clock, size, width, height
    clock = pygame.time.Clock()
    size = width, height = 1280, 424
    fps = 60
    levels = iter((DayLevel(), EveningLevel(), NightLevel()))


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
    right, left, jump = False, False, False
    if keys[pygame.K_RIGHT]:
        right = True
    elif keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_SPACE] and not jump:
        jump = True
    return right, left, jump


def movements(k_right, k_left, k_jump):
    right = True
    action = level.player.sprite.name
    if k_jump:
        level.player.vy = -2
        action = 'jump'
    if k_right:
        level.player.vx = 1
        action = 'run'
        right = True
    elif k_left:
        level.player.vx = -1
        action = 'run'
        right = False

    level.player.sprite.rect.move_ip(level.player.vx, level.player.vy)
    return action, right


def drawing(action, right):
    # Отрисовка уровня
    level.update()
    level.draw(screen)
    # Отрисовка игрока
    level.player.update(level.player.sprite.rect.x + level.player.vx, level.player.sprite.rect.y + level.player.vy,
                        action, right)
    screen.blit(level.player.sprite.image, (level.player.sprite.rect.x, level.player.sprite.rect.y))


def esc_menu():
    global run
    run = False


pygame.init()

variables()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
level = game_level()
level.spawn_player()

# main loop
ingame = True
while ingame:
    drawing(*movements(*event_checker()))
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
