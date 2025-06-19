from classes.bomber_game import BomberGame
import numpy as np

class BomberWrapper:

    def __init__(self):

        self.game = BomberGame()
        self.action_space_n = 6
        self.reset()

    def reset(self):

        self.game.generate_map()
        self.game.agent_1.position = [0, 0]
        self.game.agent_5.position = [10, 12]
        self.game.dist = 0
        return self.get_observation()
    
    def step(self, action):

        self.game.clean_animations()
        obs_map, reward, done = self.game.step(action)
        obs = self.get_observation()

        return obs, reward[0], done

    def get_observation(self):

        obs = np.zeros((4, 11, 13), dtype=np.float32)


        # channel 1 - objects + players
        for x in range(11):
            for y in range(13):

                tile = self.game.map[x][y]
                if tile == 1:
                    obs[0, x, y] = 1  
                elif tile == 5:
                    obs[0, x, y] = 2  
                elif tile == 2:
                    obs[0, x, y] = 3  
                elif tile == 3:
                    obs[0, x, y] = 4  
                elif tile == 4:
                    obs[0, x, y] = 5 
        
        # channel 2 - bombs player 1:

        for bomb in self.game.agent_1.bomb_list:

            x, y = bomb.position
            obs[1, x, y] = 1
        
        # channel 3 - bombs player 5:

        for bomb in self.game.agent_5.bomb_list:

            x, y = bomb.position
            obs[2, x, y] = 1

        # channel 4 - bombs timer:

        for bomb in self.game.agent_5.bomb_list + self.game.agent_1.bomb_list:

            x, y = bomb.position

            obs[3, x, y] = bomb.timer / 3
        
        return obs

