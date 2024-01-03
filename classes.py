import pygame
import pygame_gui
import sys
import sqlite3
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
            Background(x, y)
            if level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    """
    Функция завершения игры
    """
    pygame.quit()
    sys.exit()


def go_level(_id, result):
    running = True
    if _id != 1:
        if result == 1:
            player, level_x, level_y = generate_level(
                load_level(f"levele{_id}.txt"))
        else:
            print("error")
            return
    else:
        player, level_x, level_y = generate_level(
            load_level(f"levele{_id}.txt"))

    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            elif keys[pygame.K_ESCAPE]:
                pygame.display.iconify()
            else:
                player.moving(keys)

        if player.jump_flag:
            player.jump()

        player.update()
        screen_draw()
        if _id == 1 or _id == 2:
            fog(player)
        pygame.display.flip()
        clock.tick(FPS)

    terminate()


def fog(player):
    for x in range(WIDTH // 64):
        for y in range(HEIGHT // 64):
            if (abs(player.rect.x // 64 - x) >= 2
                    or abs(player.rect.y // 64 - y) >= 2):
                pygame.draw.rect(screen, 'black', (x * 64, y * 64, 64, 64))


def levels_screen():
    con = sqlite3.connect("game_db.db")
    cur = con.cursor()

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    levels_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    first_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 0), 20),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="1",
        manager=levels_manager
    )

    second_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 1), 20),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="2",
        manager=levels_manager
    )

    third_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 2), 20),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="3",
        manager=levels_manager
    )

    fourth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 3), 20),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="4",
        manager=levels_manager
    )

    fifth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 0), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="5",
        manager=levels_manager
    )

    sixth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 1), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="6",
        manager=levels_manager
    )

    seventh_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 2), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="7",
        manager=levels_manager
    )

    eighth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 3), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, HEIGHT // 2 - 30)),
        text="8",
        manager=levels_manager
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.display.iconify()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    level_id = 1
                    if event.ui_element == first_button:
                        level_id = 1
                    elif event.ui_element == second_button:
                        level_id = 2
                    elif event.ui_element == third_button:
                        level_id = 3
                    elif event.ui_element == fourth_button:
                        level_id = 4
                    elif event.ui_element == fifth_button:
                        level_id = 5
                    elif event.ui_element == sixth_button:
                        level_id = 6
                    elif event.ui_element == seventh_button:
                        level_id = 7
                    elif event.ui_element == eighth_button:
                        level_id = 8

                    if level_id != 1:
                        res = (cur.execute(
                            """SELECT passed FROM levels WHERE id = ?""",
                            (level_id - 1,)).fetchone())[0]
                    else:
                        res = 1

                    go_level(level_id, res)

            levels_manager.process_events(event)
        levels_manager.update(time_delta)
        levels_manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    """
    Функция создания заставки стартового окна
    """
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, 50), (300, 70)),
        text="Играть",
        manager=manager
    )

    education_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, 170), (300, 70)),
        text="Обучение",
        manager=manager
    )

    information_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, 290), (300, 70)),
        text="Об авторах",
        manager=manager
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.display.iconify()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        levels_screen()
                    elif event.ui_element == education_button:
                        return
                    elif event.ui_element == information_button:
                        return

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def screen_draw():
    """
    Функция отрисовки изменений окна
    """
    global screen, wall_group, empty_group, player_group
    screen.fill(pygame.Color(0, 0, 0))
    empty_group.draw(screen)
    wall_group.draw(screen)
    player_group.draw(screen)


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
        global jump, flag
        if jump > 0:
            flag = False
            self.rect.y -= STEP * 0.6
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
            wall = pygame.sprite.spritecollideany(self, wall_group)
            if wall is not None:
                # print(pygame.sprite.collide_mask(self, wall))
                while pygame.sprite.collide_mask(self, wall) is not None:
                    # print(self.rect)
                    self.rect.x -= 1

        if keys[pygame.K_UP] and flag:
            jump, self.jump_flag = 16, True

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
