import pygame
import pygame_gui
import sqlite3
from pygame_gui.core import ObjectID
import webbrowser
from functions import (load_image, load_level, terminate)
from classes import generate_level
from config import (tile_width, tile_height, FPS,
                    clock, wall_group, empty_group,
                    player_group, finish_group, tile_images, flags_group,
                    all_sprites)
from screen import (screen, WIDTH, HEIGHT)


pygame.init()


def screen_draw():
    """
    Функция отрисовки изменений окна
    """
    screen.fill(pygame.Color(0, 0, 0))
    empty_group.draw(screen)
    finish_group.draw(screen)
    flags_group.draw(screen)
    wall_group.draw(screen)
    player_group.draw(screen)


def print_text(text: str, coord: tuple, color='green', mn=1.5, size=40):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    text_x = coord[0] - text.get_width() // 2
    text_y = round(coord[1] * mn)
    screen.blit(text, (text_x, text_y))


def finish_screen(name, _id, flags):
    fon = pygame.transform.scale(load_image('fon3.png'), (WIDTH, HEIGHT))
    fon.set_alpha(200)
    screen.blit(fon, (0, 0))

    window = pygame.transform.scale(load_image(f'finish_picture{flags}.png'),
                                    (WIDTH // 3 * 2, HEIGHT // 3 * 2))
    screen.blit(window, (WIDTH // 6, HEIGHT // 6))

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    next_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, 310), (200, 40)),
        text="Следующий уровень",
        manager=manager
    )
    repeat_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, 370), (200, 40)),
        text="Начать заново",
        manager=manager
    )
    menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, 430), (200, 40)),
        text="К уровням",
        manager=manager
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    screen_clear()
                    if event.ui_element == next_button:
                        go_level(_id + 1, (1, flags))
                    elif event.ui_element == repeat_button:
                        go_level(_id, (1, flags))
                    elif event.ui_element == menu_button:
                        levels_screen(name)

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def screen_clear():
    all_sprites.empty()
    wall_group.empty()
    player_group.empty()
    finish_group.empty()
    empty_group.empty()
    flags_group.empty()


def finish_level(name, _id, flags):
    con = sqlite3.connect("game_db.db")
    cur = con.cursor()
    level = f"level_{_id}"
    res = cur.execute(f"""SELECT {level} FROM players WHERE name = ?""",
                      (name, )).fetchone()
    if int(res[0][3]) < flags:
        cur.execute(f"""UPDATE players SET {level} = ? WHERE name = ?""",
                    (f"1, {flags}", name))
    con.commit()
    cur.close()
    finish_screen(name, _id, flags)


def go_level(_id: int, result: tuple):
    running = True
    count_flag = 0
    if _id != 1:
        if result[0] == 1:
            player, level_x, level_y, text = generate_level(
                load_level(f"level{_id}.txt"))
        else:
            print("error")
            return
    else:
        player, level_x, level_y, text = generate_level(
            load_level(f"level{_id}.txt"))
    text_time = 0
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif keys[pygame.K_ESCAPE]:
                pygame.display.iconify()
            else:
                player.moving(keys)

        if player.jump_flag:
            player.jump()

        wall_group.update()
        player.update()
        flags_group.update()
        finish_group.update()
        count_flag += checking_flags(player, flags_group)
        screen_draw()
        if _id == 1:
            fog(player)
        if text_time < 3 * 50:
            print_text(text, (WIDTH // 2, tile_height))
            text_time += 1
        finish_tile = pygame.sprite.spritecollideany(player, finish_group)
        new_text_time = 0
        if finish_tile is not None:
            if new_text_time < 2 * 50:
                print_text("Нажмите Е для выхода",
                           (finish_tile.rect.x, finish_tile.rect.y - 17),
                           color="blue", mn=1, size=15)
                new_text_time += 1
            if keys[pygame.K_e]:
                new_text_time = 2 * 50
                running = False
        else:
            new_text_time = 2 * 50
        pygame.display.flip()
        clock.tick(FPS)

    finish_level("Player", _id, count_flag)
    levels_screen("Player")


def fog(player):
    for x in range(WIDTH // tile_width):
        for y in range(HEIGHT // tile_height):
            if (abs(player.rect.x // tile_width - x) >= 2
                    or abs(player.rect.y // tile_height - y) >= 2):
                pygame.draw.rect(screen, 'black', (x * tile_width,
                                                   y * tile_height,
                                                   tile_width,
                                                   tile_height))


def levels_screen(name):
    con = sqlite3.connect("game_db.db")
    cur = con.cursor()

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    levels_manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    first_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 0), 20),
            (WIDTH // 4 - 30,  WIDTH // 4 - 30)),
        text="1",
        manager=levels_manager
    )

    second_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 1), 20),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="2",
        manager=levels_manager
    )

    third_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 2), 20),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="3",
        manager=levels_manager
    )

    fourth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 3), 20),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="4",
        manager=levels_manager
    )

    fifth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 0), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="5",
        manager=levels_manager
    )

    sixth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 1), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="6",
        manager=levels_manager
    )

    seventh_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 2), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="7",
        manager=levels_manager
    )

    eighth_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (20 + (WIDTH // 4 * 3), 10 + HEIGHT // 2),
            (WIDTH // 4 - 30, WIDTH // 4 - 30)),
        text="8",
        manager=levels_manager
    )

    levels_sprites_group = pygame.sprite.Group()
    count = 1
    for i in range(2):
        for j in range(4):
            ind = "none"
            resul = (cur.execute(
                f"""SELECT level_{count} FROM players WHERE name = ?""",
                (name,)).fetchone())
            resul = (int(resul[0][0]), int(resul[0][3]))
            if resul[0] == 1:
                ind = resul[1]

            flag_sprite = pygame.sprite.Sprite(levels_sprites_group)
            flag_sprite.image = load_image(f"levels_flags_{ind}.png")
            flag_sprite.rect = flag_sprite.image.get_rect()
            flag_sprite.rect.x = (20 + (WIDTH // 4 * j))
            if i == 0:
                flag_sprite.rect.y = (20 + (WIDTH // 4 - 30))
            else:
                flag_sprite.rect.y = ((10 + HEIGHT // 2) + (WIDTH // 4 - 30))
            count += 1

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                start_screen()

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
                        level = f"level_{level_id - 1}"
                        res = (cur.execute(
                            f"""SELECT {level} FROM players WHERE name = ?""",
                            (name,)).fetchone())
                        res = (int(res[0][0]), int(res[0][3]))
                    else:
                        res = (1, 0)

                    cur.close()
                    go_level(level_id, res)

            levels_manager.process_events(event)
        levels_manager.update(time_delta)
        levels_manager.draw_ui(screen)
        levels_sprites_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def information_screen():
    intro_text = ["АВТОРЫ ИДЕИ:",
                  "Ерохин Егор  Никулин Никита", "",
                  "РАЗРАБОТЧИКИ:",
                  "Никулин Никита   Ерохин Егор", "",
                  "МУЗЫКАНТЫ:",
                  "Никулин Никита   Ерохин Егор", "",
                  "ХУДОЖНИКИ:",
                  "Ерохин Егор  Никулин Никита", "",
                  "ДА И ПРОСТО ХОРОШИЕ ЛЮДИ:",
                  "Никулин Никита   Ерохин Егор "
                  ]

    fon = pygame.transform.scale(load_image('fon3.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, "#2fca77")
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')

    git_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 608), (610, 50)),
        text="З.Ы. Поддержать начинающих разработчиков можно добрым словом "
             "на Github :)",
        manager=manager,
        object_id=ObjectID(class_id='@git_buttons',
                           object_id='#git_button')
    )

    support_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, 668), (290, 50)),
        text="З.Ы.Ы. Или переводом на карту ^_^",
        manager=manager,
        object_id=ObjectID(class_id='@git_buttons',
                           object_id='#git_button')
    )

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                start_screen()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == git_button:
                        webbrowser.open(
                            "https://github.com/gorgi07/pygame-project"
                        )
                    elif event.ui_element == support_button:
                        pass

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    """
    Функция создания заставки стартового окна
    """
    fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 50), (300, 70)),
        text="Играть",
        manager=manager
    )

    education_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 170), (300, 70)),
        text="Обучение",
        manager=manager
    )

    information_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 290), (300, 70)),
        text="Об авторах",
        manager=manager
    )

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 648), (300, 70)),
        text="Выход",
        manager=manager
    )

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        levels_screen("Player")
                    elif event.ui_element == education_button:
                        return
                    elif event.ui_element == information_button:
                        information_screen()
                    elif event.ui_element == exit_button:
                        terminate()

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def checking_flags(player, flags_group):
    flag = pygame.sprite.spritecollideany(player, flags_group)
    if flag is not None:
        if (flag.activity and flag.rect.x - player.rect.x < 20
                and flag.rect.y - player.rect.y < 20):
            flag.activity = False
            flag.image = tile_images['up_flag']
            return 1
    return 0
