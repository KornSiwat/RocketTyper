import arcade.key
from random import randint,random
import time

DOT_RADIUS = 40

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y

class Rocket(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.health = 1000

    def update(self):
        pass
        
    def top_y(self):
        return self.y + (DOT_RADIUS // 2)

    def bottom_y(self):
        return self.y - (DOT_RADIUS // 2)

    def die(self):
        if self.health <= 0:
            return True
        return False

class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rocket = Rocket(self, 0, 120)
        self.score = 0

        self.state = World.STATE_FROZEN

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN     

    def is_started(self):
        return self.state == World.STATE_STARTED

    def update(self, delta):
        if self.state == World.STATE_FROZEN:
            return
        self.rocket.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            pass
