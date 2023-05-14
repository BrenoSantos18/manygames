import pygame
from os import walk

width = 1084
height = 700

screen = pygame.display.set_mode((width, height))

player_sprite = pygame.sprite.Group()
car_sprite = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
interactive_sprites = pygame.sprite.Group()

street_group = pygame.sprite.Group()

gas_game = {
    'interact_range': {
        'left': pygame.math.Vector2(40,0) ,
        'right': pygame.math.Vector2(-40,0),
        'down': pygame.math.Vector2(0,40),
        'up': pygame.math.Vector2(0,-40)
    }
}



def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

