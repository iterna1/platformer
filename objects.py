import pygame
from itertools import cycle

FPS = 60
ANIMATION_SPEED = FPS // 3  # lower == faster | FPS // N -> N animation cycles in 60 frames
SIZE = WIDTH, HEIGHT = 1280, 424  # screen size


class Level(pygame.sprite.Group):
    def __init__(self, background, start, end):
        super().__init__()
        self.background = pygame.image.load(background)
        self.start, self.end = start, end
        self.blocks, self.traps = pygame.sprite.Group(), pygame.sprite.Group()
        self.floors, self.walls = pygame.sprite.Group(), pygame.sprite.Group()

        self.add_walls([0, 0, HEIGHT - 2], [WIDTH - 2, 0, HEIGHT - 2])

    def add_block(self, tile, pos):
        block = Block(tile, pos, self)
        self.blocks.add(block)

        x1, y1, width, height = block.rect
        self.add_walls([x1, y1, y1 + height], [x1 + width, y1, y1 + height])
        self.add_floors([y1, x1, x1 + width], [y1 + height, x1, x1 + width])

    def add_trap(self, tile, pos):
        Trap(tile, pos, self, self.traps)

    def add_walls(self, *args):
        for xyy in args:
            Wall(*xyy, self, self.walls)  # if self in parameters, borders will be shown

    def add_floors(self, *args):
        for yxx in args:
            Floor(*yxx, self, self.floors)  # # if self in parameters, borders will be shown

    def spawn_player(self):
        self.player = Player(*self.start, self)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


class DayLevel(Level):
    def __init__(self):
        super().__init__('data/background/daybackground.png', (35, 200), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/day.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/day/%s.png' % tile, map(int, pos))


class EveningLevel(Level):
    def __init__(self):
        super().__init__('data/background/eveningbackground.png', (30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/evening.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/evening/%s.png' % tile, map(int, pos))


class NightLevel(Level):
    def __init__(self):
        super().__init__('data/background/nightbackground.png', (30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/night.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/day/%s.png' % tile, map(int, pos))


class Block(pygame.sprite.Sprite):
    def __init__(self, tile, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(tile)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Trap(Block):
    pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y1, y2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([2, y2 - y1])
        self.rect = pygame.Rect(x, y1, 2, y2 - y1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, y, x1, x2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([x2 - x1, 2])
        self.rect = pygame.Rect(x1, y, x2 - x1, 2)


class Idle(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/idle/%s.gif' % i) for i in range(20)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 20

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'idle'
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Idle.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Idle.right if right else Idle.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Run(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/run/%s.gif' % i) for i in range(12)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 12

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'run'
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Run.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Run.right if right else Run.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Jump(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/jump/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'jump'

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Bounce(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/bounce/%s.gif' % i) for i in range(6)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 6

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'bounce'
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Run.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Bounce.right if right else Bounce.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Dead(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/dead/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'dead'

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Hold(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/hold/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)
        self.name = 'hold'

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups=None):
        super().__init__(groups)
        self.vx, self.vy = 0, 0
        self.hp = 1

        self.sprites = [Idle(), Run(), Jump(), Bounce(), Dead(), Hold()]
        self.update('idle', True)
        self.rect.x, self.rect.y = x, y

    def update(self, action, right=True):
        #  Тут нужна проверка на столкновения
        self.sprite = action, right
        for sprite in self.sprites:
            if sprite.name == action:
                sprite.update(right)
                self.rect = sprite.rect.move(self.vx, self.vy)
                self.image = sprite.image

