
class Bomb:
    
    def __init__(self, position, timer=6, bomb_power=2, owner=int):
        
        self.position = position
        self.timer = timer
        self.bomb_power = bomb_power
        self.owner = owner
        
    def tick(self):
        
        self.timer -= 1
        return self.timer == 0