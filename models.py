import arcade.key
from random import randint,random
import time

SPEED = 7

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self.is_select = False

        super().__init__(*args, **kwargs)

    def select(self):
        self.is_select = True

    def unselect(self):
        self.is_select = False

class Cloud(arcade.Sprite):
    INSTANCE_NUMBER = 0

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = SPEED
        self.center_x = randint(0, width)
        self.center_y = height + (self.INSTANCE_NUMBER * 10)

        

class Rocket(arcade.AnimatedTimeSprite):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self.health = 1000
        self.is_ready = False
        self.speed = SPEED

    def update(self):
        self.update_animation()
        if self.is_ready == False:
            self.move_up()

    def ready(self):
        self.is_ready = True

    def die(self):
        if self.health <= 0:
            return True
        return False

    def move_up(self):
        self.center_y += self.speed

    def move_down(self):
        self.center_y -= self.speed

class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.rocket = None
        self.score = 0
        self.altitude = 0
        self.is_ready = False

        self.state = World.STATE_FROZEN

        self.cloud_list = arcade.SpriteList()

    def start(self):
        self.state = World.STATE_STARTED

    def check_start_pos(self):
        if self.rocket.center_y >= self.height//2:
            self.ready()
            self.rocket.ready()

    def ready(self):
        self.is_ready = True

    def freeze(self):
        self.state = World.STATE_FROZEN     

    def is_started(self):
        return self.state == World.STATE_STARTED

    def update(self, delta):
        if self.state == World.STATE_FROZEN:
            return
        self.rocket.update()
        self.rocket.update_animation()
        self.check_start_pos()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            pass
