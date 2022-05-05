import torch
import numpy as np
import random
from collections import deque
from modified_game_for_agent import SnakeGameAI, Direction, Point
from model import LinearQNet, QTrainer
from plotting import plot

# a deque is a 'list' that's more efficient at: .append() .appendleft() .pop() .popleft()
# a deque also supports: .clear() .extend() .extendleft() *extendleft is in reverse order
# a deque also supports: .rotate()
# when specified max_len like: d = deque('hello', maxlen = 5)
# when more stuff appended to deque to exceed maxlen, originals are popped automatically
# the deque stores memory from games, with: maxlen = MAX_MEMORY
# this MAX_MEMORY global variable determines how many items to be stored
PURE_EXPLOIT = 80
BLOCK_SIZE = 20
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
GAMMA = 0.9


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness in chance to explore
        self.gamma = GAMMA  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

    def remember(self, state, action, reward, next_state, game_over):
        one_memory = (state, action, reward, next_state, game_over)
        self.memory.append(one_memory)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            samples = random.sample(self.memory, BATCH_SIZE)
        else:
            samples = self.memory
        states, actions, rewards, next_states, game_overs = zip(*samples)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = PURE_EXPLOIT - self.n_games
        action = [0, 0, 0]
        if self.epsilon > random.randint(0, 200):
            choice = random.randint(0, 2)
            action[choice] = 1
        else:
            torch_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(torch_state)
            choice = torch.argmax(prediction).item()
            action[choice] = 1
        return action


def TRAIN():
    plot_scores = []
    plot_mean_scores = []
    last_twenty = deque(maxlen=20)
    best_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # getting the current state
        curr_state = agent.get_state(game)
        # predict and action based on current state
        action = agent.get_action(curr_state)
        # perform action and get new state
        reward, game_over, score = game.play_step(action)
        new_state = agent.get_state(game)
        # train the agent
        agent.train_short_memory(curr_state, action, reward, new_state, game_over)
        # remember what we have done
        agent.remember(curr_state, action, reward, new_state, game_over)

        if game_over:
            # 0. reset the game
            # 1. train the 'long_memory'
            # 2. plot the result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            # check if we reached a new highest score
            if score > best_score:
                best_score = score
                agent.model.save()
            # print game number, the score, and the record
            print(f'Game Number: {agent.n_games} ; Score: {score} ; Record: {best_score}')
            plot_scores.append(score)
            last_twenty.append(score)
            mean_score = float(np.mean(last_twenty))
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    TRAIN()
