import arcade.key
from random import randint,random
import time


class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self.is_select = False

        super().__init__(*args, **kwargs)

    def select(self):
        self.is_select = True

    def unselect(self):
        self.is_select = False

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y

class Rocket(arcade.AnimatedTimeSprite):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self.health = 1000

    def update(self):
        self.update_animation()

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

        self.rocket = None
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
        self.rocket.update()
        # self.rocket.update_animation()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            pass
