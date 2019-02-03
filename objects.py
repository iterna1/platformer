import pygame


class Level:
    def __init__(self, start, end):
        self.blocks = []
        self.floors = []
        self.walls = []
        self.traps = []
        self.start = start
        self.end = end
        self.passed = False
        self.spawn_player()

    def add_block(self, tile, pos):
        block = Block(tile, pos)
        self.blocks.append(block)

    def add_floor(self, tile, pos):
        block = Floor(tile, pos)
        self.floors.append(block)

    def add_wall(self, tile, pos):
        block = Wall(tile, pos)
        self.walls.append(block)

    def add_trap(self, tile, pos):
        block = Trap(tile, pos)
        self.traps.append(block)

    def spawn_player(self):
        self.player = Player(*self.start)

    def add_hp(self):
        self.hp += 1

    def reached_checkpoint(self):
        if (self.player.x, self.player.y) == self.end:
            self.passed = True
            return True
        return False

    def floor_collision(self, x, y):
        player = Player(x, y)
        if any([player.foot_rect().colliderect(block.rect) for block in self.floors]):
            return True
        return False

    def wall_collision(self, x, y):
        player = Player(x, y)
        if any([player.get_rect().colliderect(block.rect) for block in self.walls]):
            return True
        return False

    def trap_collision(self, x, y):
        player = Player(x, y)
        if any([player.get_rect().colliderect(block.rect) for block in self.traps]):
            return True
        return False


class DayLevel(Level):
    background = pygame.image.load('data/background/daybackground.png')

    def __init__(self):
        super().__init__((35, 200), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/day.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, x, y = block.split(';')
            pos = (int(x) * 2, int(y) * 2)
            self.add_block('data/tiles/day/%s.png' % tile, pos)
            if tile in ('platform', 'grassblock'):
                self.add_floor('data/tiles/day/%s.png' % tile, pos)
            elif tile == 'block':
                self.add_wall('data/tiles/day/%s.png' % tile, pos)
            elif tile == 'thorn':
                self.add_trap('data/tiles/day/%s.png' % tile, pos)


class EveningLevel(Level):
    background = pygame.image.load('data/background/eveningbackground.png')

    def __init__(self):
        super().__init__((30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/evening.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, x, y = block.split(';')
            pos = (int(x) * 2, int(y) * 2)
            self.add_block('data/tiles/evening/%s.png' % tile, pos)
            if tile in ('platform', 'grassblock'):
                self.add_floor('data/tiles/evening/%s.png' % tile, pos)
            elif tile == 'block':
                self.add_wall('data/tiles/evening/%s.png' % tile, pos)
            elif tile == 'thorn':
                self.add_trap('data/tiles/evening/%s.png' % tile, pos)


class NightLevel(Level):
    background = pygame.image.load('data/background/nightbackground.png')

    def __init__(self):
        super().__init__((30, 313), (1248, 254))
        self.load_lvl()

    def load_lvl(self):
        with open('data/levels/night.txt', 'r') as file:
            self.map = map(lambda line: line.rstrip(), file.readlines())

        for block in self.map:
            tile, x, y = block.split(';')
            pos = (int(x) * 2, int(y) * 2)
            self.add_block('data/tiles/night/%s.png' % tile, pos)
            if tile in ('platform', 'grassblock'):
                self.add_floor('data/tiles/night/%s.png' % tile, pos)
            elif tile == 'block':
                self.add_wall('data/tiles/night/%s.png' % tile, pos)
            elif tile == 'thorn':
                self.add_trap('data/tiles/night/%s.png' % tile, pos)


class Block:
    def __init__(self, tile, pos):
        self.image = pygame.image.load(tile)
        self.pos = pos
        x, y, width, height = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (width * 2, height * 2))
        self.rect = pygame.Rect(*self.pos, width * 2, height * 2)


class Wall(Block):
    pass


class Floor(Block):
    pass


class Trap(Block):
    pass


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
    deadfall_r = [pygame.image.load('data/animation/deadfall_r/0.png')]
    deadfall_l = [pygame.image.load('data/animation/deadfall_l/0.png')]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 0
        self.last_action = None
        self.change_action('idle_r')
        self.hp = 1

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
        elif action == 'deadfall_r':
            self.action = Player.deadfall_r
        elif action == 'deadfall_l':
            self.action = Player.deadfall_l

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

    def foot_rect(self):
        _, __, width, height = self.action[self.count].get_rect()
        return pygame.Rect(self.x, self.y + height - 1, width * 2, 2)

    def get_rect(self):
        _, __, width, height = self.action[self.count].get_rect()
        return pygame.Rect(self.x, self.y, width * 2, height * 2)

    def update(self):
        return self.action[self.count]
