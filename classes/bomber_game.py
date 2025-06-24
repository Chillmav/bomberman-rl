import numpy as np
import random
from classes.agent import Agent
from collections import deque
from utils.shortest_path import shortest_path

# 0 - path, 1 - player, 2 - perm_wall, 3 - wall, 4 - bomb_animation, 5 - second player

class BomberGame:
    
    def __init__(self, walls=40):
        
        self.walls = walls
        self.agent_1 = Agent(start_pos=[0, 0], player_number=1)
        self.agent_5 = Agent(start_pos=[10, 12], player_number=5)
        self.map = np.zeros((11, 13), dtype=int)
        self.bombs = []
        self.dist = None
        self.steps = 0
        self.max_steps = 150  
        self.timeout_penalty = -1 

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
        self.steps += 1
        
        bombs = self.agent_1.bomb_list + self.agent_5.bomb_list
        move_reward_agent_1 = self.agent_1.update_position(move, self.map, bombs)
        move_reward_agent_5 = self.agent_5.update_position(random.choice(["w", "s", "d", "a", "x"]), self.map, bombs)
        
        bombing_rewards = self.update_bombs()
        delayed_reward_1 = self.agent_1.collect_delayed_rewards(bombing_rewards[0])
        delayed_reward_5 = self.agent_5.collect_delayed_rewards(bombing_rewards[1])
        death_reward_5 = self.death_check(self.agent_5)
        death_reward_1 = self.death_check(self.agent_1)
        safe_reward_1 = self.bomb_safety_reward(self.agent_1)
        safe_reward_5 = self.bomb_safety_reward(self.agent_5)
        self.dist, dist_reward = self.distance_reward(self.dist)


        timeout = self.steps >= self.max_steps
        done, draw_penalty = self.players_check()
        
        if timeout and not done:
            done = True
            print(f"Game timeout after {self.max_steps} steps")

            timeout_penalty = self.timeout_penalty
        else:
            timeout_penalty = 0


        reward = (
            delayed_reward_1 * 5 +
            move_reward_agent_1 * 2 +
            death_reward_1 * 5 +
            dist_reward * 3 + 
            safe_reward_1 * 5 +
            draw_penalty + 
            timeout_penalty +  
            0.01,  
            

            delayed_reward_5 + move_reward_agent_5 + death_reward_5 + safe_reward_5 - 0.01
        )

        return self.map, reward, done
        
    
    def update_bombs(self):

        rewards = [0, 0]
        max_rows, max_cols = self.map.shape
        if any(bomb.owner == 1 for bomb in self.agent_1.bomb_list):
            rewards[0] -= 0.2  
    
        def handle_player_hit(px, py, bomb):

            self.map[px][py] = 4

            if [px, py] == self.agent_1.position:
                self.agent_1.position = [-1, -1]
                if bomb.owner == 5:
                    rewards[1] += 2.0  
                else:
                    rewards[0] -= 2.0  

            elif [px, py] == self.agent_5.position:
                
                self.agent_5.position = [-1, -1]
                if bomb.owner == 1:
                    rewards[0] += 1.0  
                else:
                    rewards[1] -= 0.5


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
                            rewards[0] += 0.1
                            self.map[nx, ny] = 4
                            break
                        else:
                            self.map[nx, ny] = 4


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
        is_player_1_alive = self.agent_1.position != [-1, -1]
        is_player_5_alive = self.agent_5.position != [-1, -1]

        if not is_player_1_alive or not is_player_5_alive:
            if not is_player_1_alive and not is_player_5_alive:
                print("Game over - draw")
                return True, -2 
            elif not is_player_1_alive:
                print("Game over - player 5 won")
                return True, 0
            else:
                print("Game over - player 1 won")
                return True, 0
        return False, 0  
    
    def death_check(self, player):
        if player.position == [-1, -1]:
            if player == self.agent_1 and any(bomb.owner == 1 for bomb in self.agent_1.bomb_list):
                return -10  
            return -5  
        return 0
        
    def distance_reward(self, prev_dist):

        if self.agent_1.position == [-1, -1] or self.agent_5.position == [-1 , -1]:
            
            return 0, 0
        
        new_dist = shortest_path(self.agent_1.position, self.agent_5.position, self.map)

        if new_dist < prev_dist:
            return new_dist, 0.002
        elif new_dist > prev_dist:
            return new_dist, -0.002
        else:
            return new_dist, 0
        
    def bomb_safety_reward(self, agent: Agent):
        danger_level = 0
        for bomb in self.agent_1.bomb_list + self.agent_5.bomb_list:
            dist = abs(agent.position[0] - bomb.position[0]) + abs(agent.position[1] - bomb.position[1])
            if dist <= bomb.bomb_power:
                danger_level += (bomb.bomb_power - dist + 1) * 0.2  
        
        if danger_level > 0:
            return -danger_level 
        return 0.05  