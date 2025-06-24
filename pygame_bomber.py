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
import os
# --- Inicjalizacja PyGame ---

pygame.init()
screen = pygame.display.set_mode((520, 440))
clock = pygame.time.Clock()
running = True

# --- Ładowanie grafik ---

def load_image(img):
    return pygame.image.frombuffer(replace_black_with_brown(img.copy()).tobytes(), img.shape[1::-1], "RGB")

bomb_player_1_img = load_image(bomb_cv_player_1_img)
bomb_player_5_img = load_image(bomb_cv_player_5_img)
player_1_img = load_image(player_1)
player_5_img = load_image(player_5)
explosion_img = load_image(explosion)
breakable_img = pygame.image.frombuffer(breakable.tobytes(), breakable.shape[1::-1], "RGB")
unbreakable_img = pygame.image.frombuffer(unbreakable.tobytes(), unbreakable.shape[1::-1], "RGB")

img_dict = {
    1: player_1_img, 
    2: unbreakable_img,
    3: breakable_img,
    4: explosion_img,
    5: player_5_img
}

def draw_game(map, game):
    for row in range(11):
        for col in range(13):
            obj = int(map[row, col])
            if obj in img_dict:
                screen.blit(img_dict[obj], (col * 40, row * 40))

    for bomb in game.agent_1.bomb_list:
        screen.blit(bomb_player_1_img, (bomb.position[1] * 40, bomb.position[0] * 40))
    for bomb in game.agent_5.bomb_list:
        screen.blit(bomb_player_5_img, (bomb.position[1] * 40, bomb.position[0] * 40))


GAMMA = 0.99  
ENTROPY_COEF = 0.01 
MAX_EPISODES = 1000
BATCH_SIZE = 32
LR = 0.001

EPS_START = 1.0
EPS_END = 0.01
EPS_DECAY = 0.995
epsilon = EPS_START


env = BomberWrapper(BomberGame())
model = BomberModel(channels=4, n=11, m=13, action_space_n=6)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)
action_map = ['w', 'a', 's', 'd', 'f', 'x']


episode_rewards = []
batch_losses = []


MODEL_PATH = "bomberman_model_1000.pth"
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH))
    print(f"Loaded model from {MODEL_PATH}")
model.train()  




for episode in range(MAX_EPISODES):
    state = env.reset()
    episode_reward = 0
    done = False
    
    while not done:
        screen.fill([244, 164, 96])
        draw_game(env.game.map, env.game)
        pygame.display.flip()
        

        if model.training and random.random() < epsilon:

            action = random.randint(0, 5)
            action_str = action_map[action]
            action_to_store = action
        else:

            with torch.no_grad():
                logits, _ = model(state)
                if model.training:
                    dist = Categorical(logits=logits)
                    action = dist.sample()
                else:
                    action = torch.argmax(logits)
                action_str = action_map[action.item()]
                action_to_store = action.item()
        

        next_state, reward, done = env.step(action_str)
        

        if model.training:
            env.remember(state, action_to_store, reward, next_state, done)
        episode_reward += reward
        

        if model.training and len(env.memory) > BATCH_SIZE:
            batch = random.sample(env.memory, BATCH_SIZE)
            
            states = torch.stack([s[0].squeeze(0) for s in batch])
            actions = torch.tensor([s[1] for s in batch])
            rewards = torch.tensor([s[2] for s in batch], dtype=torch.float32)
            next_states = torch.stack([s[3].squeeze(0) for s in batch])
            dones = torch.tensor([s[4] for s in batch], dtype=torch.float32)
            

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
        

        if model.training:
            epsilon = max(EPS_END, epsilon * EPS_DECAY)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    

    episode_rewards.append(episode_reward)
    print(f"Episode {episode}, Reward: {episode_reward:.2f}, Avg Reward: {np.mean(episode_rewards[-10:]):.2f}")
    
    if env.game.steps >= env.game.max_steps:
        print(f"Episode {episode} ended by timeout after {env.game.steps} steps")
    else:
        print(f"Episode {episode} ended by player elimination")

