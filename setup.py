import pygame
from settings import *

class Setup_Player(pygame.sprite.Sprite):
    def __init__(self, groups, game):
        super().__init__(groups)
        self.status = 'down'
        self.game = game
        self.direction = pygame.math.Vector2()
        self.speed = 180

        self.interact = False
        self.cooldown = 500
        self.time_interact = 0



    def collision(self, direction):
        if direction == 'horizontal':
            for sprites in obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.rect.x > sprites.rect.x:
                        self.rect.left = sprites.rect.right
                    if self.rect.x < sprites.rect.x:
                        self.rect.right = sprites.rect.left


        if direction == 'vertical':
            for sprites in obstacle_sprites:
                if sprites.rect.colliderect(self.rect):
                    if self.rect.y > sprites.rect.y:
                        self.rect.top = sprites.rect.bottom
                    if self.rect.y < sprites.rect.y:
                        self.rect.bottom = sprites.rect.top





    def interact_cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.time_interact >= self.cooldown:
            self.interact = False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.y > 0:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s] and self.rect.y < height - self.rect.height:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_a] and self.rect.x > 0:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d] and self.rect.x < width - self.rect.width:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_e] and not self.interact:
            self.interact = True
            self.time_interact = pygame.time.get_ticks()

    def move(self, dt):
        pos = round(dt * self.speed)

        if self.direction.magnitude() != 0:
            self.direction.normalize()

        self.rect.y += self.direction.y * pos
        self.collision('vertical')
        self.rect.x += self.direction.x * pos
        self.collision('horizontal')

        #print(f'Direction: {self.direction.x}x  {self.direction.y}y')
        #print(f'DT: {dt}')
        #print(f'Round: {pos}')

