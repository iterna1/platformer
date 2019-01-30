import pygame


class Player:
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

        self.anim_count = 0
        self.divider = len(self.action)

    def get_rect(self):
        return self.action[self.anim_count].get_rect()

    def update(self):
        return self.action[self.anim_count // self.divider]

