import pygame
import sys
from load_images import load_image
from config import (tile_images, tile_width, tile_height,
                    STEP, GRAVITY, WIDTH, HEIGHT, FPS)

pygame.init()
player = None
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()  # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
flag = True
jump = 0


def load_level(filename: str) -> list:
    """
    Функция для загрузки (чтения) уровня
    игры из текстового файла
    """
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    """
    Функция для генерации уровня, по
    прочитанной схеме уровня
    """
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Background(x, y)
            elif level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                Background(x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    """
    Функция завершения игры
    """
    pygame.quit()
    sys.exit()


def start_screen():
    """
    Функция создания заставки стартового окна
    """
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.KEYDOWN or
                  event.type == pygame.MOUSEBUTTONDOWN):
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def screen_draw():
    """
    Функция отрисовки изменений окна
    """
    global screen, wall_group, empty_group, player_group
    screen.fill(pygame.Color(0, 0, 0))
    wall_group.draw(screen)
    empty_group.draw(screen)
    player_group.draw(screen)


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

        self.add(player_group)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.jump_flag = True

    def jump(self):
        """
        Метод прыжка у игрока
        """
        global jump, flag
        if jump > 0:
            flag = False
            self.rect.y -= STEP * 1.2
            if pygame.sprite.spritecollideany(self, wall_group):
                jump = 0
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y += 1
            if jump > 0:
                jump -= 1
            else:
                self.jump_flag = False

    def moving(self, keys):
        """
        Метод вижения у игрока
        """
        global jump
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

        if keys[pygame.K_UP] and flag:
            jump, self.jump_flag = 6, True

    def update(self):
        """
        Метод обновления изменений игрока
        """
        global jump, flag
        if jump == 0:
            self.rect.y += GRAVITY
            if not (pygame.sprite.spritecollideany(self, wall_group)):
                flag = False
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= 1
                flag = True
