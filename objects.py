import pygame

FPS = 60


class Level(pygame.sprite.Group):
    def __init__(self, start, end):
        super().__init__()
        self.start, self.end = start, end
        self.blocks, self.traps = set(), set()
        self.floors = {Floor(0, 0, 1240, self), Floor(424, 0, 1240, self)}
        self.walls = {Wall(0, 0, 424, self), Wall(1240, 0, 424, self)}

    def add_block(self, tile, pos):
        block = Block(tile, pos, self)
        self.blocks.add(block)

        x1, y1, width, height = block.rect
        self.add_wall(x1, y1, y1 + height)
        self.add_wall(x1 + width, y1, y1 + height)
        self.add_floor(y1, x1, x1 + width)
        self.add_floor(y1 + height, x1, x1 + width)

    def add_trap(self, tile, pos):
        block = Trap(tile, pos, self)
        self.traps.add(block)

    def add_wall(self, x, y1, y2):
        wall = Wall(x, y1, y2, self)
        self.walls.add(wall)

    def add_floor(self, y, x1, x2):
        floor = Floor(y, x1, x2, self)
        self.floors.add(floor)

    def spawn_player(self):
        self.player = Player(*self.start)


class DayLevel(Level):
    background = pygame.image.load('data/background/daybackground.png')

    def __init__(self):
        super().__init__((35, 200), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/day.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/day/%s.png' % tile, pos)


class EveningLevel(Level):
    background = pygame.image.load('data/background/eveningbackground.png')

    def __init__(self):
        super().__init__((30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/evening.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/day/%s.png' % tile, pos)


class NightLevel(Level):
    background = pygame.image.load('data/background/nightbackground.png')

    def __init__(self):
        super().__init__((30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/night.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            self.add_block('data/tiles/day/%s.png' % tile, pos)


class Block(pygame.sprite.Sprite):
    def __init__(self, tile, pos, group=None):
        super().__init__(group)
        self.image = pygame.transform.scale2x(pygame.image.load(tile))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Trap(Block):
    pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y1, y2, group=None):
        super().__init__(group)
        self.image = pygame.Surface([2, y2 - y1])
        self.rect = pygame.Rect(x, y1, 2, y2 - y1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, y, x1, x2, group=None):
        super().__init__(group)
        self.image = pygame.Surface([x2 - x1, 2])
        self.rect = pygame.Rect(x1, y, x2 - x1, 2)


class Idle(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/idle/%s.gif' % i) for i in range(20)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 20

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'idle'
        self.images = Idle.right if right else Idle.left
        self.animcount = 0

    def update(self, x, y):
        self.image = self.images[self.animcount // (FPS // Idle.length)]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.animcount += 1 if self.animcount < FPS else -self.animcount


class Run(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/run/%s.gif' % i) for i in range(12)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 12

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'run'
        self.images = Run.right if right else Run.left
        self.animcount = 0

    def update(self, x, y):
        self.image = self.images[self.animcount // (FPS // Run.length)]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.animcount += 1 if self.animcount < FPS else -self.animcount


class Jump(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/jump/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'jump'
        self.image = Jump.right if right else Jump.left
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y


class Bounce(pygame.sprite.Sprite):
    right = [pygame.image.load('data/animation/bounce/%s.gif' % i) for i in range(6)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 6

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'bounce'
        self.images = Bounce.right if right else Bounce.left
        self.animcount = 0

    def update(self, x, y):
        self.image = self.images[self.animcount // (FPS // Bounce.length)]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.animcount += 1 if self.animcount < FPS else -self.animcount


class Dead(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/dead/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'dead'
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y


class Hold(pygame.sprite.Sprite):
    right = pygame.image.load('data/animation/hold/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, right=True, group=Player):
        super().__init__(group)
        self.name = 'hold'
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y


class Player(pygame.sprite.Group):
    def __init__(self, x, y):
        super().__init__()
        self.vx, self.vy = 5, 0
        self.hp = 1

        self.add(Idle, Run, Jump, Bounce, Dead, Hold)
        self.sprite = None
        self.update(x, y, 'idle', True)

    def update(self, x, y, action, right=True):
        #  Тут нужна проверка на столкновения
        for sprite in self.sprites():
            if sprite.name == action:
                sprite.update(x, y, right)
                self.sprite = sprite
                return sprite
