import pygame
from game_functions import start_screen, screen_clear, terminate
from screen import screen
from functions import check_db

pygame.init()
pygame.key.set_repeat(200, 70)
screen = screen

check_db("game_db")

try:
    start_screen()
except KeyboardInterrupt:
    terminate()
finally:
    screen_clear()
