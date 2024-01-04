import pygame
import pygame_gui
import sqlite3
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


def finish_level():
    pass


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
        flags_group.update()
        finish_group.update()
        checking_flags(player, flags_group)
        screen_draw()
        # if _id == 1 or _id == 2:
        #     fog(player)
        pygame.display.flip()
        clock.tick(FPS)
        finish_tile = pygame.sprite.spritecollideany(player, finish_group)
        if (finish_tile is not None and player.rect.x > finish_tile.rect.x
                and finish_tile.rect.y - player.rect.y < 20):
            running = False

    finish_level()
    levels_screen()


def fog(player):
    for x in range(WIDTH // tile_width):
        for y in range(HEIGHT // tile_height):
            if (abs(player.rect.x // tile_width - x) >= 2
                    or abs(player.rect.y // tile_height - y) >= 2):
                pygame.draw.rect(screen, 'black', (x * tile_width,
                                                   y * tile_height,
                                                   tile_width,
                                                   tile_height))


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


def checking_flags(player, flags_group):
    flag = pygame.sprite.spritecollideany(player, flags_group)
    if flag is not None:
        if (flag.activity and flag.rect.x - player.rect.x < 20
                and flag.rect.y - player.rect.y < 20):
            flag.activity = False
            flag.image = tile_images['up_flag']
