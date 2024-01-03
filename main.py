from classes import *
from config import (WIDTH, HEIGHT)

pygame.init()
pygame.key.set_repeat(200, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.FULLSCREEN)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()    # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()

start_screen()
