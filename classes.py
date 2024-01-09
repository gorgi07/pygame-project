import pygame
from functions import load_image
from config import (tile_width, tile_height, tile_images, STEP, GRAVITY, FPS,
                    wall_group, empty_group, game_flag, jump_move, SPEED,
                    player_group, finish_group, all_sprites, flags_group)

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
            elif level[y][x] == '_':
                Platform(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == 'F':
                Finish(x, y)
            elif level[y][x] == 'f':
                Flag(x, y)
            elif level[y][x] == '+':
                ActVertPlatform(x, y, 64)
            elif level[y][x] == '-':
                ActGorPlatform(x, y, 32)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Wall(pygame.sprite.Sprite):
    """
    Класс твердой стены
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['wall']
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


class Platform(pygame.sprite.Sprite):
    """
    Класс платформы (полублока)
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['platform']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class ActVertPlatform(Platform):
    """
    Класс подвижной платформы(вертикальное движение)
    """
    def __init__(self, pos_x, pos_y, distance):
        super().__init__(pos_x, pos_y)
        self.v = SPEED
        self.start = pos_y * tile_height
        self.y = float(pos_y * tile_height)
        self.dist = distance

    def update(self):
        self.y += self.v / FPS
        if abs(self.y - self.start) >= self.dist:
            self.y -= self.v / FPS
            self.v = -self.v
        self.rect.y = int(self.y)
        if pygame.sprite.spritecollideany(self, player_group):
            player = pygame.sprite.spritecollide(self, player_group, False)[0]
            if player.rect.y > self.rect.y:
                print(1)


class ActGorPlatform(Platform):
    """
    Класс подвижной платформы(горизонтальное движение)
    """
    def __init__(self, pos_x, pos_y, distance):
        super().__init__(pos_x, pos_y)
        self.v = SPEED
        self.dist = distance
        self.start = pos_x * tile_height
        self.x = float(pos_x * tile_height)

    def update(self):
        self.x += self.v / FPS
        if abs(self.x - self.start) >= self.dist:
            self.x -= self.v / FPS
            self.v = -self.v
        self.rect.x = int(self.x)
        while pygame.sprite.spritecollideany(self, player_group):
            player = pygame.sprite.spritecollide(self, player_group, False)[0]
            if self.v > 0:
                player.rect.x += 1
            else:
                player.rect.x -= 1


class Finish(pygame.sprite.Sprite):
    """
    Класс финиша
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images['portal']
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10,
                                               tile_height * pos_y + 13)


class Flag(pygame.sprite.Sprite):
    """
    Класс флажков
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(flags_group, all_sprites)
        self.image = tile_images['down_flag']
        self.activity = True
        self.rect = self.image.get_rect().move(tile_width * pos_x + 12,
                                               tile_height * pos_y + 3)


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
        self.flying = False
        self.can_fly = False
        self.image = self.player_image_right
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 20)
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

        if not keys[pygame.K_SPACE]:
            self.flying = False

        if self.can_fly and keys[pygame.K_SPACE]:
            self.flying = True

    def update(self):
        """
        Метод обновления изменений игрока
        """
        global game_flag, jump_move
        if jump_move == 0:
            if self.flying:
                grav = GRAVITY // 4
            else:
                grav = GRAVITY
            self.rect.y += grav
            sprites = pygame.sprite.spritecollide(self, wall_group, False)
            if not pygame.sprite.spritecollideany(self, wall_group):
                game_flag = False
            while (pygame.sprite.spritecollideany(self, wall_group) and
                   all(map(lambda block: block.rect.y >= self.rect.y,
                           sprites))):
                self.rect.y -= 1
                game_flag = True
