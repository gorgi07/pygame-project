import os
import sys
import pygame
# from PIL import Image

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 400
HEIGHT = 300
STEP = 20
GRAVITY = 3.5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()    # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()


def mirroring(image):
    im = Image.open('data/' + image)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im.save(f'data/flipped{image}')
    return f'flipped{image}'


def load_image(name, color_key=None):
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Grass(x, y)
            elif level[y][x] == '#':
                Box(x, y)
            elif level[y][x] == '@':
                Grass(x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
# player_image_right = load_image(mirroring('mario.png'))
player_image_left = load_image('mario.png')


tile_width = tile_height = 50


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = tile_images['wall']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class Grass(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height
                                               * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image_left
        self.add(player_group)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.jump_flag = True

    def jump(self):
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
        global jump
        if keys[pygame.K_LEFT]:
            self.rect.x -= STEP
            # self.image = player_image_left
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x += 1
        if keys[pygame.K_RIGHT]:
            self.rect.x += STEP
            # self.image = player_image_right
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.x -= 1
        if keys[pygame.K_UP] and flag:
            jump, self.jump_flag = 6, True

    def update(self):
        global jump, flag
        if jump == 0:
            self.rect.y += GRAVITY
            if not pygame.sprite.spritecollideany(self, wall_group):
                flag = False
            while pygame.sprite.spritecollideany(self, wall_group):
                self.rect.y -= 1
                flag = True


start_screen()

player, level_x, level_y = generate_level(load_level("levelex.txt"))

running = True
flag = True
jump = 0


def screen_draw():
    global screen, wall_group, empty_group, player_group
    screen.fill(pygame.Color(0, 0, 0))
    wall_group.draw(screen)
    empty_group.draw(screen)
    player_group.draw(screen)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player.moving(pygame.key.get_pressed())

    if player.jump_flag:
        player.jump()

    player.update()

    screen_draw()

    pygame.display.flip()

    clock.tick(FPS)

terminate()