import sqlite3
import sys
import pygame
import os
import qrcode
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


def check_db(name: str):
    """
    Функция для создания базы данных игры, если она отсутствует
    """
    if not os.path.exists(f"data/{name}.db"):
        file = open(f"data/{name}.db", "a+")
        file.close()

        con = sqlite3.connect(f"data/{name}.db")
        cur = con.cursor()

        cur.execute('''CREATE TABLE "players" (
            "name"	TEXT,
            "level_1"	TEXT,
            "level_2"	TEXT,
            "level_3"	TEXT,
            "level_4"	TEXT,
            "level_5"	TEXT,
            "level_6"	TEXT,
            "level_7"	TEXT,
            "level_8"	TEXT)''')

        con.commit()
        con.close()

        con = sqlite3.connect(f"data/{name}.db")
        cur = con.cursor()

        cur.execute('''INSERT INTO players 
            (name, level_1, level_2, level_3, level_4, 
            level_5, level_6, level_7, level_8) 
            VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    ("Player", "0, 0", "0, 0", "0, 0", "0, 0",
                     "0, 0", "0, 0", "0, 0", "0, 0"))

        con.commit()
        con.close()


def create_qr(text: str):
    image = qrcode.make(text)
    new_text = text.replace(" ", "_")
    if len(new_text) > 10:
        image.save(f"data/qr_{new_text[:9]}.png")
    else:
        image.save(f"data/qr_{new_text}.png")


def terminate():
    """
    Функция завершения игры
    """
    pygame.quit()
    sys.exit()
