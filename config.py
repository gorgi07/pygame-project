from functions import load_image
import pygame


FPS = 50
STEP = 16
GRAVITY = 4.5
SPEED = 32
tile_images = {'wall': load_image('cobblestone.png'),
               'empty': load_image('font.png'),
               'empty_fakel': load_image('font_with_fakel.png'),
               'platform': load_image('cobblestone_16.png'),
               'portal': load_image('portal.png'),
               'down_flag': load_image('down_flag.png'),
               'up_flag': load_image('up_flag.png'),
               'down_btn1': load_image('down_button1.png'),
               'up_btn1': load_image('up_button1.png'),
               'down_btn2': load_image('down_button2.png'),
               'up_btn2': load_image('up_button2.png')}
tile_width = tile_height = 64

jump_sound = pygame.mixer.Sound('data/jump.ogg')

player = None
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()  # игрок сталкивается с этими спрайтами
empty_group = pygame.sprite.Group()  # игрок проходит через эти спрайты
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()    # спрайт портала(финиша)
flags_group = pygame.sprite.Group()     # спрайт флажков
buttons_group = pygame.sprite.Group()


clock = pygame.time.Clock()

game_flag = True
jump_move = 0
