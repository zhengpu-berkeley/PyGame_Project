import pygame
from pygame.locals import *
import time
import random
print('hello world')
block_size = 40
window_size = 600


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((window_size, window_size))
        self.surface.fill((255, 255, 255))
        self.snake = Snake(self.surface, 3)
        self.snake.draw_block()
        self.apple = Apple(self.surface)
        self.apple.draw_apple()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                elif event.type == QUIT:
                    running = False
            self.draw_all()
            time.sleep(0.3)

    def draw_all(self):
        self.snake.always_move()
        self.apple.draw_apple()
        if self.is_collision(self.apple.block_x, self.apple.block_y,
                             self.snake.block_x[0], self.snake.block_y[0]):
            self.apple.move()
            self.snake.increase_length()



    def is_collision(self, apple_x, apple_y, block_x, block_y):
        if apple_x == block_x and apple_y == block_y:
            return True
        else:
            return False


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/apple.jpeg').convert()
        self.block_x = block_size * random.randint(0, window_size/block_size-1)
        self.block_y = block_size * random.randint(0, window_size/block_size-1)

    def draw_apple(self):
        self.parent_screen.blit(self.block, (self.block_x, self.block_y))
        pygame.display.flip()
        return

    def move(self):
        self.block_x = block_size * random.randint(0, window_size / block_size - 1)
        self.block_y = block_size * random.randint(0, window_size / block_size - 1)


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load('resources/block.jpeg').convert()
        self.block_x = [block_size] * length
        self.block_y = [block_size] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.block_x.append(self.block_x[-1])
        self.block_y.append(self.block_y[-1])

    def draw_block(self):
        self.parent_screen.fill((255, 255, 255))
        for block_id in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[block_id], self.block_y[block_id]))
        pygame.display.flip()
        return

    def always_move(self):
        for block_id in range(self.length-1, 0, -1):
            self.block_x[block_id] = self.block_x[block_id-1]
            self.block_y[block_id] = self.block_y[block_id-1]
        if self.direction == 'up':
            self.block_y[0] -= block_size
        elif self.direction == 'down':
            self.block_y[0] += block_size
        elif self.direction == 'right':
            self.block_x[0] += block_size
        elif self.direction == 'left':
            self.block_x[0] -= block_size
        self.draw_block()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'


if __name__ == '__main__':

    game = Game()
    game.run()