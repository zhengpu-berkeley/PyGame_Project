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
        pygame.mixer.init()
        self.background = pygame.image.load('resources/background.jpeg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()
        self.ate_apple_sound = pygame.mixer.Sound('resources/1_snake_game_resources_ding.mp3')
        self.died_sound = pygame.mixer.Sound('resources/1_snake_game_resources_crash.mp3')
        pygame.mixer.Sound.set_volume(self.ate_apple_sound, 0.1)
        pygame.mixer.Sound.set_volume(self.died_sound, 0.1)
        self.surface = pygame.display.set_mode((window_size, window_size))
        self.render_background()
        pygame.display.flip()
        self.snake = Snake(self.surface, 3)
        self.snake.draw_block()
        self.apple = Apple(self.surface)
        self.apple.draw_apple()

    def render_background(self):
        self.surface.blit(self.background, (-1, -1))

    def run(self):
        running = False
        starting = True
        died = False
        while starting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    starting = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        starting = False
                    if event.key == K_RETURN:
                        starting = False
                        running = True
            self.draw_all(False)
            time.sleep(0.3)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        died = False
                        pygame.mixer.music.unpause()
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
            try:
                if not died:
                    self.draw_all()
            except:
                pygame.mixer.music.pause()
                self.show_game_over()
                died = True
                self.reset()
            time.sleep(0.3)

    def display_score(self):
        font = pygame.font.SysFont('arial', 20)
        score = font.render(f"Score: {self.snake.length}", True, (255, 0, 0))
        self.surface.blit(score, (window_size // 1.25, window_size // 8))
        pygame.display.flip()

    def snake_ate_apple(self):
        if self.apple.block_x == self.snake.block_x[0] and self.apple.block_y == self.snake.block_y[0]:
            pygame.mixer.Sound.play(self.ate_apple_sound)
            self.apple.move()
            self.snake.increase_length()

    def show_game_over(self):
        pygame.mixer.Sound.play(self.died_sound)
        self.surface.fill((125, 0, 0))
        font = pygame.font.SysFont('arial', 30)
        show_score = font.render(f'You Died... Final Score: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(show_score, (window_size // 10, window_size // 2))
        play_again = font.render(f'To Play Again, Press Enter', True, (255, 255, 255))
        self.surface.blit(play_again, (window_size // 10, window_size // 2 + block_size))
        pygame.display.flip()
        self.reset()

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    # playing the game
    def draw_all(self, moving=True):
        self.render_background()
        if moving:
            self.snake.always_move()
        else:
            font = pygame.font.SysFont('arial', 30)
            show_score = font.render(f'To Play, Press Enter', True, (255, 255, 255))
            self.surface.blit(show_score, (window_size // 10, window_size // 2))
        self.apple.draw_apple()
        self.display_score()
        self.snake_ate_apple()
        self.snake.ate_itself()
        self.snake.is_out()


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/apple.jpeg').convert()
        self.block_x = block_size * random.randint(0, window_size//block_size-1)
        self.block_y = block_size * random.randint(0, window_size//block_size-1)

    def draw_apple(self):
        self.parent_screen.blit(self.block, (self.block_x, self.block_y))
        pygame.display.flip()
        return

    def move(self):
        self.block_x = block_size * random.randint(0, window_size // block_size - 1)
        self.block_y = block_size * random.randint(0, window_size // block_size - 1)


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

    def ate_itself(self):
        if self.length <= 3:
            return
        for i in range(1, self.length):
            if self.block_x[0] == self.block_x[i] and self.block_y[0] == self.block_y[i]:
                print('snake ate itself')
                raise 'Game Over - You ate yourself'
        return

    def is_out(self):
        if self.block_x[0] < 0 or self.block_x[0] >= window_size:
            print('snake is out')
            raise 'Game Over - You went out of bound'
        if self.block_y[0] < 0 or self.block_y[0] >= window_size:
            print('snake is out')
            raise 'Game Over - You went out of bound'
        return

    def draw_block(self):
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
