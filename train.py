import random
import pygame
import torch
import torch.nn.functional as F
from torch.distributions import Categorical
import numpy as np
from classes.bomber_game import BomberGame
from bomber_env import BomberWrapper
from model import BomberModel
from utils.images import bomb_cv_player_1_img, bomb_cv_player_5_img, player_1, player_5, explosion, breakable, unbreakable
from utils.black_to_brows import replace_black_with_brown
from utils.shortest_path import shortest_path


GAMMA = 0.90
ENTROPY_COEF = 0.01
MAX_EPISODES = 10000  
BATCH_SIZE = 128      
LR = 0.0005           
EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 0.9995    

epsilon = EPS_START

env = BomberWrapper(BomberGame())
model = BomberModel(channels=4, n=11, m=13, action_space_n=6)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
action_map = ['w', 'a', 's', 'd', 'f', 'x']


episode_rewards = []
batch_losses = []


for episode in range(MAX_EPISODES):
    state = env.reset()
    episode_reward = 0
    done = False
    
    while not done:

        if random.random() < epsilon:
            action = random.randint(0, 5)
            action_str = action_map[action]
        else:
            with torch.no_grad():
                logits, _ = model(state)
                action = torch.argmax(logits).item()
                action_str = action_map[action]

        next_state, reward, done = env.step(action_str)
        
 
        env.remember(state, action, reward, next_state, done)
        episode_reward += reward
        

        if len(env.memory) > BATCH_SIZE:
            batch = random.sample(env.memory, BATCH_SIZE)
            
            states = torch.stack([s[0].squeeze(0) for s in batch])
            actions = torch.tensor([s[1] for s in batch])
            rewards = torch.tensor([s[2] for s in batch], dtype=torch.float32)
            next_states = torch.stack([s[3].squeeze(0) for s in batch])
            dones = torch.tensor([s[4] for s in batch], dtype=torch.float32)
            

            rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-7)
            

            logits, values = model(states)
            dists = Categorical(logits=logits)
            log_probs = dists.log_prob(actions)
            entropies = dists.entropy()

            with torch.no_grad():
                _, next_values = model(next_states)
                targets = rewards + GAMMA * next_values.squeeze() * (1 - dones)
                advantages = targets - values.squeeze()

            critic_loss = F.mse_loss(values.squeeze(), targets)
            actor_loss = -(log_probs * advantages.detach()).mean() - ENTROPY_COEF * entropies.mean()
            loss = actor_loss + critic_loss
            

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()
            
            batch_losses.append(loss.item())
        
        state = next_state
        epsilon = max(EPS_END, epsilon * EPS_DECAY)
    
    episode_rewards.append(episode_reward)
    

    if episode % 100 == 0:
        avg_reward = np.mean(episode_rewards[-100:])
        print(f"Episode {episode}, Avg Reward (last 100): {avg_reward:.2f}, Epsilon: {epsilon:.3f}")
        

        if episode % 1000 == 0:
            torch.save(model.state_dict(), f"bomberman_model_{episode}.pth")


torch.save(model.state_dict(), "bomberman_model_final.pth")
