from objects import *


def variables():
    global fps, right, left, jump, hold, climbjump, level, levels, clock, size, width, height, n
    clock = pygame.time.Clock()
    size = width, height = 1280, 424
    fps = 30
    levels = list((DayLevel(), EveningLevel(), NightLevel()))
    n = -1
    right, left, jump, hold, climbjump = False, False, False, False, False
    level = None


def game_level():
    global n
    if level is None or level.passed:
        n += 1 if n < 3 else 0
        return levels[n]
    elif level.player.hp == 0:
        n -= 1 if n != 0 else 0


def event_checker():
    global running, right, left, jump
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_menu()
            if event.key == pygame.K_HOME:
                level.spawn_player()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and level.player.x < 1235:
        right, left = True, False
    elif keys[pygame.K_LEFT] and level.player.x > 0:
        right, left = False, True
    else:
        right, left = False, False
    if keys[pygame.K_SPACE] and not jump:
        jump = True


def movements():
    global right, left, jump, hold, climbjump, on_floor
    if not jump:
        if not level.floor_collision(level.player.x, level.player.y + 1) and not hold:  # гравитация
            on_floor = True
            level.player.change_action('jump_%s' % level.player.last_action[-1])
            if level.floor_collision(level.player.x, level.player.y + level.player.vy):
                while not level.floor_collision(level.player.x, level.player.y):
                    level.player.y += 1
                level.player.y -= 1
            else:
                level.player.y += level.player.vy
                level.player.vy += 1
        if right and not hold:
            level.player.change_action('run_r')
            level.player.x += level.player.vx
            if level.wall_collision(level.player.x, level.player.y):
                hold = True
                level.player.change_action('climbhold_r')
                while level.wall_collision(level.player.x, level.player.y):
                    level.player.x -= 1
        elif left and not hold:
            level.player.change_action('run_l')
            level.player.x -= level.player.vx
            if level.wall_collision(level.player.x, level.player.y):
                hold = True
                level.player.change_action('climbhold_l')
                while level.wall_collision(level.player.x, level.player.y):
                    level.player.x += 1
        elif not hold and not on_floor and level.wall_collision(level.player.x, level.player.y):
            level.player.change_action('climbhold_%s' % level.player.last_action[-1])
            hold = True
        elif on_floor:
            level.player.change_action('idle_%s' % level.player.last_action[-1])

    elif jump:
        on_floor = False
        if 'hold' in level.player.last_action:
            level.player.change_action('climbjump_%s' % level.player.last_action[-1])
            climbjump = True
            hold = False
            level.player.vy = -7
        if climbjump:
            level.player.x += level.player.vx if level.player.last_action[-1] == 'l' else -level.player.vx
            level.player.y += level.player.vy
            level.player.vy += 1
            if level.player.vy == 0:
                climbjump = False
                jump = False
        else:
            if 'jump' not in level.player.last_action and not hold:
                level.player.vy = -10
            if right:
                level.player.change_action('jump_r')
                level.player.vy += 1
                if level.player.vy == 0:
                    jump = False
                else:
                    level.player.y += level.player.vy
                    level.player.x += level.player.vx
                    level.player.change_action('jump_r')
                if level.wall_collision(level.player.x, level.player.y):
                    jump = False
                    hold = True
                    level.player.change_action('climbhold_r')
                    while level.wall_collision(level.player.x, level.player.y):
                        level.player.x -= 1
            elif left:
                level.player.vy += 1
                if level.player.vy == 0:
                    jump = False
                else:
                    level.player.y += level.player.vy
                    level.player.x -= level.player.vx
                    level.player.change_action('jump_l')
                if level.wall_collision(level.player.x, level.player.y):
                    jump = False
                    hold = True
                    level.player.change_action('climbhold_l')
                    while level.wall_collision(level.player.x, level.player.y):
                        level.player.x += 1
            else:
                level.player.vy += 1
                if level.player.vy == 0:
                    jump = False
                else:
                    level.player.y += level.player.vy
                    level.player.change_action('jump_%s' % level.player.last_action[-1])
                if level.wall_collision(level.player.x, level.player.y):
                    jump = False
                    hold = True
                    level.player.change_action('climbhold_%s' % level.player.last_action[-1])

    if level.trap_collision(level.player.x, level.player.y):
        level.player.hp -= 1
        if level.player.hp == 0:
            print('died')
        level.player.change_action('deadfall_%s' % level.player.last_action[-1])
        pygame.time.delay(1000)
        level.spawn_player()


def drawing():
    # Отрисовка уровня
    screen.blit(pygame.transform.scale(level.background, (1280, 424)), (0, 0))
    for block in level.blocks:
        screen.blit(block.image, block.pos)
    # Отрисовка игрока
    screen.blit(pygame.transform.scale(level.player.update(),
                                       (level.player.get_rect()[2], level.player.get_rect()[3])),
                (level.player.x, level.player.y))


def esc_menu():
    global running
    running = False


pygame.init()

variables()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
level = game_level()

# main loop
running = True
while running:
    event_checker()
    movements()
    drawing()
    # updating frame
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
