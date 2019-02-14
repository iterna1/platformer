import pygame
import sys
from itertools import cycle

FPS = 60
ANIMATION_SPEED = FPS // 3  # lower == faster | FPS // N -> N animation cycles in 60 frames
SIZE = WIDTH, HEIGHT = 1280, 424  # screen size

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('game')
ingame = True

intro_text = ['Инструкция такова:',
              '    Вам необходимо пройти 3 уровня.',
              '    Морковки добавляют жизни.',
              '    Шипы жизнь отнимают.',
              '    Чем больше жизней вы сохраните', '    к концу игры, тем круче', '', '', '', '', ''
              '                                                                         '
              '[Чтобы начать, нажимите кнопку ENTER]']
begin_fon = pygame.transform.scale(pygame.image.load('data/menu/instructions.jpg'), (WIDTH, HEIGHT))
end_fon = None

escape_fon = pygame.Surface([485, 300])
escape_fon.fill((255, 204, 0))

begin_screen_font = pygame.font.Font('data/fonts/font.ttf', 30)
