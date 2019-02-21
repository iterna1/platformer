from variables import *
from classes import *


def terminate():
    pygame.quit()
    sys.exit()


def change_level():
    try:
        return next(levels)
    except Exception as e:
        print(e)


def game_over():
    pygame.mixer.music.load('data/music/gameover.mp3')
    pygame.mixer.music.play()
    screen.fill((0, 0, 0))
    gameover = Label('GAME OVER', 'data/fonts/font.ttf', 292, (2000, 424), (0, 0, 0), (255, 255, 255))
    speed = 10
    x = -1280
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        x += speed
        if x > 0:
            pygame.time.delay(7777)
            break
        screen.blit(gameover.image, (x, 90))
        pygame.display.flip()
        clock.tick(FPS)

    # ... score
    # ...
    terminate()


def escape():
    global playing_music
    pygame.mixer.music.pause()
    pygame.mouse.set_visible(True)

    # screen
    esc_screen = pygame.Surface([485, 300])
    esc_screen.fill((255, 204, 0))
    # title
    title = Label("  The Walkthrough", 'data/fonts/font.ttf', 60, (457, 58), (255, 204, 0), (0, 0, 0))
    esc_screen.blit(title.image, (14, 14))
    # sprite label
    label = Label("   Player", 'data/fonts/font.ttf', 42, (147, 58), (255, 204, 0), ('#241956', ))
    esc_screen.blit(label.image, (14, 86))
    # sprite image
    sprite = pygame.transform.scale(level.player.sprite.image, (level.player.sprite.rect.width * 3,
                                                                level.player.sprite.rect.height * 3))
    _, __, s_width, s_height = sprite.get_rect()
    esc_screen.blit(sprite, (14 + (161 - s_width) // 2, 136))

    # frames
    pygame.draw.rect(esc_screen, (0, 0, 0), (0, 0, 484, 299), 4)

    # resume button
    resume_button = Button(('      Resume', ), 44, ('#190773', ), (255, 255, 255),
                           (189, 86, 280, 58))  # coordinates on new surface
    # music button
    music_button = Button((' Music: turn off' if playing_music else ' Music: turn on',
                           ' Music: turn on' if playing_music else ' Music: turn off'),
                          44, ('#190773', ), (255, 255, 255),
                          (189, 158, 280, 58))  # coordinates
    # exit button
    exit_button = Button(('        Exit', ), 44, ('#190773', ), (255, 255, 255),
                         (189, 230, 280, 58))  # coordinates
    # button group
    buttons = Buttons(exit_button, resume_button, music_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(False)
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                pressed_button = buttons.check_pressed((x - 377, y - 62))
                buttons.update()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if pressed_button is not None:
                    for button in buttons.sprites():
                        button.high()
                    if 'Exit' in pressed_button.text.text:
                        terminate()
                    elif 'Resume' in pressed_button.text.text:
                        pygame.mouse.set_visible(False)
                        return
                    elif 'Music' in pressed_button.text.text:
                        music_button.text.set_image(next(music_button.texts),
                                                    music_button.text.bg_color, music_button.text.txt_color)
                        if 'turn on' in music_button.text.text:
                            playing_music = False
                        else:
                            playing_music = True
                    buttons.update()

        # drawing
        buttons.draw(esc_screen)
        screen.blit(esc_screen, (377, 62))

        pygame.display.flip()
        clock.tick(FPS)


def begin():
    pygame.mixer.music.load('data/music/intro.mp3')
    pygame.mixer.music.play(-1)
    
    intro = pygame.transform.scale(pygame.image.load('data/menu/intro.png'), (WIDTH, HEIGHT))
    
    screen.blit(intro, (0, 0))
    surface = pygame.Surface([644, 192])
    surface.fill((255, 204, 0))
    # frame
    pygame.draw.rect(screen, (10, 9, 8), (316, 114, 648, 196), 2)
    
    title = Label('The Walkthrough', 'data/fonts/font.ttf', 76, (485, 75), (255, 204, 0), (0, 0, 0))
    surface.blit(title.image, (16, 63))
    
    play_button = Button((' Play', ), 64, ('#190773', ), (255, 255, 255), (500, 10, 135, 83))
    exit_button = Button((' Exit', ), 64, ('#190773', ), (255, 255, 255), (500, 99, 135, 83))
    buttons = Buttons(play_button, exit_button)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                pressed_button = buttons.check_pressed((x - 318, y - 116))
                buttons.update()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if pressed_button is not None:
                    pygame.mixer.music.stop()
                    for button in buttons.sprites():
                        button.high()
                    if 'Play' in pressed_button.text.text:
                        return
                    elif 'Exit' in pressed_button.text.text:
                        terminate()
                    buttons.update()
        buttons.draw(surface)
        screen.blit(surface, (318, 116))
        pygame.display.flip()
        clock.tick(FPS)


def mainloop():
    global playing_music, levels, level, health_bar
    pygame.mixer.music.load('data/music/main_theme.mp3')
    pygame.mixer.music.play(-1)
    playing_music = True
    pygame.mouse.set_visible(False)

    # init levels
    levels = iter((DayLevel(), EveningLevel(), NightLevel()))
    level = change_level()
    # init player
    level.spawn_player()
    hp = 0
    # health bar
    health_bar = HealthBar()

    # main loop
    while ingame:
        # music
        if not playing_music:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        # getting pressed keys
        k_right, k_left, k_up = event_checker()
        # updating level
        level.update(k_right, k_left, k_up, level)
        # checking for carrot collision
        for carrot in level.carrots:
            if pygame.sprite.collide_rect(level.player, carrot):
                level.player.hp += 1
                carrot.remove(level)
                del level.carrots[level.carrots.index(carrot)]

        level.draw(screen)
        screen.blit(health_bar.surface, (0, 0))

        # checking for ending level
        if level.player.rect.collidepoint(level.end):
            if level.endgame:
                end()
            hp = level.player.hp
            level = change_level()
            level.spawn_player()
            level.player.hp = hp
            continue
        # checking for player hp
        if level.player.hp == 0:
            game_over()
        if hp != level.player.hp:
            health_bar.update(level.player.hp)
            hp = level.player.hp

        # updating frame
        pygame.display.flip()
        clock.tick(FPS)
    return


def end():
    pygame.mixer.music.load('data/music/end.mp3')
    pygame.mixer.music.play()
    # ... Формирование титров
    surface = pygame.Surface([1280, 1550])
    surface.fill((0, 0, 0))
    
    font = 'data/fonts/font.ttf'
    title = Label('The Walkthrough', font, 150, (1080, 150), (0, 0, 0), (255, 204, 0))
    surface.blit(title.image, (180, 636))
    
    # people
    label = Label('Над игрой работали:', font, 75, (1000, 75), (0, 0, 0), (255, 255, 128))
    surface.blit(label.image, (190, 836))
    
    # programmer
    label = Label('    Программист', font, 50, (1000, 50), (0, 0, 0), (228, 228, 228))
    surface.blit(label.image, (190, 936))
    label = Label('        Никнейм: iternal', font, 25, (1000, 25), (0, 0, 0), (255, 255, 255))
    surface.blit(label.image, (190, 1000))
    label = Label('        Контактная информация: fortun.ik@yandex.ru', font, 25, (1000, 25), (0, 0, 0),
                  (255, 255, 255))
    surface.blit(label.image, (190, 1039))
    # designer
    label = Label('    Арт-дизайнер', font, 50, (500, 50), (0, 0, 0), (228, 228, 228))
    surface.blit(label.image, (190, 1089))
    label = Label('        Никнейм: Tecka', font, 25, (1000, 25), (0, 0, 0), (255, 255, 255))
    surface.blit(label.image, (190, 1153))
    label = Label('        Контактная информация: https://vk.com/skullboxgames', font, 25, (1000, 25), (0, 0, 0),
                  (255, 255, 255))
    surface.blit(label.image, (190, 1192))
    # designer
    label = Label('    Арт-дизайнер', font, 50, (500, 50), (0, 0, 0), (228, 228, 228))
    surface.blit(label.image, (190, 1242))
    label = Label('        Никнейм: Ultralord Belobay', font, 25, (1000, 25), (0, 0, 0), (255, 255, 255))
    surface.blit(label.image, (190, 1306))
    label = Label('        Контактная информация: lketchup@list.ru', font, 25, (1000, 25), (0, 0, 0), (255, 255, 255))
    surface.blit(label.image, (190, 1345))
    # designer
    label = Label('    Арт-дизайнер', font, 50, (500, 50), (0, 0, 0), (228, 228, 228))
    surface.blit(label.image, (190, 1395))
    label = Label('        Никнейм: vovorov', font, 25, (1000, 25), (0, 0, 0), (255, 255, 255))
    surface.blit(label.image, (190, 1459))
    label = Label('        Контактная информация: mega.chistyak@mail.ru', font, 25, (1000, 25), (0, 0, 0),
                  (255, 255, 255))
    surface.blit(label.image, (190, 1498))
    
    # score
    carrots = pygame.transform.scale(health_bar.surface, tuple(map(lambda n: n * 4, health_bar.surface.get_rect()))[2:])
    exit_button = Button(('', ''), 0, (255, 204, 0), (255, 204, 0), (-10, 90, 700, 250))
    score_surface = pygame.Surface([618, 424])
    score_surface.fill((255, 204, 0))

    score_surface.blit(exit_button.image, (exit_button.rect.x, exit_button.rect.y))
    score_surface.blit(carrots, (20, 100))
    score_surface.set_alpha(0)
    screen.blit(score_surface, (331, 0))
    # ...

    pressed = False
    surface_y = 0
    surface_velocity = 0.618
    times = 0
    alpha = 0
    while alpha != 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                surface_y = -1550
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and surface_y < -1550:
                x, y = event.pos
                if exit_button.rect.collidepoint((x - 331, y)):
                    pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and surface_y < -1550:
                    if pressed:
                        terminate()
        if surface_y < -1550 and times % 5 == 0:
            pygame.mouse.set_visible(True)
            alpha += 1
            score_surface.set_alpha(alpha)

        surface_y -= surface_velocity
        times += 1
        screen.blit(score_surface, (331, 0))
        screen.blit(surface, (0, surface_y))
        pygame.display.flip()
        clock.tick(FPS)

    # leaving game
    while pygame.event.wait().type != pygame.QUIT:
        pass
    terminate()


def event_checker():
    global ingame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escape()

    keys = pygame.key.get_pressed()
    up = True if keys[pygame.K_UP] else False
    right = True if keys[pygame.K_RIGHT] else False
    left = True if keys[pygame.K_LEFT] else False
    return right, left, up


def main():
    begin()
    mainloop()
    end()
    terminate()


if __name__ == '__main__':
    main()
