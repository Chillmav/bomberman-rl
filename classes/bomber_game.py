import numpy as np
import random
from classes.agent import Agent
from collections import deque
from utils.shortest_path import shortest_path

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
        self.dist = None

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
        
        bombs = self.agent_1.bomb_list + self.agent_5.bomb_list

        move_reward_agent_1 = self.agent_1.update_position(move, self.map, bombs)
        move_reward_agent_5 = self.agent_5.update_position(random.choice(["w", "s", "d", "a", "x"]), self.map, bombs) # x - nothing
        
        bombing_rewards = self.update_bombs()

        delayed_reward_1 = self.agent_1.collect_delayed_rewards(bombing_rewards[0])
        delayed_reward_5 = self.agent_5.collect_delayed_rewards(bombing_rewards[1])

        death_reward_5 = self.death_check(self.agent_5)
        death_reward_1 = self.death_check(self.agent_1)

        self.dist, dist_reward = self.distance_reward(self.dist)

        reward = delayed_reward_1 + move_reward_agent_1 + death_reward_1 + dist_reward, delayed_reward_5 + move_reward_agent_5 + death_reward_5 + dist_reward
        print(reward)


        # return observation, reward, done, info
        return self.map, reward, self.players_check()
        
    
    def update_bombs(self):

        rewards = [0, 0]
        max_rows, max_cols = self.map.shape

        def handle_player_hit(px, py, bomb):

            self.map[px][py] = 4

            if [px, py] == self.agent_1.position:

                self.agent_1.position = [-1, -1] 

                if bomb.owner == 5:
                    rewards[1] += 50

                else:
                    rewards[0] -= 50

            elif [px, py] == self.agent_5.position:

                self.agent_5.position = [-1, -1]

                if bomb.owner == 1:

                    rewards[0] += 50

                else:

                    rewards[1] -= 50

        # Process agent_1's bombs
        for bomb in self.agent_1.bomb_list[:]:

            if bomb.tick():

                self.agent_1.bomb_list.remove(bomb)

                x, y = bomb.position
                bomb_power = bomb.bomb_power

                if [x, y] == self.agent_1.position or [x, y] == self.agent_5.position:
                    handle_player_hit(x, y, bomb)
                else:
                    self.map[x][y] = 4


                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for dx, dy in directions:
                    for i in range(1, bomb_power + 1):
                        nx = x + dx * i
                        ny = y + dy * i

                        if not (0 <= nx < max_rows and 0 <= ny < max_cols):
                            break

                        if [nx, ny] == self.agent_1.position or [nx, ny] == self.agent_5.position:
                            handle_player_hit(nx, ny, bomb)

                        tile = self.map[nx, ny]

                        if tile == 2:
                            break
                        elif tile == 3:
                            rewards[0] += 5
                            self.map[nx, ny] = 4
                            break
                        else:
                            self.map[nx, ny] = 4

        # Process agent_5's bombs
        for bomb in self.agent_5.bomb_list[:]:

            if bomb.tick():

                self.agent_5.bomb_list.remove(bomb)

                x, y = bomb.position
                bomb_power = bomb.bomb_power

                if [x, y] == self.agent_1.position or [x, y] == self.agent_5.position:

                    handle_player_hit(x, y, bomb)

                else:
                    
                    self.map[x][y] = 4

                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for dx, dy in directions:
                    for i in range(1, bomb_power + 1):

                        nx = x + dx * i
                        ny = y + dy * i

                        if not (0 <= nx < max_rows and 0 <= ny < max_cols):
                            break

                        if [nx, ny] == self.agent_1.position or [nx, ny] == self.agent_5.position:
                            handle_player_hit(nx, ny, bomb)

                        tile = self.map[nx, ny]

                        if tile == 2:
                            break

                        elif tile == 3:
                            rewards[1] += 5
                            self.map[nx, ny] = 4
                            break

                        else:
                            self.map[nx, ny] = 4

        return rewards



     
    def clean_animations(self):
        
        for row in range(11):
            for col in range(13):
                if self.map[row, col] == 4:
                    
                    self.map[row, col] = 0

    def players_check(self):

        is_player_1_alive = False
        is_player_5_alive = False
        game_in_progress = True

        for row in range(11):
            for col in range(13):
                if self.map[row, col] == 1:
                    is_player_1_alive = True
                elif self.map[row, col] == 5:
                    is_player_5_alive = True

        if False in [is_player_1_alive, is_player_5_alive]:

            if (is_player_1_alive == False and is_player_5_alive == True):
                result = "player 5 won"
            elif (is_player_1_alive == True and is_player_5_alive == False):
                result = "player 1 won"
            elif (is_player_1_alive == False and is_player_5_alive == False):
                result = "both players lost"

            print(f"game over, {result}")
            game_in_progress = False

        return game_in_progress
    
    def death_check(self, player):

        if player.position == [-1, -1]:
            return -50
        else:
            return 0
        
    def distance_reward(self, prev_dist):

        if self.agent_1.position == [-1, -1] or self.agent_5.position == [-1 , -1]:
            
            return 0, 0
        
        new_dist = shortest_path(self.agent_1.position, self.agent_5.position, self.map)

        return new_dist, prev_dist - new_dist