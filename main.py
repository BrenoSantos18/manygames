import pygame, time, sys
from settings import *
from gasgame import GasGame
from drivegame import DriveGame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Many Games')
        self.gasgame = GasGame()
        self.drivegame = DriveGame()

        self.in_menu = True
        self.choosing = False
        self.running_game = False
        self.paused = False
        self.actual_game = 'none'

        self.click = False
        self.click_cooldown = 100
        self.click_time = 0


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.click_time >= self.click_cooldown:
            self.click = False


    def main_menu(self):
        pos = pygame.mouse.get_pos()


        if not self.choosing:
            bg = pygame.image.load('Assets/menu/menu.png')
            bg_rect = bg.get_rect(topleft = (0,0))
            screen.blit(bg, bg_rect)

            games = pygame.Rect(142,103,800,100)
            quit = pygame.Rect(142,496,800,100)
            options = pygame.Rect(142,300,800,100)

            if games.collidepoint(pos):
                games_surf = pygame.image.load('Assets/menu/start.png')
                games_rect = games_surf.get_rect(topleft = (142, 104))
                screen.blit(games_surf, games_rect)
                if self.click:
                    self.click = False
                    self.choosing = True

            if options.collidepoint(pos):
                options_surf = pygame.image.load('Assets/menu/options.png')
                options_rect = options_surf.get_rect(topleft = (142, 300))
                screen.blit(options_surf, options_rect)

            if quit.collidepoint(pos):
                quit_surf = pygame.image.load('Assets/menu/quit.png')
                quit_rect = quit_surf.get_rect(topleft = (142, 496))
                screen.blit(quit_surf, quit_rect)
                if self.click:
                    pygame.quit()
                    sys.exit()

        else:
            screen.fill('black')
            gasgame = pygame.image.load('Assets/game_icon/gasgame.png').convert_alpha()
            scale = pygame.transform.scale(gasgame, (300,400))
            gas_rect = gasgame.get_rect(topleft = (20,20))

            drivegame = pygame.image.load('Assets/game_icon/drivegame.png').convert_alpha()
            d_scale = pygame.transform.scale(drivegame, (100,200))
            drive_rect = d_scale.get_rect(topleft = (280,150))


            gas_bg = pygame.Rect(20,20,200,400)
            pygame.draw.rect(screen, 'white', gas_bg)
            screen.blit(scale, gas_rect)

            drive_bg = pygame.Rect(240,20,200,400)
            pygame.draw.rect(screen, 'white', drive_bg)
            screen.blit(d_scale, drive_rect)

            if gas_bg.collidepoint(pos):
                pygame.draw.rect(screen, 'grey', gas_bg, 5)

                if self.click:
                    self.in_menu = False
                    self.choosing = False
                    self.running_game = True
                    self.actual_game = 'gasgame'

            if drive_bg.collidepoint(pos):
                pygame.draw.rect(screen, 'grey', drive_bg, 5)

                if self.click:
                    self.in_menu = False
                    self.choosing = False
                    self.running_game = True
                    self.actual_game = 'drivegame'

    def paused_menu(self):
        pos = pygame.mouse.get_pos()
        bg = pygame.Rect(width/2 - 300,50,600,500)
        resume = pygame.Rect(width/2 - 200,80,400,50)
        quit = pygame.Rect(width/2 - 200,170,400,50)

        pygame.draw.rect(screen, 'black', bg)
        pygame.draw.rect(screen, 'white', resume)
        pygame.draw.rect(screen, 'white', quit)

        if resume.collidepoint(pos):
            pygame.draw.rect(screen, 'grey', resume)
            if self.click:
                self.paused = False

        if quit.collidepoint(pos):
            pygame.draw.rect(screen, 'grey', quit)

            if self.click:
                self.paused = False
                self.running_game = False
                self.in_menu = True








    def run(self):
        current_time = time.time()
        while True:
            dt = time.time() - current_time
            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.click:
                    if event.button == 1:
                        self.click = True
                        self.click_time = pygame.time.get_ticks()

            self.cooldown()
            self.player_input()


            screen.fill('black')
            if self.in_menu:
                self.main_menu()

            if self.running_game:
                if self.actual_game == 'gasgame':
                    self.gasgame.game_run(dt, self)

                if self.actual_game == 'drivegame':
                    self.drivegame.in_game = True
                    self.drivegame.run(dt, self)

                if self.paused:
                    self.paused_menu()


            pygame.display.update()


    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.running_game:
            if self.actual_game == 'gasgame':
                if keys[pygame.K_ESCAPE]:
                    self.paused = True

                if keys[pygame.K_TAB]:
                    self.gasgame.in_shop = True





if __name__ == "__main__":
    game = Game()
    game.run()


