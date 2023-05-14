import pygame
from settings import *
from setup import Setup_Player
from random import randint

class Player(Setup_Player):
    def __init__(self, groups, game = 'gasgame'):
        super().__init__(groups, game)
        self.amount_of_gas = 100
        self.max_amount = 200
        self.fill_per_sec = 1

        self.point = 0
        self.money = 0

        self.status = 'down_idle'
        self.frame_index = 0
        self.import_graphics()
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = (150,200))

    def update(self, dt):
        self.get_target_pos()
        self.interact_cooldown()
        self.input()
        self.move(dt)
        self.get_status()
        self.animate(dt)
        self.ui()


    #ANIMATION
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

    def import_graphics(self):
        self.animations = {'left_idle': [], 'right_idle': [], 'down_idle': [],'up_idle': [],
                           'left': [], 'right': [], 'down': [], 'up': []
                           }

        for animation in self.animations.keys():
            full_path = 'Assets/gasgame/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]


    #HANDLE GAME
    def get_target_pos(self):
        self.target_pos = self.rect.center + gas_game['interact_range'][self.status.split("_")[0]]

    def player_money(self, sprites):
        total = round((sprites.numb_random * 40)/100)

        self.money += total


    def ui(self):
        bg = pygame.Rect(10,10, 40, 200)
        border = bg.copy()

        ratio = self.amount_of_gas / self.max_amount
        current_height = bg.height * ratio
        current_surf = pygame.Surface((40, current_height))
        current_surf.fill('red')
        current_rect = current_surf.get_rect(midbottom = (30,210))

        pygame.draw.rect(screen, 'grey', bg)
        screen.blit(current_surf, current_rect)
        pygame.draw.rect(screen, 'black', border, 5)

        font = pygame.font.SysFont(None, 40)
        points = font.render(f"Attended Cars: {self.point}", True, 'Blue')
        points_rect = points.get_rect(topleft = (width-250,10))
        screen.blit(points, points_rect)
        money = font.render(f"Money: ${self.money}", True, 'Blue')
        money_rect = money.get_rect(topleft = (width-250,60))
        screen.blit(money, money_rect)









class Car(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        #SPRITE
        self.import_assets()
        self.rect = self.image.get_rect(topleft = (-150, 500))

        #VARIABLES - BOOLEAN
        self.can_drive = True
        self.filling = False
        self.was_attended = False


        #VARIABLE - INT
        self.max_amount = 100
        self.numb_random = randint(20, 60)
        self.current_amount = self.numb_random

        #HANDLE TIMES
        self.max_wait = 10000
        self.arrive_time = 0
        self.fill_time = 0
        self.cooldown = 100

    def update(self):
        if not self.filling:
            self.fill_time = 0

        if self.rect.x > 1200:
            if self.current_amount >= self.max_amount:
                self.was_attended = True
            if not self.was_attended:
                for sprites in player_sprite.sprites():
                    sprites.money -= round((self.numb_random * 10)/100)
            self.kill()

        if self.rect.x == 500:
            self.can_drive = False


        for sprites in player_sprite.sprites():
            if self.rect.collidepoint(sprites.target_pos):
                if self.current_amount < self.max_amount:
                    self.show_gasoline()
                if sprites.interact:
                    self.filling = True
                else:
                    self.filling = False

        if self.current_amount >= self.max_amount:
            self.filling = False
            self.can_drive = True

        self.put_gas()

        self.wait_time()

        if self.can_drive:
            self.rect.x += 1


    #CHOOSE WHAT CAR SPRITE IT WILL BE
    def import_assets(self):
        random = randint(1,2)
        self.image = pygame.image.load(f'Assets/gasgame/car{random}.png')


    def show_gasoline(self):
        ratio = self.current_amount / self.max_amount
        bg = pygame.Rect( self.rect.x + self.rect.width/2 - 25, self.rect.y  + self.rect.height/2 - 2, 50, 5)

        current_width = bg.width * ratio
        current_rect = bg.copy()
        current_rect.width = current_width

        pygame.draw.rect(screen, 'black', bg)
        pygame.draw.rect(screen, 'red', current_rect)




    #TELL HOW MUCH TIME THE NPC WILL WAIT FOR YOU
    def wait_time(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.arrive_time > self.max_wait and not self.filling:
            self.can_drive = True

    def put_gas(self):
        current_time = pygame.time.get_ticks()

        for sprites in player_sprite.sprites():
            if sprites.direction.magnitude() != 0:
                self.filling = False
            if self.filling:
                if sprites.amount_of_gas > sprites.fill_per_sec:
                    if current_time - self.fill_time > self.cooldown:
                        self.fill_time = pygame.time.get_ticks()
                        self.current_amount += sprites.fill_per_sec
                        sprites.amount_of_gas -= sprites.fill_per_sec

                        if self.current_amount == self.max_amount:
                            self.was_attended = True







class Gastank(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_type):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.image.load('Assets/gasgame/gastank.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (400, 200))

        self.filling = False

        self.fill_time = 0
        self.cooldown = 100
        self.max_amount = 100
        self.current = 100

    def update(self):
        if not self.filling:
            self.fill_time = 0

            for sprites in player_sprite.sprites():
                if not sprites.interact:
                    if self.current < self.max_amount:
                        self.current += 1


        for sprites in player_sprite.sprites():
            if self.rect.collidepoint(sprites.target_pos):
                if sprites.interact:
                    self.filling = True
                else:
                    self.filling = False

        if not self.current > 0:
            self.filling = False

        self.getting_gas()
        self.update_image()
        for sprites in player_sprite.sprites():
            if self.rect.collidepoint(sprites.target_pos):
                block = pygame.Rect(self.rect.x + self.rect.width/2 -5,self.rect.y + self.rect.height/2 - 5,10,10)
                pygame.draw.rect(screen, 'black', block)



    def getting_gas(self):
        current_time = pygame.time.get_ticks()

        for sprites in player_sprite.sprites():
            if sprites.direction.magnitude() != 0:
                self.filling = False

            if self.filling:
                if current_time - self.fill_time > self.cooldown:
                    if sprites.amount_of_gas < sprites.max_amount:
                        self.fill_time = pygame.time.get_ticks()
                        self.current -= 1
                        sprites.amount_of_gas += 1

    def update_image(self):
        h = self.rect.height - 20
        w = self.rect.width - 4
        x = self.rect.x + 2
        y = self.rect.y + 20


        bg = pygame.Rect(x, y, w, h)

        ratio = self.current / self.max_amount
        current_height = h * ratio

        current_surf = pygame.Surface((w, current_height))
        current_surf.fill('red')
        current_rect = current_surf.get_rect(midbottom = (x + w/2,y + h))

        pygame.draw.rect(screen, 'grey', bg)
        screen.blit(current_surf, current_rect)
        interactive_sprites.draw(screen)






class GasGame:
    def __init__(self):
        self.player = Player(player_sprite)
        self.gas = Gastank([interactive_sprites, obstacle_sprites], 'interactive')

        self.car_creation_cooldown = 1200
        self.can_creat = False
        self.get_cooldown = 0
        self.in_shop = False


    def car_creation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.get_cooldown >= self.car_creation_cooldown:
            self.can_creat = True


    def game_run(self, dt, game):
        self.draw_map()

        player_sprite.draw(screen)

        if len(car_sprite.sprites()) == 0:
            self.car = Car([car_sprite, obstacle_sprites])
            self.car.arrive_time = pygame.time.get_ticks()

        car_sprite.draw(screen)
        interactive_sprites.draw(screen)
        player_sprite.update(dt)
        interactive_sprites.update()
        car_sprite.update()

        for sprites in car_sprite.sprites():
            if sprites.was_attended:
                for sprite in player_sprite.sprites():
                    sprites.was_attended = False
                    sprite.point += 1
                    sprite.player_money(sprites)


        if self.in_shop:
            self.buy_menu(game)

    def draw_map(self):
        screen.fill('green')
        street = pygame.Rect(0, (height * 70)/100, width, (height * 30)/100)
        pygame.draw.rect(screen, 'black', street)
        walk = pygame.Rect(0, (height * 70)/100 - 100, width, 100)
        pygame.draw.rect(screen, 'white', walk)
        gas_floor = pygame.Rect(250,20, 500,350)
        pygame.draw.rect(screen, 'grey', gas_floor)

        gas_station = pygame.image.load('Assets/gasgame/gas_station.png')
        gas_station_rect = gas_station.get_rect(topleft = (450,50))
        screen.blit(gas_station, gas_station_rect)

    def buy_menu(self, game):
        pos = pygame.mouse.get_pos()
        bg_x = width/2 - 290
        bg_y = height/2- 200
        bg = pygame.image.load('Assets/gasgame/buy_menu.png')
        bg_rect = bg.get_rect(topleft = (bg_x, bg_y))
        screen.blit(bg, bg_rect)

        more_fill = pygame.Rect(bg_x + 20, bg_y + 64, 172, 172)

        if more_fill.collidepoint(pos):
            pygame.draw.rect(screen, 'blue', more_fill, 4)

            if game.click:
                for sprites in player_sprite:
                    if sprites.money >= 100:
                        sprites.fill_per_sec += 1
                        sprites.money -= 100

        if not bg_rect.collidepoint(pos) and game.click:
            self.in_shop = False
















