import arcade.key
from random import randint,choice
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
        self.append_texture(arcade.load_texture('images/missile.png'))
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.target = target - 10
        self.distance = 60
        self.word = Word(self.right , self.center_y - 5, word)
        self.type = ''
        self.selected = False
        self.active = True
        self.length = self.right + 10 * len(self.word.char_list)

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
    def __init__(self, width, height, target, difficulty=0, missile_height=100):
        self.attack_zone_x = [target, width]
        self.attack_zone_y = [150, height]
        self.difficulty = difficulty
        self.slot_list = []
        for y_pos in range(self.attack_zone_y[1],200, -missile_height):
            self.slot_list.append(Slot(self.attack_zone_x, y_pos-50, target))
        self.word_list = None
        self.timer = time.time()

    def add_word_list(self, lst):
        self.word_list = lst

    def update(self):
        if time.time() - self.timer >= 5:
            self.deploy()
            self.timer = time.time()
        for slot in self.slot_list:
            slot.update()

    def deploy(self):
        choice([slot for slot in self.slot_list if slot.free == True]).create_missile('try')

class Slot():
    def __init__(self, x, y, target):
        self.free = True
        self.x_points = x
        self.y_pos = y
        self.missile = None
        self.wait_pixel = 0
        self.start_alphabet = ''
        self.target = target

    def create_missile(self, word):
        self.missile = Missile(self.x_points[1], self.y_pos, word=word, target=self.target)
        self.start_alphabet = word[0]
        self.free = False

    def draw(self):
        if self.missile != None:
            self.missile.draw_with_word()
            if self.missile.active == False:
                self.missile = None

    def update(self):
        if self.missile != None:
            self.missile.update()

class ReadWordFile():
    def __init__(self, file_name=''):
        with open(file_name, 'r') as Fin:
            self.raw_word = [x.strip() for x in Fin.readlines()]
        self.catagorized_word = {}
        for word in self.raw_word:
            if word[0].lower() not in self.catagorized_word:
                self.catagorized_word[word[0].lower()] = [word]
            else:
                self.catagorized_word[word[0].lower()].append(word)

    def get_list(self):
        return self.catagorized_word

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

    def add_missile_manager(self):
        self.missile_manager = MissileManager(self.width, self.height, target=0)

    def add_word_list(self, path):
        self.missile_manager.add_word_list(ReadWordFile(path).get_list())

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def check_start_pos(self):
        if self.rocket.center_y >= self.height//2:
            self.ready()
            self.rocket.ready()

    def ready(self):
        self.is_ready = True

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
        self.missile_manager.update()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            if self.is_started():
                self.freeze()
            else:
                self.start()

