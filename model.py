import torch
import torch.nn as nn
import torch.nn.functional as F

class BomberModel(nn.Module):
    def __init__(self, channels, n, m, action_space_n):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(channels, 32, kernel_size=3, padding=1), 
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),        
            nn.ReLU()
        )

        conv_out_dim = 64 * n * m  

        self.fc = nn.Sequential(
            nn.Linear(conv_out_dim, 256),
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

        if observation.dim() == 3: 
            x = observation.unsqueeze(0)  
        elif observation.dim() == 4:  
            x = observation
        elif observation.dim() == 5:  
            x = observation.squeeze(0)
        else:
            raise ValueError(f"Unexpected input dimension: {observation.dim()}")
        
        x = self.conv(x)
        x = x.view(x.size(0), -1) 
        features = self.fc(x)
        logits = self.actor(features)
        value = self.critic(features)
        return logits, value
