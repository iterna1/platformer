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


def escape():
    global playing_music
    pygame.mixer.music.pause()
    pygame.mouse.set_visible(True)

    # screen
    esc_screen = pygame.Surface([485, 300])
    esc_screen.fill((255, 204, 0))
    # title
    title = Label("  The walkthrough", 'data/fonts/font.ttf', 60, (457, 58), (255, 204, 0), (0, 0, 0))
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
                           (189, 86, 280, 58))  # coordinates
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
        clock.tick(FPS)


def mainloop():
    global playing_music
    pygame.mixer.music.play(-1)
    playing_music = True
    pygame.mouse.set_visible(False)

    # main loop
    while ingame:
        if not playing_music:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        # updating level
        action = movements(*event_checker())
        level.update(action)
        level.draw(screen)
        # updating frame
        pygame.display.flip()
        clock.tick(FPS)
    return


def end():
    pass


def movements(k_right, k_left, k_space):
    action = level.player.sprite.name

    return action


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


def main():
    global levels, level
    levels = iter((DayLevel(), NightLevel(), EveningLevel()))
    level = change_level()
    level.spawn_player()

    begin()
    mainloop()
    end()
    terminate()


if __name__ == '__main__':
    main()
