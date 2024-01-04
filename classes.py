import pygame
from functions import load_image
from config import (tile_width, tile_height, tile_images, STEP, GRAVITY,
                    wall_group, empty_group, game_flag, jump_move,
                    player_group, finish_group, all_sprites)

pygame.init()
game_flag, jump_move = game_flag, jump_move


def generate_level(level):
    """
    Функция для генерации уровня, по
    прочитанной схеме уровня
    """
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Background(x, y)
            if level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == 'F':
                Finish(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Wall(pygame.sprite.Sprite):
    """
    Класс твердой стены
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['wall']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class Background(pygame.sprite.Sprite):
    """
    Класс фона
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class Finish(pygame.sprite.Sprite):
    """
    Класс финиша
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class Player(pygame.sprite.Sprite):
    """
    Класс игрока
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.player_image_right = load_image('player.png')
        self.player_image_left = pygame.transform.flip(
            self.player_image_right,
            True,
            False
        )
        self.image = self.player_image_right
        self.mask = pygame.mask.from_surface(self.image)

        self.add(player_group)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.jump_flag = True

    def jump(self):
        """
        Метод прыжка у игрока
        """
        global game_flag, jump_move
        if jump_move > 0:
            game_flag = False
            self.rect.y -= STEP * 0.6
            if pygame.sprite.spritecollideany(self, wall_group):
                jump_move = 0
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y += 1
            if jump_move > 0:
                jump_move -= 1
            else:
                self.jump_flag = False

    def moving(self, keys):
        """
        Метод вижения у игрока
        """
        global jump_move, game_flag
        if keys[pygame.K_LEFT]:
            self.rect.x -= STEP
            self.image = self.player_image_left
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += 1

        if keys[pygame.K_RIGHT]:
            self.rect.x += STEP
            self.image = self.player_image_right
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= 1

        if keys[pygame.K_UP] and game_flag:
            jump_move, self.jump_flag = 16, True

    def update(self):
        """
        Метод обновления изменений игрока
        """
        global game_flag, jump_move
        if jump_move == 0:
            self.rect.y += GRAVITY
            sprites = pygame.sprite.spritecollide(self, wall_group, False)
            if not pygame.sprite.spritecollideany(self, wall_group):
                game_flag = False
            while (pygame.sprite.spritecollideany(self, wall_group) and
                   all(map(lambda block: block.rect.y >= self.rect.y,
                           sprites))):
                self.rect.y -= 1
                game_flag = True
