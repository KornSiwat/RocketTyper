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

class ModelSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class Rocket(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.health = 1000

    def update(self):
        pass

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

        self.rocket = Rocket(self, 200, 120)
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
        self.rocket.update_animation()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            pass
