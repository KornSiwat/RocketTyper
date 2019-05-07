import arcade.key
from random import randint,choice
import time
import string

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
    def __init__(self, x, y, word='',target=0, damage=10,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_texture(arcade.load_texture('images/missile.png'))
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.target = target - 10
        self.distance = 60
        self.word = Word(self.right , self.center_y - 5, word)
        self.first_alphabet = ord(self.word.char_list[0].char)
        self._select = False
        self.active = True
        self.hit = True
        self.damage = damage
        self.length = self.right + 10 * len(self.word.char_list)

    def is_select(self):
        return self._select

    def explode(self):
        self.active = False
        self._select = False

    def draw_with_word(self):
        self.draw()
        self.word.draw()

    def update_pos(self):
        if self.left >= self.target:
            self.center_x -= 0.5
            self.word.update_pos(self.center_x + self.distance)
            self.check_word()
        else:
            self.explode()

    def update_key(self, key):
        self.word.update_key(key)

    def check_word(self):
        if self.word.is_select() == True:
            self._select = True
        if self.word.is_completed() == True:
            self.hit = False
            self.explode()

    def is_active(self):
        return self.active

    def get_damage(self):
        if self.hit == True:
            return self.damage
        return 0

class Word():
    def __init__(self,x ,y, word):
        self.x = x
        self.y = y
        self.char_list = list(map(lambda x: Char(x), word))
        self.current_char = self.char_list[0]
        self.complete = False
        self._select = False

    def draw(self):
        for index, elem in enumerate(self.char_list):
            arcade.draw_text(str(elem.char),self.x + 10 * index, self.y, elem.color, font_size=16)

    def update_pos(self, new_x):
        self.x = new_x

    def update_key(self, key):
        for char in self.char_list:
            if char.active == True:
                self.current_char = char
                break
        else:
            self.complete = True
        self.check_key(key)

    def check_key(self, key):
        if key == ord(self.current_char.char):
            self.current_char.is_typed()
            self._select = True

    def is_select(self):
        return self._select

    def is_completed(self):
        return self.complete

    def print_word(self):
        for char in self.char_list:
            print(char)

class Char():
    def __init__(self,char):
        self.char = char
        self.color = arcade.color.WHITE
        self.active = True    

    def is_typed(self):
        self.color = arcade.color.RED
        self.active = False

    def __str__(self):
        return self.char

class MissileManager():
    def __init__(self, width, height, target, difficulty=0, missile_height=100):
        self.attack_zone_x = [target, width]
        self.attack_zone_y = [150, height]
        self.difficulty = difficulty
        self.slot_list = []
        for y_pos in range(self.attack_zone_y[1],200, -(missile_height)):
            self.slot_list.append(Slot(self.attack_zone_x, y_pos-50, target))
        self.word_list = None
        self.timer = time.time()
        self.wait_time = 3
        self.current_slot = None

    def add_word_list(self, lst):
        self.word_list = lst

    def update(self, key):
        self.check_deploy_time()
        for slot in self.get_used_slot():
            slot.update_pos()
        if self.current_slot == None or self.current_slot.is_select() == False:
            for slot in self.get_used_slot():
                slot.update_key(key)
                if slot.is_select() == True:
                    self.current_slot = slot
                    break
        elif self.current_slot.is_use() == True:
            self.current_slot.update_key(key)

    def check_deploy_time(self):
        if time.time() - self.timer >= self.wait_time:
            self.deploy()
            self.timer = time.time()

    def deploy(self):
        if self.have_free_slot() == True:
            choice(self.get_free_slot()).create_missile(choice(self.word_list[choice([x for x in self.word_list])]))

    def get_free_slot(self):
        return [slot for slot in self.slot_list if slot.is_use() == False]

    def get_used_slot(self):
        return [slot for slot in self.slot_list if slot.is_use() == True]

    def have_free_slot(self):
        for slot in self.slot_list:
            if slot.is_use() == False:
                return True
        return False

class Slot():
    def __init__(self, x, y, target):
        self._in_use = False
        self._select = False
        self.x_points = x
        self.y_pos = y
        self.missile = None
        self.wait_pixel = 0
        self.target = target
        self.damage = 0

    def create_missile(self, word):
        self.missile = Missile(self.x_points[1], self.y_pos, word=word, target=self.target)
        self._in_use = True

    def draw(self):
        if self.missile != None:
            self.missile.draw_with_word()
            if self.missile.active == False:
                self.missile = None

    def update_pos(self):
        self.missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        self.missile.update_key(key)

    def is_use(self):
        return self._in_use

    def is_select(self):
        return self._select

    def check_missile_status(self):
        if self.missile.is_select() == True:
            self._select = True
        if self.missile.is_active() == False:
            self.delete_missile()

    def delete_missile(self):
        self.damage += self.missile.get_damage()
        self.missile = None
        self._in_use = False
        self._select = False

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

class WordManager():
    def __init__(self, word_dict):
        self._used = []
        self._unused = []
        self._long_word = dict()
        self._short_word = dict()
        for alphabet in word_dict:
            self._short_word[alphabet] = []
            self._long_word[alphabet] = []
            for word in word_dict[alphabet]:
                if len(word) >= 5:
                    self._long_word[alphabet].append(word)
                else:
                    self._short_word[alphabet].append(word)

    def _get_short(self):
        self._result = dict()
        for alphabet in self._unused:
            self._result[alphabet] = self._short_word[alphabet]
        return self._result

    def _get_long(self):
        self._result = dict()
        for alphabet in self._unused:
            self._result[alphabet] = self._short_word[alphabet]
        return self._result

    def generate(self):
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
        self.type = None

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
        self.missile_manager.update(self.type)
        self.type = 0

    def any_selected(self):
        for slot in self.missile_manager.slot_list:
            if slot.missile != None:
                if slot.missile.selected == True:
                    return True
        return False

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            if self.is_started():
                self.freeze()
            else:
                self.start()
        else:
            self.type = key
            print(self.type)
