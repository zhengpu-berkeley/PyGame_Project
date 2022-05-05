import torch
import numpy as np
from modified_game_for_agent import SnakeGameAI, Direction, Point
from model import LinearQNet


PATH = './saved_model/model.pth'
BLOCK_SIZE = 20


class Agent:

    def __init__(self):
        self.model = LinearQNet(11, 256, 3)
        self.model.load_state_dict(torch.load(PATH))

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),
            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
        ]
        return np.array(state, dtype=int)

    def get_action(self, state):
        action = [0, 0, 0]
        torch_state = torch.tensor(state, dtype=torch.float)
        prediction = self.model(torch_state)
        choice = torch.argmax(prediction).item()
        action[choice] = 1
        return action


def PLAY():
    agent = Agent()
    game = SnakeGameAI(speed=25)
    game_over = False
    while not game_over:
        # getting the current state
        curr_state = agent.get_state(game)
        # predict and action based on current state
        action = agent.get_action(curr_state)
        # perform action and get new state
        reward, game_over, score = game.play_step(action)
        if game_over:
            print(f'Score: {score}')


if __name__ == '__main__':
    PLAY()
