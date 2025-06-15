import numpy as np
import random
from classes.agent import Agent

# 0 - path, 1 - player, 2 - perm_wall, 3 - wall, 4 - bomb_animation, 5 - second player

# Ideas:

# generate score after each game, so I can evaluate each attempt

# dwóch agentów (2 różne strategie)

class BomberGame:
    
    def __init__(self, walls = 40):
        
        self.walls = walls
        self.agent_1 = Agent(start_pos=[0, 0], player_number=1)
        self.agent_5 = Agent(start_pos=[10, 12], player_number=5)
        self.map = np.zeros((11, 13), dtype=int)
        self.bombs = []
    
    def generate_map(self):
        
        # player
        
        self.map[0][0] = 1 
        self.map[10][12] = 5
        
        # perm walls 
        
        for row in range(11):
            for col in range(13):
                if (row % 2 != 0 and col % 2 != 0):
                    
                    self.map[row][col] = 2
                    
        # walls
        
        while np.count_nonzero(self.map == 3) != self.walls:
            
                row = random.randint(0, 10)
                col = random.randint(0, 12)
                
                if not ((row % 2 != 0 and col % 2 != 0) or (row in [0, 1, 9, 10] and col in [0, 1, 11, 12])):
                    
                    if self.map[row, col] == 0:
                        self.map[row, col] = 3
                    
        
        
        return self.map

    def step(self, move):
    
        self.agent_1.update_position(move, self.map)
        self.agent_5.update_position(random.choice(["w", "s", "d", "a", "n"]), self.map) # n - nothing
        
        return self.update_bombs()
        
        
    
    def update_bombs(self):
        
        are_players_alive = True

        for bomb in self.agent_1.bomb_list[:]:
            if bomb.tick():
                self.agent_1.bomb_list.remove(bomb)
                result = self.explode_bomb(bomb)
                if not result:
                    are_players_alive = False
        
        for bomb in self.agent_5.bomb_list[:]:
            if bomb.tick():
                self.agent_5.bomb_list.remove(bomb)
                result = self.explode_bomb(bomb)
                if not result:
                    are_players_alive = False

        return are_players_alive
            
    def explode_bomb(self, bomb):  # return False if player is dead

        x, y = bomb.position
        bomb_power = bomb.bomb_power
        
        are_players_alive = True

        max_rows, max_cols = self.map.shape


        if [x, y] in [self.agent_1.position, self.agent_5.position]:
            
            self.map[x][y] = 4
            are_players_alive = False
            
        else:
            self.map[x][y] = 4


        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            for i in range(1, bomb_power + 1):
                nx = x + dx * i
                ny = y + dy * i

                if not (0 <= nx < max_rows and 0 <= ny < max_cols):
                    break

                if [nx, ny] in [self.agent_1.position, self.agent_5.position]:
                    
                    are_players_alive = False

                tile = self.map[nx, ny]

                if tile == 2:
                      
                    break
                
                elif tile == 3:
                     
                    self.map[nx, ny] = 4
                    break
                
                else:
                    self.map[nx, ny] = 4

        return are_players_alive 
     
    def clean_animations(self):
        
        for row in range(11):
            for col in range(13):
                if self.map[row, col] == 4:
                    
                    self.map[row, col] = 0
        