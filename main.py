from classes import *
from config import (FPS, WIDTH, HEIGHT)

pygame.init()
pygame.key.set_repeat(200, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()    # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()

start_screen()

player, level_x, level_y = generate_level(load_level("levelex.txt"))

running = True
flag = True
jump = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player.moving(pygame.key.get_pressed())

    if player.jump_flag:
        player.jump()

    player.update()
    screen_draw()
    pygame.display.flip()
    clock.tick(FPS)

terminate()
