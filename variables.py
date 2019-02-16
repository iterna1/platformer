import pygame
import sys
from itertools import cycle

FPS = 60
ANIMATION_SPEED = FPS // 2  # lower == faster | FPS // N -> N animation cycles in 60 frames
SIZE = WIDTH, HEIGHT = 1280, 424  # screen size

pygame.init()
clock = pygame.time.Clock()
ingame = True

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("The walkthrough")

intro_text = ['Инструкция такова:',
              '    Вам необходимо пройти 3 уровня.',
              '    Морковки добавляют жизни.',
              '    Шипы жизнь отнимают.',
              '    Чем больше жизней вы сохраните', '    к концу игры, тем круче', '', '', '', '', ''
              '                                                                         '
              '[Чтобы начать, нажимите кнопку ENTER]']
captions_text = ['THE END.']

begin_fon = pygame.transform.scale(pygame.image.load('data/menu/instructions.jpg'), (WIDTH, HEIGHT))
end_fon = pygame.Surface([1240, 1240])
end_fon.fill((26, 10, 16))

playing_music = False
game_music = pygame.mixer.music.load('data/music/main_theme.mp3')
volumes = cycle((100, 0))

begin_screen_font = pygame.font.Font('data/fonts/font.ttf', 30)
