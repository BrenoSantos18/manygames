import pygame
from random import randint
import time
from settings import *

#create a game about a car driving and avoiding other cars


other_cars = {}
clock = pygame.time.Clock()
street_surf = pygame.Surface((500, 700))
street_surf.fill('black')
street_rect = street_surf.get_rect(topleft = (width/2-250,0))

car_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
street_group = pygame.sprite.Group()

class Car(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Assets/drivegame/car.png')
        self.rect = self.image.get_rect(topleft = (width/2 - 5,height/2 - 5))
        self.speed = 2

    def update(self, game):
        self.input()
        self.collision(game)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= 1
        if keys[pygame.K_s] and self.rect.y < 550:
            self.rect.y += 1
        if keys[pygame.K_a] and self.rect.x > width/2-255:
            self.rect.x -= 1
        if keys[pygame.K_d] and self.rect.x < (width/2+135):
            self.rect.x += 1

        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= 1
        if keys[pygame.K_DOWN] and self.rect.y < 550:
            self.rect.y += 1
        if keys[pygame.K_LEFT] and self.rect.x > width/2-255:
            self.rect.x -= 1
        if keys[pygame.K_RIGHT] and self.rect.x < (width/2+135):
            self.rect.x += 1

    def collision(self,game):
        for sprites in obstacle_group:
            if sprites.rect.colliderect(self.rect):
                game.running = False




class Enemies(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('Assets/drivegame/car_npc.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = randint(200, 600)

    def update(self, dt):
        pos = round(self.speed * dt)
        self.rect.y += 1 * pos

        if self.rect.top > 1000:
            self.kill()







class DriveGame:
    def __init__(self):
        self.player = Car(car_group)
        self.font = pygame.font.SysFont(None, 30)
        self.bigger_font = pygame.font.SysFont(None, 120)


        self.line_surf = pygame.image.load('Assets/drivegame/line.png')
        self.line_scale = pygame.transform.scale(self.line_surf, (500,150))
        self.line_rect = self.line_scale.get_rect(topleft = (width/2-246, -150))

        self.create_time = 0
        self.creation_cooldown = 3000
        self.can_creat = True
        self.click = False
        self.rerun = False

        #GAME STATES
        self.in_game = True

        self.paused = False
        self.running = True
        self.win = False


        self.run_time = 20000
        self.init_run = 0
        self.can_init = True
        self.main_rect_y = -150


    def check_state(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.init_run > self.run_time and self.running:
            self.win = True


    def generate(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.create_time >= self.creation_cooldown:
            self.can_creat = True




    def run(self, dt, game):

        if self.in_game:
            if self.can_init:
                self.running = True
                self.can_init = False
                self.init_run = pygame.time.get_ticks()

            mx, my = pygame.mouse.get_pos()
            self.check_state()

            #DRAW EVERYTHING
            self.draw_map()
            car_group.draw(screen)
            obstacle_group.draw(screen)
            self.generate()



            #CHECK STATE OF THE GAME

            if self.rerun:
                for sprites in obstacle_group:
                    sprites.kill()
                self.rerun = False

                self.line_rect.y = -150
                self.player.rect.y = height/2 - 5

                self.win = False
                self.running = True
                self.init_run = pygame.time.get_ticks()


            #THE CAR DONT STAND STILL WHEN YOU WIN
            if self.win and self.running:
                self.line_rect.y += 2

            #CHECK IF YOU WIN
            for sprites in car_group:
                if sprites.rect.colliderect(self.line_rect):
                    self.running = False

            if self.running:
                car_group.update(self)
                obstacle_group.update(dt)



            #CAR CREATION
            if self.can_creat and self.running:
                self.can_creat = False
                self.create_time = pygame.time.get_ticks()
                random_x = randint((width/2)-235, (width/2)+150)
                obstacle_car = Enemies((random_x, -150), obstacle_group)


            #CHECK STATE OF THE GAME
            if self.win == True and self.running == False:
                win = self.bigger_font.render(f'You Won!', True, 'yellow')
                win_rect = win.get_rect(topleft = (50,10))
                screen.blit(win, win_rect)
                self.player.rect.y -= 2
                for sprites in obstacle_group.sprites():
                    sprites.rect.y += 1

            if self.running == False and self.win == False:
                failed = self.bigger_font.render(f'You failed!', True, 'yellow')
                failed_rect = failed.get_rect(topleft = (50,10))
                screen.blit(failed, failed_rect)

            if not self.running:
                rerun = pygame.image.load('Assets/drivegame/rerun.png')
                rerun_rect = rerun.get_rect(topleft = (width/2 - 10 - 200, height/2-52))
                screen.blit(rerun, rerun_rect)

                back = pygame.image.load('Assets/drivegame/quit.png')
                back_rect = back.get_rect(topleft = (width/2 + 10, height/2-52))
                screen.blit(back, back_rect)


                if rerun_rect.collidepoint((mx,my)) and game.click == True:
                    self.rerun = True

                if back_rect.collidepoint((mx,my)) and game.click == True:
                    self.in_game = False
                    game.running_game = False
                    game.in_menu = True

                    self.can_init = True
                    self.win = False












    def draw_map(self):
        screen.fill('green')

        #DRAW THE MAIN STREET
        street_surf = pygame.Surface((500, 700))
        street_surf.fill('black')
        street_rect = street_surf.get_rect(topleft = (width/2-250,0))
        screen.blit(street_surf,street_rect)

        #DRAW THE WALKS (APPARENCE PURPOSES)
        walk_left = pygame.Rect(width/2+250, 0, 60, 700)
        walk_right = pygame.Rect(width/2-300, 0, 60, 700)
        pygame.draw.rect(screen, 'grey', walk_left)
        pygame.draw.rect(screen, 'grey', walk_right)


        #DRAW THE WIN LINE
        screen.blit(self.line_scale, self.line_rect)





