class Bomb:
    
    def __init__(self, position, timer=4, bomb_power=2):
        
        self.position = position
        self.timer = timer
        self.bomb_power = bomb_power
        
    def tick(self):
        
        self.timer -= 1
        return self.timer == 0