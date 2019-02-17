from variables import *


class Level(pygame.sprite.Group):
    def __init__(self, background, start, end):
        super().__init__()
        self.background = pygame.image.load(background)
        self.start, self.end = start, end
        self.blocks, self.traps = [], []
        self.floors, self.walls = [], []

        self.gravity = 0.75

    def load_lvl(self, txt):
        with open('data/levels/%s.txt' % txt, 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            if tile == 'trap':
                self.add_trap('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))
            else:
                self.add_block('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))

    def add_block(self, tile, pos):
        block = Block(tile, pos, self)
        self.blocks.append(block)

    def add_trap(self, tile, pos):
        trap = Trap(tile, pos, self)
        self.traps.append(trap)

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
        super().__init__('data/background/daybackground.png', (14, 96), (1248, 254))
        self.load_lvl('day')


class EveningLevel(Level):
    def __init__(self):
        super().__init__('data/background/eveningbackground.png', (16, 152), (1248, 254))
        self.load_lvl('evening')


class NightLevel(Level):
    def __init__(self):
        super().__init__('data/background/nightbackground.png', (16, 32), (1248, 254))
        self.load_lvl('night')


class Block(pygame.sprite.Sprite):
    def __init__(self, file, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Trap(Block):
    pass


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
        self.image = Jump.right if right else Jump.left
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
        self.image = Hold.right if right else Hold.left
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups=None):
        super().__init__(groups)
        self.vx, self.vy = 0, 0
        self.hp = 1

        self.right = True
        self.onGround = False
        self.onWall = False
        self.jumpower = 10

        self.sprites = [Idle(), Run(), Jump(), Bounce(), Dead(), Hold()]
        self.sprite = self.sprites[0]
        self.sprite.update(True)
        self.image = self.sprite.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def change_facing(self):
        if self.vx > 0:
            self.right = True
        elif self.vx < 0:
            self.right = False

    def collide(self, lvl):
        for obj in lvl.blocks:
            if pygame.sprite.spritecollide(self, [obj], False):
                if self.vx > 0:
                    self.right = False
                    self.vx = 0
                    self.rect.right = obj.rect.left
                    self.onWall = True
                    self.onGround = False
                elif self.vx < 0:
                    self.right = True
                    self.vx = 0
                    self.rect.left = obj.rect.right
                    self.onWall = True
                    self.onGround = False
                if self.vy > 0:  # если падает вниз
                    self.rect.bottom = obj.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.onWall = False
                    self.vy = 0  # и энергия падения пропадает

                elif self.vy < 0:  # если движется вверх
                    self.rect.top = obj.rect.bottom  # то не движется вверх
                    self.onGround = False
                    self.vy = 0  # и энергия прыжка пропадает
                break

    def move_ip(self, lvl):
        self.rect.y += self.vy
        self.collide(lvl)
        self.rect.x += self.vx
        self.collide(lvl)

    def update(self, action, lvl):
        self.change_facing()
        if action != self.sprite.name:
            self.sprites = [Idle(), Run(), Jump(), Bounce(), Dead(), Hold()]
        for sprite in self.sprites:
            if sprite.name == action:
                self.sprite = sprite
                self.sprite.update(self.right)
                self.image = self.sprite.image
                self.rect.width, self.rect.height = self.image.get_width(), self.image.get_height()
                break
        self.move_ip(lvl)


class Label(pygame.sprite.Sprite):
    def __init__(self, text, font_file, font_size, label_rect, bg_color=(0, 0, 0), txt_color=(255, 255, 255)):
        super().__init__()
        self.text = text
        self.font_size = font_size
        self.font_file = font_file
        self.image = pygame.Surface(label_rect)
        self.rect = self.image.get_rect()
        self.txt_color = txt_color
        self.bg_color = bg_color
        self.set_image(text, bg_color, txt_color)

    def set_font(self, file, size):
        self.size = size
        self.font = pygame.font.Font(file, size)

    def set_text(self, text, color):
        text = self.font.render(text, 1, color)
        self.image.blit(text, (0, 0))

    def set_image(self, text, bg_color, txt_color):
        self.image.fill(pygame.Color(*bg_color))
        self.text = text
        self.set_font(self.font_file, self.font_size)
        self.set_text(text, pygame.Color(*txt_color))


class Buttons(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def check_pressed(self, pos):
        for sprite in self.sprites():
            result = sprite.pressed(pos)
            if result:
                sprite.deep()
                return result


class Button(pygame.sprite.Sprite):
    def __init__(self, texts, text_size, bg_color, text_color, rect):
        super().__init__()
        x, y, width, height = rect
        self.bg_color = pygame.Color(*bg_color)
        self.text_color = pygame.Color(*text_color)
        self.bg_hsva = self.bg_color.hsva
        self.txt_hsva = self.text_color.hsva

        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.texts = cycle(texts)
        self.text = Label(next(self.texts), 'data/fonts/font.ttf', text_size,
                          (width - 8, height - 8), self.bg_color, text_color)
        self.text_x, self.text_y = 4, 4  # self.rect.width // 2 - self.text.rect.width // 2, 4
        self.image.blit(self.text.image, (self.text_x, self.text_y))

    def pressed(self, pos):
        if self.rect.collidepoint(pos):
            return self
        return None

    def deep(self):
        # changing background color
        hsv = self.bg_hsva
        self.bg_color.hsva = (hsv[0], hsv[1], 0.6 * hsv[2], hsv[3])
        # changing text color
        hsv = self.txt_hsva
        self.text_color.hsva = (hsv[0], hsv[1], 0.6 * hsv[2], hsv[3])

        self.text.set_image(self.text.text, self.bg_color, self.text_color)

    def high(self):
        self.bg_color.hsva = self.bg_hsva
        self.text_color.hsva = self.txt_hsva

        self.text.set_image(self.text.text, self.bg_color, self.text_color)

    def update(self):
        self.image.fill((0, 0, 0))
        self.image.blit(self.text.image, (self.text_x, self.text_y))
