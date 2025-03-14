import pygame
from os.path import join, isfile
from os import listdir

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

FPS = 60
PLAYER_VEL = 5


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=None):
    path = join("platformer-assets-main", dir1, dir2)


    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[image.replace('.png', '') + '_right'] = sprites
                all_sprites[image.replace('.png', '') + '_left'] = flip(sprites)
            else:
                all_sprites[image.replace('.png', '')] = sprites
    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.sprite = self.SPRITES["idle_right"][0]

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size, name="Block")
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):
    image = pygame.image.load(join("platformer-assets-main", "Background", name))
    _, _, width, height = image.get_rect()

    background = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            background.append(pos)

    return background, image


def get_block(size):
    path = join('platformer-assets-main', 'Terrain', 'Terrain.png')

    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)

    return pygame.transform.scale2x(surface)


def draw(window, background, bg_image, player, objects):
    for positions in background:
        window.blit(bg_image, positions)

    for object in objects:
        object.draw(window)

    player.draw(window)

def handle_vertical_collision(player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()
                collided_objects.append(obj)

        return collided_objects

def handle_move(player,objects):
    keys = pygame.key.get_pressed()
    print(keys[pygame.K_LEFT])

    player.x_vel = 0

    # collide_left = coll
    # todo написати collide_left та collide_right, тобто повинні бути функції які повертають
    # todo об'єкти з якими взаємодіє гравець зліва та справа




    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
        
    elif keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)


    vertical_collide = handle_vertical_collision(player,objects,player.y_vel)

    to_check = [*vertical_collide] #todo тут потрібно також добавити collide_left та collide right

    # for obj in to_check:
    #     if obj and obj.name == 




def main(window):
    clock = pygame.time.Clock()

    background, image = get_background('Blue.png')

    block_size = 96

    player = Player(100, HEIGHT - block_size - 64, 50, 50)

    floor = []
    for i in range(WIDTH // block_size + 1):
        floor.append(Block(i * block_size, HEIGHT - block_size, block_size))

    block = Block(block_size*2,HEIGHT - block_size * 2, block_size)
    block1 = Block(block_size*2,HEIGHT - block_size * 3, block_size)

    objects = [*floor,block,block1]

    running = True

    vel = 5

  
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.loop(FPS)
        handle_move(player,objects)
        draw(screen, background, image, player, objects)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main(screen)
