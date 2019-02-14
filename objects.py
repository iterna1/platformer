from variables import *


class Level(pygame.sprite.Group):
    def __init__(self, background, start, end):
        super().__init__()
        self.background = pygame.image.load(background)
        self.start, self.end = start, end
        self.blocks, self.traps = pygame.sprite.Group(), pygame.sprite.Group()
        self.floors, self.walls = pygame.sprite.Group(), pygame.sprite.Group()

        self.add_walls([0, 0, HEIGHT - 2], [WIDTH - 2, 0, HEIGHT - 2])

    def load_lvl(self, txt):
        with open('data/levels/%s.txt' % txt, 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            if tile in ('grassblock', 'block'):
                self.add_trap('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))
            else:
                self.add_block('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))

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
        try:
            self.remove(self.player)
        except AttributeError:
            pass
        finally:
            self.player = Player(*self.start, self)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for sprite in self.sprites():
            surface.blit(sprite.image, (sprite.rect.x, sprite.rect.y))


class DayLevel(Level):
    def __init__(self):
        super().__init__('data/background/daybackground.png', (35, 300), (1248, 254))
        self.load_lvl('day')


class EveningLevel(Level):
    def __init__(self):
        super().__init__('data/background/eveningbackground.png', (30, 313), (1248, 254))
        self.load_lvl('evening')


class NightLevel(Level):
    def __init__(self):
        super().__init__('data/background/nightbackground.png', (30, 313), (1248, 254))
        self.load_lvl('night')


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
        self.rect = pygame.Rect(x - 1, y1, 2, y2 - y1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, y, x1, x2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([x2 - x1, 2])
        self.rect = pygame.Rect(x1, y - 1, x2 - x1, 2)


class Idle(pygame.sprite.Sprite):
    name = 'idle'
    right = [pygame.image.load('data/animation/idle/%s.gif' % i) for i in range(20)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 20

    def __init__(self, *groups):
        super().__init__(*groups)
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Idle.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Idle.right if right else Idle.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Run(pygame.sprite.Sprite):
    name = 'run'
    right = [pygame.image.load('data/animation/run/%s.gif' % i) for i in range(12)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 12

    def __init__(self, *groups):
        super().__init__(*groups)
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Run.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Run.right if right else Run.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Jump(pygame.sprite.Sprite):
    name = 'jump'
    right = pygame.image.load('data/animation/jump/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Bounce(pygame.sprite.Sprite):
    name = 'bounce'
    right = [pygame.image.load('data/animation/bounce/%s.gif' % i) for i in range(6)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 6

    def __init__(self, *groups):
        super().__init__(*groups)
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Run.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Bounce.right if right else Bounce.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()


class Dead(pygame.sprite.Sprite):
    name = 'dead'
    right = pygame.image.load('data/animation/dead/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Hold(pygame.sprite.Sprite):
    name = 'hold'
    right = pygame.image.load('data/animation/hold/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups=None):
        super().__init__(groups)
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.hp = 1

        self.sprites = [Idle, Run, Jump, Bounce, Dead, Hold]
        self.right = True
        self.update('idle')

    def change_facing(self):
        if self.vx > 0:
            self.right = True
        elif self.vx < 0:
            self.right = False

    def move_ip(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x, self.rect.y = self.x, self.y

    def update(self, action):
        self.change_facing()
        for sprite in self.sprites:
            if sprite.name == action:
                self.sprite = sprite()
                self.sprite.update(self.right)
                self.image = self.sprite.image
                self.rect = self.image.get_rect()

        self.move_ip()


class Button(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        self.button = pygame.Surface((width, height))
        self.button.fill(color)
        pygame.draw.rect(self.button, (100, 100, 100), (0, 0, width, height), 2)
        self.rect = self.button.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = None

    def set_font(self, file, size):
        self.size = size
        self.font = pygame.font.Font(file, size)

    def set_text(self, text, color=(255, 255, 255)):
        if self.font is not None:
            text = self.font.render(text, 1, color)
            text_x = self.button.get_width() // 2 - text.get_width() // 2
            text_y = self.button.get_height() // 2 - text.get_height() // 2
            self.button.blit(text, (text_x, text_y))

    def pressed(self, pos):
        if self.rect.collidepoint(pos):
            self.update()
            return True
        return False

    def update(self):
        pass
