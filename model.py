import torch
import torch.nn as nn
import torch.nn.functional as F
from bomber_env import BomberWrapper

class BomberModel(nn.Module):

    def __init__(self, channels, n, m, action_space_n):
        super().__init__()

        input_size = n * m * channels

        self.feature_extractor = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU()
        )

        self.actor = nn.Sequential(
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, action_space_n)
        )

        self.critic = nn.Sequential(
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, observation: torch.Tensor):
        print("Obs shape:", observation.shape)
        x = observation.flatten()  # spłaszcza całość do [572]
        x = x.unsqueeze(0)         # dodaje batch dim -> [1, 572]
        features = self.feature_extractor(x)
        logits = self.actor(features)
        value = self.critic(features)
        return logits.squeeze(0), value.squeeze(0)

