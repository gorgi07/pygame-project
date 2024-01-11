import sys
import pygame
import os
from screen import screen

pygame.init()
screen = screen


def load_image(name: str, color_key=None):
    """
    Функция загрузки изображений
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename: str) -> list:
    """
    Функция для загрузки (чтения) уровня
    игры из текстового файла
    """
    filename = "data/" + filename
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map[:-1]))
    array = list(map(lambda x: x.ljust(max_width, '.'), level_map[:-1]))
    array.append(level_map[-1])
    return array


def terminate():
    """
    Функция завершения игры
    """
    pygame.quit()
    sys.exit()
