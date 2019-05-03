from models import MissileManager

a = MissileManager(1000, 700, 200)
for i in a.map:
    print(i.y_pos)