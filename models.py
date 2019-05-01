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
        self.screen_height = height
        self.screen_width = width
        self.speed = SPEED
        self.center_x = randint(0, self.screen_width)
        self.center_y = self.screen_height + (self.INSTANCE_NUMBER * 300)

        Cloud.INSTANCE_NUMBER += 1

    def update(self):
        self.center_y -= self.speed
        if self.out_of_screen():
            self.reuse()

    def out_of_screen(self):
        if self.center_y + 47 < 0:
            return True
        return False

    def reuse(self):
        self.center_x = randint(100, self.screen_width)
        self.center_y = self.screen_height + 300

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

class Missile(arcade.Sprite):
    def __init__(self, x, y, word='',target=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self.target = target - 10
        self.distance = 60
        self.word = Word(self.center_x + self.distance , self.center_y - 5, word)
        self.type = ''
        self.selected = False
        self.active = True

    def explode(self):
        self.active = False

    def draw_with_word(self):
        self.draw()
        self.word.draw()

    def update(self):
        if self.left >= self.target:
            self.center_x -= 0.5
            self.word.update(self.center_x + self.distance)
        else:
            self.explode()

class Word():
    def __init__(self,x ,y, word):
        self.x = x
        print(self.x)
        self.y = y

        self.char_list = list(map(lambda x: Char(x), word))

    def draw(self):
        for index, elem in enumerate(self.char_list):
            arcade.draw_text(str(elem.char),self.x + 10 * index, self.y, elem.color, font_size=16)

    def update(self, new_x):
        self.x = new_x
        
    def print_word(self):
        for char in self.char_list:
            print(char)

class Char():
    def __init__(self,char):
        self.char = char
        self.color = arcade.color.WHITE
        self.active = True    

    def is_typed(self):
        self.color = arcade.color.GRAY
        self.active = False

    def __str__(self):
        return self.char

class MissileManager():
    def __init__(self, width, height, rocket_right=0):
        pass


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height, cloud_amount=5):
        self.width = width
        self.height = height

        self.rocket = None
        self.score = 0
        self.altitude = 0
        self.is_ready = False

        self.state = World.STATE_FROZEN

        self.cloud_amount = cloud_amount
        self.cloud_list = arcade.SpriteList()
        for _ in range(self.cloud_amount):
            self.cloud_list.append(Cloud(self.width, self.height))


    def start(self):
        self.state = World.STATE_STARTED

    def check_start_pos(self):
        if self.rocket.center_y >= self.height//2:
            self.ready()
            self.rocket.ready()
            self.missile_manager = MissileManager(self.width, self.height, self.rocket.right)

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
        for cloud in self.cloud_list:
            cloud.update()

    # def on_key_press(self, key, key_modifiers):
    #     if key == arcade.key.SPACE:
    #         pass
