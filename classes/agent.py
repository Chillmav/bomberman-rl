import numpy as np
from classes.bomb import Bomb

# 0 - wait, w - move up, s - move down, a - move left, d - move right, f - bomb

class Agent:
    
    def __init__(self, start_pos, bomb_power=2, player_number=int):
        
        self.position = start_pos
        self.bomb_power = bomb_power
        self.bomb_list = []
        self.player_number = player_number
        
    def action(self, move):
        
        row, col = self.position
        
        if move not in ["w", "s", "a", "d", "f"]:
            return self.position
        
        if move == "w":   
            return [row - 1, col]
        elif move == "s": 
            return [row + 1, col]
        elif move == "a":  
            return [row, col - 1]
        elif move == "d":  
            return [row, col + 1]
        elif move == "f": 
            return [row, col]
            
                    
    def update_position(self, move, game_map):
        
        new_position = self.action(move)
        max_row, max_col = game_map.shape
        bomb_positions = [tuple(bomb.position) for bomb in self.bomb_list]

        
        if (0 <= new_position[0] < max_row) and (0 <= new_position[1] < max_col) and move != "f" and tuple(new_position) not in bomb_positions:
            
            if game_map[new_position[0], new_position[1]] == 0:
                
                game_map[self.position[0], self.position[1]] = 0
                game_map[new_position[0], new_position[1]] = self.player_number
                
                self.position = new_position
                
                return True
            
            else:
                
                return False
        
        elif move == "f":
            
            game_map[self.position[0], self.position[1]] = self.player_number # player
            
            bomb = Bomb([self.position[0], self.position[1]])
            
            self.bomb_list.append(bomb)

            return True