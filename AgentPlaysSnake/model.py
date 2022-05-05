import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class LinearQNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.Linear1 = nn.Linear(input_size, hidden_size)
        # self.Linearh = nn.Linear(hidden_size, hidden_size)
        self.Linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.Linear1(x))
        # x = F.relu(self.Linearh(x))
        x = self.Linear2(x)
        return x

    def save(self, file_name='model.pth'):
        folder = './saved_model'
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, game_over):
        # NOTE:
        # if running train_short_memory: each is a single variable
        # if running train_long_memory: each is a list of individual variables
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over,)

        pred = self.model(state)
        target = pred.clone()

        for sample_idx in range(len(game_over)):
            Qnew = reward[sample_idx]
            if not game_over[sample_idx]:
                Qnew = reward[sample_idx] + self.gamma * torch.max(self.model(next_state[sample_idx]))
            target[sample_idx][torch.argmax(action[sample_idx]).item()] = Qnew

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
