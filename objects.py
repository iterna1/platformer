import pygame


class Level:
    def __init__(self):
        self.blocks = set()

    def add_block(self, tile, pos):
        self.blocks.add(Block(tile, pos))


class DayLevel(Level):
    background = pygame.image.load('data/background/daybackground.png')
    platform = pygame.image.load('data/tiles/day/platform.png')
    block = pygame.image.load('data/tiles/day/block.png')
    grassblock = pygame.image.load('data/tiles/day/grassblock.png')

    def __init__(self):
        super().__init__()
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/day.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, x, y = block.split(';')
            pos = (int(x) * 2, int(y) * 2)
            self.add_block('data/tiles/day/%s.png' % tile, pos)


class Block:
    def __init__(self, tile, pos):
        self.image = pygame.image.load(tile)
        self.image = pygame.transform.scale(self.image, tuple(map(lambda i: i * 2, self.image.get_rect()[2:4])))
        self.pos = pos
        self.size = self.get_rect()

    def get_rect(self):
        return self.pos, self.image.get_rect()


class Player:
    fps = 30
    idle_r = [pygame.image.load('data/animation/idle_r/%s.gif' % i) for i in range(20)]
    idle_l = [pygame.image.load('data/animation/idle_l/%s.gif' % i) for i in range(20)]
    run_r = [pygame.image.load('data/animation/run_r/%s.gif' % i) for i in range(12)]
    run_l = [pygame.image.load('data/animation/run_l/%s.gif' % i) for i in range(12)]
    jump_r = [pygame.image.load('data/animation/jump_r/0.png')]
    jump_l = [pygame.image.load('data/animation/jump_l/0.png')]
    climbhold_r = [pygame.image.load('data/animation/climbhold_r/0.png')]
    climbhold_l = [pygame.image.load('data/animation/climbhold_l/0.png')]
    climbjump_r = [pygame.image.load('data/animation/climbjump_r/%s.gif' % i) for i in range(6)]
    climbjump_l = [pygame.image.load('data/animation/climbjump_l/%s.gif' % i) for i in range(6)]
    climbslide_r = [pygame.image.load('data/animation/climbslide_r/0.png')]
    climbslide_l = [pygame.image.load('data/animation/climbslide_l/0.png')]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_action = None
        self.change_action('idle_r')

    def change_action(self, action):
        if action == 'idle_r':
            self.action = Player.idle_r
        elif action == 'idle_l':
            self.action = Player.idle_l
        elif action == 'run_r':
            self.action = Player.run_r
        elif action == 'run_l':
            self.action = Player.run_l
        elif action == 'jump_r':
            self.action = Player.jump_r
        elif action == 'jump_l':
            self.action = Player.jump_l
        elif action == 'climbhold_r':
            self.action = Player.climbhold_r
        elif action == 'climbhold_l':
            self.action = Player.climbhold_l
        elif action == 'climbjump_r':
            self.action = Player.climbjump_r
        elif action == 'climbjump_l':
            self.action = Player.climbjump_l
        elif action == 'climbslide_r':
            self.action = Player.climbslide_r
        elif action == 'climbslide_l':
            self.action = Player.climbslide_l

        if action != self.last_action:
            self.anim_count = 0
            self.divider = round(Player.fps / len(self.action))
            self.count = 0
        else:
            if (self.anim_count // self.divider) + 1 == len(self.action):
                self.anim_count = 0
                self.count = 0
            else:
                self.anim_count += 1
                self.count = self.anim_count // self.divider
        self.last_action = action

    def get_rect(self):
        return self.action[self.count].get_rect()

    def update(self):
        return self.action[self.count]

