import pygame
import os

pygame.init()
screen = pygame.display.set_mode((100, 100))


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
