import pygame
from classes.bomber_game import BomberGame
from utils.images import bomb_cv_player_1_img, player_1, player_5, explosion, breakable, unbreakable, bomb_cv_player_5_img
from utils.black_to_brows import replace_black_with_brown
import numpy as np

pygame.init()

screen = pygame.display.set_mode((520, 440))

running = True

bomb_player_1_img = pygame.image.frombuffer(replace_black_with_brown(bomb_cv_player_1_img.copy()).tobytes(), bomb_cv_player_1_img.shape[1::-1], "RGB")
bomb_player_5_img = pygame.image.frombuffer(replace_black_with_brown(bomb_cv_player_5_img.copy()).tobytes(), bomb_cv_player_5_img.shape[1::-1], "RGB")
player_1_img = pygame.image.frombuffer(replace_black_with_brown(player_1.copy()).tobytes(), player_1.shape[1::-1], "RGB")
player_5_img = pygame.image.frombuffer(replace_black_with_brown(player_5.copy()).tobytes(), player_5.shape[1::-1], "RGB")
explosion_img = pygame.image.frombuffer(replace_black_with_brown(explosion.copy()).tobytes(), explosion.shape[1::-1], "RGB")
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
            obj = map[row, col]
            if int(obj) in img_dict:
                screen.blit(img_dict[int(obj)], (col * 40, row * 40))

    bombs_agent_1 = game.agent_1.bomb_list
    bombs_agent_5 = game.agent_5.bomb_list
    
    for bomb in bombs_agent_1:
        screen.blit(bomb_player_1_img, (bomb.position[1] * 40, bomb.position[0] * 40))
    
    for bomb in bombs_agent_5:
        screen.blit(bomb_player_5_img, (bomb.position[1] * 40, bomb.position[0] * 40))
        
game = BomberGame()
game.generate_map()

while running:
    
    screen.fill([244, 164, 96])
    draw_game(game.map, game)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            running = False
            
        if event.type == pygame.KEYDOWN:
                
            key_map = {
                pygame.K_w: "w",
                pygame.K_a: "a",
                pygame.K_s: "s",
                pygame.K_d: "d",
                pygame.K_f: "f"
            }

            move = key_map.get(event.key, "x")

            game.clean_animations()
            running = game.step(move)
            screen.fill([244, 164, 96])
            draw_game(game.map, game)
            pygame.display.flip() 

    
    
    
    pygame.display.flip()        
            
pygame.quit()