from variables import *
from objects import *


def terminate():
    pygame.quit()
    sys.exit()


def change_level():
    try:
        return next(levels)
    except Exception as e:
        print(e)


def escape():
    width, height = escape_fon.get_width(), escape_fon.get_height()
    screen.blit(escape_fon, (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2))
    pygame.draw.rect(escape_fon, (0, 0, 0), (0, 0, width - 1, height - 1), 4)

    player_sheet = pygame.Rect(14, height // 3, width // 3, height - height // 3 - 14)
    pygame.draw.rect(escape_fon, (100, 100, 100), player_sheet, 2)
    # дорисовать игрока в этом окошке
    # ...
    exit_button_xy = (width // 2 + 14, height - height // 5)
    button_size = (width // 2 - 28, height // 5)
    exit_button = Button((50, 50, 50), *exit_button_xy, *button_size)
    exit_button.set_font('data/fonts/font.ttf', 50)
    exit_button.set_text('Exit', (255, 204, 0))
    screen.blit(exit_button.button, (exit_button.rect.x, exit_button.rect.y))

    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.pressed(event.pos):
                terminate()
        pygame.time.delay(50)


def begin():
    screen.blit(begin_fon, (0, 0))
    text_coord = 50
    for line in intro_text:
        string_rendered = begin_screen_font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return
        pygame.time.delay(50)


def mainloop():
    # main loop
    while ingame:
        # updating level
        movements(*event_checker())
        level.draw(screen)
        # updating frame
        pygame.display.flip()
        clock.tick(FPS)
    return


def end():
    pass


def movements(k_right, k_left, k_space):
    action = level.player.sprite.name
    if floor_collision(level):
        level.player.vy = 0
        if k_space:
            level.player.vy = -4
            action = 'jump'
        if k_right:
            level.player.vx = 2
            action = 'run'
        if k_left:
            level.player.vx = -2
            action = 'run'
    elif wall_collision(level):
        level.player.vy = 1
        action = 'hold'

    elif trap_collision(level):
        pass

    else:
        level.player.vy += 1
        action = 'jump'
        if k_right:
            level.player.vx = 2
        elif k_left:
            level.player.vx = -2
    wall_collision(level)
    floor_collision(level)

    level.update(action)


def event_checker():
    global ingame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ingame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape()
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


def wall_collision(lvl):
    obj = pygame.sprite.spritecollideany(lvl.player, lvl.walls)
    if obj is not None:
        if lvl.player.vx < 0:
            lvl.player.rect.x = obj.rect.x + 1
        else:
            lvl.player.rect.x = obj.rect.x - lvl.player.rect[2] - 1
    return False if obj is None else True


def floor_collision(lvl):
    obj = pygame.sprite.spritecollideany(lvl.player, lvl.floors)
    if obj is not None:
        if lvl.player.vy < 0:
            lvl.player.rect.y = obj.rect.y + 1
        else:
            lvl.player.rect.y = obj.rect.y - lvl.player.rect[3] - 1
    return False if obj is None else True


def trap_collision(lvl):
    obj = pygame.sprite.spritecollideany(lvl.player, lvl.traps)
    return False if obj is None else True


levels = iter((DayLevel(), EveningLevel(), NightLevel()))
level = change_level()
level.spawn_player()
