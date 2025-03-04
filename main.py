import pygame
from os.path import join
pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

FPS = 60

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name = None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self,window):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Block(Object):
    def __init__(self,x,y,size):
        super().__init__(x,y,size,size,name = "Block")
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)



def get_background(name):
    image = pygame.image.load(join("platformer-assets-main","Background",name))
    _,_,width,height = image.get_rect()

    background = []
    
    for i in range(WIDTH//width + 1):
        for j in range(HEIGHT//height+1):
            pos = (i*width,j*height)
            background.append(pos)

    return background,image

def get_block(size):
    path = join('platformer-assets-main','Terrain','Terrain.png')

    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)

    rect = pygame.Rect(96,0,size,size)
    surface.blit(image,(0,0),rect)

    return pygame.transform.scale2x(surface)




def draw(window, background,bg_image,objects):
    for positions in background:
        window.blit(bg_image,positions)

    for object in objects:
        object.draw(window)


def main(window):
    pygame.time.Clock().tick(FPS)

    background,image = get_background('Blue.png')

    block_size = 96

    block = Block(0,0,block_size)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Оновлення екрану
        draw(screen,background,image,[block])
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main(screen)