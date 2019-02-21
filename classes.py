from variables import *


class Level(pygame.sprite.Group):
    def __init__(self, background, start, end, finishing=False):
        super().__init__()
        self.background = pygame.image.load(background)
        self.start, self.end = start, end
        self.blocks, self.traps = [], []
        self.walls, self.floors = [], []
        self.floors, self.walls = [], []
        self.carrots = []
        # level borders
        self.border_l = Wall(0, 0, HEIGHT)
        self.border_r = Wall(WIDTH, 0, HEIGHT)
        self.border_t = Floor(0, 0, WIDTH)
        self.border_b = Floor(HEIGHT, 0, WIDTH)
        # game finishing level
        self.endgame = end if finishing else False

    def load_lvl(self, txt):
        with open('data/levels/%s.txt' % txt, 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, *pos = block.split(';')
            if tile == 'thorn':
                self.add_trap('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))
            elif tile == 'carrot':
                self.add_carrot('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))
            else:
                self.add_block('data/tiles/%s/%s.png' % (txt, tile), map(int, pos))

    def add_block(self, tile, pos):
        block = Block(tile, pos, self)
        self.blocks.append(block)

    def add_trap(self, tile, pos):
        trap = Trap(tile, pos, self)
        self.traps.append(trap)

    def add_carrot(self, tile, pos):
        carrot = Carrot(tile, pos, self)
        self.carrots.append(carrot)

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
        super().__init__('data/background/daybackground.png', (8, 96), (1248, 160))
        self.load_lvl('day')


class EveningLevel(Level):
    def __init__(self):
        super().__init__('data/background/eveningbackground.png', (16, 152), (1248, 184))
        self.load_lvl('evening')


class NightLevel(Level):
    def __init__(self):
        super().__init__('data/background/nightbackground.png', (16, 32), (1248, 220), True)
        self.load_lvl('night')
        self.endgame = (1248, 220)


class Block(pygame.sprite.Sprite):
    def __init__(self, file, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Trap(Block):
    pass


class Carrot(Block):
    pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y1, y2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([1, y2 - y1])
        self.rect = pygame.Rect(x, y1, 1, y2 - y1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, y, x1, x2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([x2 - x1, 1])
        self.rect = pygame.Rect(x1, y, x2 - x1, 1)


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

    def set_default(self):
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Idle.length)) for f in range(ANIMATION_SPEED)])


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

    def set_default(self):
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Run.length)) for f in range(ANIMATION_SPEED)])


class Jump(pygame.sprite.Sprite):
    name = 'jump'
    right = pygame.image.load('data/animation/jump/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Jump.right if right else Jump.left
        self.rect = self.image.get_rect()

    def set_default(self):
        pass


class Bounce(pygame.sprite.Sprite):
    name = 'bounce'
    right = [pygame.image.load('data/animation/bounce/%s.gif' % i) for i in range(6)]
    left = [pygame.transform.flip(im, True, False) for im in right]
    length = 6

    def __init__(self, *groups):
        super().__init__(*groups)
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Bounce.length)) for f in range(ANIMATION_SPEED)])

    def update(self, right=True):
        self.images = Bounce.right if right else Bounce.left
        self.image = self.images[next(self.animcount)]
        self.rect = self.image.get_rect()

    def set_default(self):
        self.animcount = cycle([int(f / (ANIMATION_SPEED / Bounce.length)) for f in range(ANIMATION_SPEED)])


class Dead(pygame.sprite.Sprite):
    name = 'dead'
    right = pygame.image.load('data/animation/dead/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Dead.right if right else Dead.left
        self.rect = self.image.get_rect()

    def set_default(self):
        pass


class Hold(pygame.sprite.Sprite):
    name = 'hold'
    right = pygame.image.load('data/animation/hold/0.png')
    left = pygame.transform.flip(right, True, False)

    def __init__(self, *groups):
        super().__init__(*groups)

    def update(self, right=True):
        self.image = Hold.right if right else Hold.left
        self.rect = self.image.get_rect()

    def set_default(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups=None):
        super().__init__(groups)
        self.vx, self.vy = 0, 0
        self.hp = 1

        self.right = True  # facing
        self.onGround = False
        self.onWall = False
        self.jumpower = 8

        self.sprites = [Idle(), Run(), Jump(), Bounce(), Dead(), Hold()]
        self.sprite = self.sprites[0]
        self.sprite.update(True)
        self.image = self.sprite.image
        self.rect = self.image.get_rect()  # rect is fixed statement (it needs is correctly check collisions)
        self.rect.x, self.rect.y = x, y

        self.head_rect = self.image.get_rect()  # head rect needs to check wall collisions
        self.head_rect.height = self.rect.height // 3

    def update(self, right, left, up, lvl):
        if self.onWall:
            self.vx = 0
            self.vy = 0
            if up:
                self.right = not self.right
                self.set_sprite('jump')
                self.onWall = False

                self.vy = -self.jumpower
                if self.right:
                    self.vx = 4
                else:
                    self.vx = -4
        else:
            if up:
                if self.onGround:  # jumping only when on floor
                    self.vy = -self.jumpower
                    self.set_sprite('jump')

            if left:
                self.vx = -4
                self.right = False
                if up:
                    self.set_sprite('jump')
                elif self.onGround:
                    self.set_sprite('run')

            if right:
                self.vx = 4
                self.right = True
                if up:
                    self.set_sprite('jump')
                elif self.onGround:
                    self.set_sprite('run')

            elif not (right or left):  # idle when not any(right, left)
                self.vx = 0
                if up:
                    self.set_sprite('jump')
                elif not up and self.onGround:
                    self.set_sprite('idle')

            if not self.onGround:
                self.vy += GRAVITY

        self.onGround = False

        self.rect.y += self.vy
        self.head_rect.y = self.rect.y + 8
        collision_y = self.collide(0, self.vy, lvl)

        self.rect.x += self.vx
        self.head_rect.x = self.rect.x
        collision_x = self.collide(self.vx, 0, lvl)
        
    def collide(self, vx, vy, lvl):
        platforms = lvl.blocks
        traps = lvl.traps
        border_l = lvl.border_l
        border_r = lvl.border_r
        border_t = lvl.border_t
        border_b = lvl.border_b

        # checking for trap collision
        for trap in traps:
            if pygame.sprite.collide_mask(self, trap):
                self.set_sprite('dead')
                lvl.spawn_player()
                lvl.player.hp = self.hp - 1
                return

        # checking for block collision
        collision = False
        for block in platforms:
            if pygame.sprite.collide_rect(self, block):  # if collision between player and block
                collision = True
                if vx > 0:                       # if moving right
                    if self.head_rect.colliderect(block.rect):
                        self.onWall = True
                        self.set_sprite('hold')
                    self.rect.right = block.rect.left  # stop

                if vx < 0:                       # if moving left
                    if self.head_rect.colliderect(block.rect):
                        self.onWall = True
                        self.set_sprite('hold')
                    self.rect.left = block.rect.right  # stop

                if vy > 0:                       # if falling down
                    self.rect.bottom = block.rect.top  # then standing on floor
                    self.onGround = True
                    self.vy = 0

                if vy < 0:                       # if moving up
                    self.rect.top = block.rect.bottom  # then stop
                    self.vy = 0

        # checking for level borders collision
        if self.rect.colliderect(border_l):
            self.rect.left = border_l.rect.right
        if self.rect.colliderect(border_t):
            self.rect.top = border_t.rect.bottom
            self.vy = 0
        if self.rect.colliderect(border_b):
            self.set_sprite('dead')
            lvl.spawn_player()
            lvl.player.hp = self.hp - 1
            return
        if self.rect.colliderect(border_r):
            self.rect.right = border_r.rect.left

        return collision

    def set_sprite(self, action):
        if action != self.sprite.name:
            self.sprite.set_default()
        for sprite in self.sprites:
            if sprite.name == action:
                self.sprite = sprite
                self.sprite.update(self.right)
                self.image = self.sprite.image
                break


class HealthBar:
    filled_carrot = (pygame.image.load('data/tiles/day/carrot.png'), True)
    unfilled_carrot = (pygame.image.load('data/tiles/grey_carrot.png'), False)
    
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface([148, 48])
        self.surface.fill((255, 204, 0))
        self.hp = 0
        self.carrots = [HealthBar.unfilled_carrot, HealthBar.unfilled_carrot,
                        HealthBar.unfilled_carrot, HealthBar.unfilled_carrot]
    
    def update(self, hp):
        self.hp = hp
        for i in range(len(self.carrots)):
            if i >= hp:
                self.carrots[i] = HealthBar.unfilled_carrot
        if not self.carrots[hp - 1][1]:
            self.carrots[hp - 1] = HealthBar.filled_carrot
            
        for i in range(len(self.carrots)):
            self.surface.blit(self.carrots[i][0], (8 + i * 32, 8))       


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
