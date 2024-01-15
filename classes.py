import pygame
from functions import load_image
from config import (tile_width, tile_height, tile_images, STEP, GRAVITY, FPS,
                    wall_group, empty_group, game_flag, jump_move, SPEED,
                    player_group, finish_group, all_sprites, flags_group,
                    buttons_group)

pygame.init()
game_flag, jump_move = game_flag, jump_move


def generate_level(level):
    """
    Функция для генерации уровня, по
    прочитанной схеме уровня
    """
    new_player, x, y = None, None, None
    for y in range(len(level) - 1):
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
            elif level[y][x] == 'U':
                ActiveBlock(x, y, 'up', 64)
            elif level[y][x] == 'D':
                ActiveBlock(x, y, 'down', 65)
            elif level[y][x] == 'L':
                ActiveBlock(x, y, 'left', 64)
            elif level[y][x] == 'R':
                ActiveBlock(x, y, 'right', 64)
            elif level[y][x] == '1':
                NotStickyButton(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, level[-1]


class Wall(pygame.sprite.Sprite):
    """
    Класс твердой стены
    """
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class ActiveBlock(Wall):
    def __init__(self, pos_x, pos_y, direct, distance):
        super().__init__(pos_x, pos_y)
        self.start = {'x': float(pos_x * tile_width),
                      'y': float(pos_y * tile_height)}
        self.distance = distance
        self.act_flag = False
        self.x, self.y = pos_x * tile_width, pos_y * tile_height
        if direct == 'up' or direct == 'left':
            self.v = -32
        elif direct == 'down' or direct == 'right':
            self.v = 32
        if direct == 'up' or direct == 'down':
            self.action = 'y'
        else:
            self.action = 'x'

    def update(self):
        if self.action == 'x' and self.act_flag:
            self.x += self.v / FPS
            blocks = pygame.sprite.spritecollide(self, wall_group, False)
            flag = True
            if abs(self.x - self.start['x']) >= self.distance:
                self.x -= self.v / FPS
                self.act_flag = False
                flag = False
            if flag and len(blocks) > 1:
                self.x -= 3 * self.v / FPS
                self.act_flag = False
            self.rect.x = int(self.x)
            while pygame.sprite.spritecollideany(self, player_group):
                player = \
                    pygame.sprite.spritecollide(self, player_group, False)[0]
                if 0 < self.v:
                    player.rect.x += 1
                else:
                    player.rect.x -= 1
        elif self.action == 'y' and self.act_flag:
            self.y += self.v / FPS
            blocks = pygame.sprite.spritecollide(self, wall_group, False)
            flag = True
            if abs(self.y - self.start['y']) >= self.distance:
                self.y -= self.v / FPS
                self.act_flag = False
                flag = False
            if flag and len(blocks) > 1:
                self.y -= 3 * self.v / FPS
                self.act_flag = False
            self.rect.y = int(self.y)
            if pygame.sprite.spritecollideany(self, player_group):
                player = \
                    pygame.sprite.spritecollide(self, player_group, False)[0]
                if player.rect.y > self.rect.y:
                    pass


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
        blocks = pygame.sprite.spritecollide(self, wall_group, False)
        flag = True
        if abs(self.y - self.start) >= self.dist:
            self.y -= self.v / FPS
            self.v = -self.v
            flag = False
        if flag and len(blocks) > 1:
            self.y -= 3 * self.v / FPS
            self.v = -self.v
        self.rect.y = int(self.y)
        if pygame.sprite.spritecollideany(self, player_group):
            player = pygame.sprite.spritecollide(self, player_group, False)[0]
            if player.rect.y > self.rect.y:
                pass


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
        blocks = pygame.sprite.spritecollide(self, wall_group, False)
        flag = True
        if abs(self.x - self.start) >= self.dist:
            self.x -= self.v / FPS
            self.v = -self.v
            flag = False
        if flag and len(blocks) > 1:
            self.x -= 3 * self.v / FPS
            self.v = -self.v
        self.rect.x = int(self.x)
        while pygame.sprite.spritecollideany(self, player_group):
            player = pygame.sprite.spritecollide(self, player_group, False)[0]
            if 0 < self.v:
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


class NotStickyButton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buttons_group, all_sprites)
        self.image = tile_images['up_btn1']
        self.activity = True
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y + 53)

    def update(self):
        if (pygame.sprite.spritecollideany(self, player_group)
                and self.activity):
            self.image = tile_images['down_btn1']
            self.rect.y += 2
            self.activity = False
            for elem in wall_group:
                if type(elem) is ActiveBlock:
                    elem.act_flag = True


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
