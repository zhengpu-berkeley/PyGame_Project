import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)


# TO DO ---> to make the game AGENT playable
# TO DO ---> to make the game take AI's action rather than keyboard input
# implement reset() function for the game
# implement reward variable to return reward to the AGENT
#       reward = 10 if apple eaten, 0 if not, -10 if died
# modify the play_step() function such that it take 'action' variable rather than keyboard input
#       in play_step(), 'action' variable will update 'direction'
# create sef.game_iteration variable to keep track of game progress w.r.t. time
# modify _is_collision helper function to check for collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 155, 155)
RED = (200, 100, 100)
BLUE1 = (50, 0, 100)
BLUE2 = (100, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20


APPLE_AWARD = 10
DEATH_PENALTY = -10


class SnakeGameAI:

    def __init__(self, w=600, h=400, speed=500):
        self.w = w
        self.h = h
        self.speed = speed
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        # all these will be reseted when game starts
        self.direction = None
        self.head = None
        self.snake = None
        self.score = None
        self.food = None
        self.frame_iteration = None
        # initial reset
        self.reset()

    def reset(self):
        # this is original game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        # 0. update the iteration of the game
        self.frame_iteration += 1
        # 1. use AGENT 'action' to change direction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        # _move will update the new head
        self._move(action)
        # insert new head to the snake
        self.snake.insert(0, self.head)
        # NOTE: later, if no food was eaten, snake's last will be pop()ed

        # 3. check if game over
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            # return:
            # 1. DEATH_PENALTY
            # 2. game_over is TRUE
            # 3. the score
            return DEATH_PENALTY, True, self.score

        # 4. place new food or just move
        if self.head == self.food:
            reward = APPLE_AWARD
            self.score += 1
            self._place_food()  # if food was eaten, we do not pop last part of snake's body
        else:
            reward = 0
            self.snake.pop()  # if no food was eaten, we pop the last part of the snake's body

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.speed)
        # 6. return game over and score
        return reward, False, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        pygame.draw.circle(self.display, RED,
                           [self.food.x + BLOCK_SIZE//2, self.food.y+BLOCK_SIZE//2],
                           BLOCK_SIZE // 1.7)
        # pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # action is [1,0,0] or [0,1,0] or [0,0,1]
        # action can take [keep_straight, turn_right, turn_left]
        # we use the action variable to update direction:
        right_turn = {Direction.RIGHT: Direction.DOWN, Direction.DOWN: Direction.LEFT,
                      Direction.LEFT: Direction.UP, Direction.UP: Direction.RIGHT}
        left_turn = {Direction.RIGHT: Direction.UP, Direction.DOWN: Direction.RIGHT,
                     Direction.LEFT: Direction.DOWN, Direction.UP: Direction.LEFT}

        # update direction based on action
        if action == [1, 0, 0]:
            new_dir = self.direction
        elif action == [0, 1, 0]:
            new_dir = right_turn[self.direction]
        else:
            new_dir = left_turn[self.direction]
        self.direction = new_dir
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


