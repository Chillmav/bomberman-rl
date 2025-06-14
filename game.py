import numpy as np
import random
from agent import Agent
# 0 - path, 1 - player, 2 - perm_wall, 3 - wall, 4 - mob, 5 - bomb, 6 - bomb_animation, 7 - bomb + player

# Ideas:

# generate score after each game, so I can evaluate each attempt

# dwóch agentów (2 różne strategie)

class BomberGame:
    
    def __init__(self, game_time = 1, step_time = 1, walls = 30, mobs = 3):
        
        self.game_time = game_time
        self.step_time = step_time
        self.walls = walls
        self.agent = Agent(start_pos=[0, 0])
        self.map = np.zeros((11, 13), dtype=int)
        
    def generate_map(self):
        
        # player
        
        self.map[0][0] = 1 
        
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

    def step(self):
        
        move = input()

        return self.agent.update_position(move, self.map)

def main():
    
    game = BomberGame()
    game.generate_map()
    play = True
    
    while play:
        
        print(game.map)
        game.step()
        
        
    
main()