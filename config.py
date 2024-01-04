from functions import load_image
import pygame


FPS = 50
STEP = 16
GRAVITY = 4.5
tile_images = {'wall': load_image('down_wall.png'),
               'empty': load_image('font.png')}
tile_width = tile_height = 64

player = None
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()  # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()

clock = pygame.time.Clock()

game_flag = True
jump_move = 0

