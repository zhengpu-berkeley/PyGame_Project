import pygame
from pygame.locals import *
print('hello world')


def draw_block():
    surface.fill((255, 255, 255))
    surface.blit(block, (block_x, block_y))
    pygame.display.flip()
    return


if __name__ == '__main__':
    pygame.init()
    # this creates a display of size (500,500) pixels
    # the surface variable is the main window, the background
    surface = pygame.display.set_mode((500,500))
    # this modifies the color of the display to (R,G,B)
    # we can use Google Color Picker to find what we want
    surface.fill((255,255,255)) # (255,255,255) is white

    # loading the block image into a variable called block
    # .convert() : Creates a new copy of the Surface with the pixel format changed
    block = pygame.image.load('resources/block.jpeg').convert()



    # drawing the block onto the surface with the blit() function
    # specify position of block with (block_x , block_y)
    block_x , block_y = 100 , 100
    surface.blit(block, (block_x , block_y))

    # flip() : Update the full display Surface to the screen
    pygame.display.flip()

    running = True
    while running:
        # check out all kinds of events:
        # https://www.pygame.org/docs/ref/event.html
        # events like KEYDOWN, QUIT are from pygame.locals
        # they are variables predefined...
        for event in pygame.event.get():
            # KEYDOWN event triggered when the keyboard buttons are pressed
            # check out all the keys:
            # https://www.pygame.org/docs/ref/key.html
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    block_y -= 10
                    draw_block()
                elif event.key == K_DOWN:
                    block_y += 10
                    draw_block()
                elif event.key == K_RIGHT:
                    block_x += 10
                    draw_block()
                elif event.key == K_LEFT:
                    block_x -= 10
                    draw_block()
                pass
            # QUIT in event type means we hit the [x] to close window
            elif event.type == QUIT:
                running = False




