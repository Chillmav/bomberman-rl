import pygame
import torch
from classes.bomber_game import BomberGame
import torch.nn.functional as F
from torch.distributions import Categorical
from utils.images import (
    bomb_cv_player_1_img, bomb_cv_player_5_img,
    player_1, player_5,
    explosion, breakable, unbreakable
)
from utils.black_to_brows import replace_black_with_brown
from utils.shortest_path import shortest_path
from model import BomberModel
from bomber_env import BomberWrapper

pygame.init()
screen = pygame.display.set_mode((520, 440))
clock = pygame.time.Clock()
running = True


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

# --- Funkcja rysująca mapę ---
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

# --- Inicjalizacja gry i modelu ---
game = BomberGame()
env = BomberWrapper(game)
game.generate_map()
game.dist = shortest_path(game.agent_1.position, game.agent_5.position, game.map)


model = BomberModel(channels=4, n=11, m=13, action_space_n=6)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

action_map = ['w', 'a', 's', 'd', 'f', 'x']

# --- Główna pętla ---
while running:
    screen.fill([244, 164, 96])
    draw_game(game.map, game)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Pobranie obserwacji z wrappera ---
    observation = env.get_observation()

    # --- Przewidywanie: logits + value ---
    logits, value = model(observation)
    print("Logits:", logits)
    print("Value:", value)
    dist = Categorical(logits=logits)
    action = dist.sample()
    log_prob = dist.log_prob(action)

    action_str = action_map[action.item()]

    # --- Wykonaj akcję ---
    obs_next, reward, done = env.step(action_str)

    # --- Liczenie wartości docelowej i strat ---
    target_value = torch.tensor([reward], dtype=torch.float32)
    advantage = target_value - value.detach()

    critic_loss = F.mse_loss(value, target_value)
    actor_loss = -log_prob * advantage
    loss = actor_loss + critic_loss

    # --- Trening ---
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if not done:
        env.reset()

    clock.tick(5)
    pygame.display.flip()
pygame.quit()
