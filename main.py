from objects import *


def variables():
    global fps, level, levels, clock, size, width, height
    clock = pygame.time.Clock()
    size = width, height = 1280, 424
    fps = 60
    levels = iter((DayLevel(), EveningLevel(), NightLevel()))
    right, left, jump, hold, climbjump = False, False, False, False, False
    level = None


def game_level():
    try:
        return next(levels)
    except Exception as e:
        print(e)


def event_checker():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            if event.key == pygame.K_HOME:
                level.spawn_player()

    keys = pygame.key.get_pressed()
    right, left = False, False
    if keys[pygame.K_RIGHT]:
        right = True
    elif keys[pygame.K_LEFT]:
        left = True
    if keys[pygame.K_SPACE] and not jump:
        jump = True
    return running, right, left, jump


def movements(right, left, jump):
    return x, y, action, right


def drawing(x, y, action, right):
    # Отрисовка уровня
    level.update()
    level.draw(screen)
    # Отрисовка игрока
    level.player.update(x, y, action, right)
    screen.blit(pygame.transform.scale(level.player.update(),
                                       (level.player.get_rect()[2], level.player.get_rect()[3])),
                (level.player.x, level.player.y))


def esc_menu():
    global run
    run = False


pygame.init()

variables()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
level = game_level()

# main loop
run = True
while run:
    run, right, left, jump = event_checker()
    x, y, action, right = movements(right, left, jump)
    drawing(x, y, action, right)
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
