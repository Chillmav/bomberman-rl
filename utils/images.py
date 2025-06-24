import cv2 


# windows paths

bomb_cv_player_1_img = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\bomb_player_1.png"), (40, 40)), cv2.COLOR_BGR2RGB)
bomb_cv_player_5_img = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\bomb_player_5.png"), (40, 40)), cv2.COLOR_BGR2RGB)
player_1 = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\player_1.png"), (40, 40)), cv2.COLOR_BGR2RGB)
player_5 = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\player_5.png"), (40, 40)), cv2.COLOR_BGR2RGB)
explosion = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\explosion.png"), (40, 40)), cv2.COLOR_BGR2RGB)
unbreakable = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\unbreakable.png"), (40, 40)), cv2.COLOR_BGR2RGB)
breakable = cv2.cvtColor(cv2.resize(cv2.imread("C:\\Users\\Kubus\\Desktop\\Bomberman\\images\\breakable.png"), (40, 40)), cv2.COLOR_BGR2RGB)

# linux paths

# bomb_cv_player_1_img = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/bomb_player_1.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# bomb_cv_player_5_img = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/bomb_player_5.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# player_1 = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/player_1.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# player_5 = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/player_5.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# explosion = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/explosion.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# unbreakable = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/unbreakable.png"), (40, 40)), cv2.COLOR_BGR2RGB)
# breakable = cv2.cvtColor(cv2.resize(cv2.imread("/home/chillmaw/Projects/bomberman-rl/images/breakable.png"), (40, 40)), cv2.COLOR_BGR2RGB)