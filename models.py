import arcade.key
from random import randint,choice
import time
import string

SPEED = 7

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self._selected = False

        super().__init__(*args, **kwargs)

    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False

    def is_selected(self):
        return self._selected

class Cloud(arcade.Sprite):
    INSTANCE_NUMBER = 0

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._screen_height = height
        self._screen_width = width
        self._speed = SPEED
        self.center_x = randint(0, self._screen_width)
        self.center_y = self._screen_height + (self.INSTANCE_NUMBER * 300)

        Cloud.INSTANCE_NUMBER += 1

    def update(self):
        self.center_y -= self._speed
        if self.out_of_screen():
            self.reuse()

    def out_of_screen(self):
        if self.center_y + 47 < 0:
            return True
        return False

    def reuse(self):
        self.center_x = randint(100, self._screen_width)
        self.center_y = self._screen_height + 300

class Rocket(arcade.AnimatedTimeSprite):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self._health = 1000
        self._ready = False
        self._speed = SPEED

    def update(self):
        self.update_animation()
        if self._ready == False:
            self.move_up()

    def get_health(self):
        return self._health

    def ready(self):
        self._ready = True

    def die(self):
        if self._health <= 0:
            return True
        return False

    def move_up(self):
        self.center_y += self._speed

    def move_down(self):
        self.center_y -= self._speed

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
    def __init__(self, width, height, target=0, level=0, missile_height=100):
        self._target = target
        self._attack_zone_x = [target, width]
        self._attack_zone_y = [150, height]
        self._level = level
        self._slot_list = []
        for y_pos in range(self._attack_zone_y[1],200, -(missile_height)):
            self._slot_list.append(Slot(self._attack_zone_x, y_pos-50, self._target))
        self._timer = time.time()
        self._wait_time = 3
        self._current_slot = None

    def add_word_manager(self, path):
        self._word_manager = WordManager(ReadWordFile(path).get_list())
    
    def draw(self):
        for slot in self._slot_list:
            slot.draw()

    def update(self, key):
        self._check_deploy_time()
        for slot in self._get_used_slot():
            slot.update_pos()
        if self._current_slot == None or self._current_slot.is_select() == False:
            for slot in self._get_used_slot():
                slot.update_key(key)
                if slot.is_select() == True:
                    self._current_slot = slot
                    break
        elif self._current_slot.is_use() == True:
            self._current_slot.update_key(key)

    def _check_deploy_time(self):
        if time.time() - self._timer >= self._wait_time:
            self._deploy()
            self._timer = time.time()

    def _deploy(self):
        if self.have_free_slot() == True:
            choice(self._get_free_slot()).create_missile(self._word_manager.generate())

    def _get_free_slot(self):
        return [slot for slot in self._slot_list if slot.is_use() == False]

    def _get_used_slot(self):
        return [slot for slot in self._slot_list if slot.is_use() == True]

    def have_free_slot(self):
        for slot in self._slot_list:
            if slot.is_use() == False:
                return True
        return False

class Slot():
    def __init__(self, x, y, target):
        self._in_use = False
        self._select = False
        self._x_points = x
        self._y_pos = y
        self._missile = None
        self._wait_pixel = 0
        self._target = target
        self._damage = 0

    def create_missile(self, word):
        self._missile = Missile(self._x_points[1], self._y_pos, word=word, target=self._target)
        self._in_use = True

    def draw(self):
        if self._missile != None:
            self._missile.draw_with_word()
            if self._missile.active == False:
                self._missile = None

    def update_pos(self):
        self._missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        self._missile.update_key(key)

    def is_use(self):
        return self._in_use

    def is_select(self):
        return self._select

    def check_missile_status(self):
        if self._missile.is_select() == True:
            self._select = True
        if self._missile.is_active() == False:
            self.delete_missile()

    def delete_missile(self):
        self._damage += self._missile.get_damage()
        self._missile = None
        self._in_use = False
        self._select = False

class ReadWordFile():
    def __init__(self, file_name=''):
        with open(file_name, 'r') as Fin:
            self._raw_word = [x.strip() for x in Fin.readlines()]
        self._catagorized_word = {}
        for word in self._raw_word:
            if word[0].lower() not in self._catagorized_word:
                self._catagorized_word[word[0].lower()] = [word]
            else:
                self._catagorized_word[word[0].lower()].append(word)

    def get_list(self):
        return self._catagorized_word

class WordManager():
    def __init__(self, word_dict, level=1):
        self._level = level
        self._used = []
        self._unused = list(string.ascii_lowercase)
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
        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def _get_long(self):
        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def generate(self):
        alphabet = choice(self._unused)
        self._used.append(alphabet)
        self._unused.remove(alphabet)
        return choice(self._short_word[alphabet] + self._long_word[alphabet] * self._level)

    def recycle(self, alphabet):
        self._unused.append(alphabet)
        self._used.remove(alphabet)

class Component_list():
    def __init__(self):
        self._components = []

    def draw(self):
        if len(self._components) > 0:
            [component.draw() for component in self._components]

    def add_component(self, component):
        self._components.append(component)

    def update(self):
        if len(self._components) > 0:
            [component.update() for component in self._components]
            [component.update_animation() for component in self._components]


    def print_component(self):
        print(self._components)
        

class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height, cloud_amount=5):
        self._width = width
        self._height = height

        self._rocket = None
        self._score = 0
        self._altitude = 0
        self._ready = False

        self._state = World.STATE_FROZEN

        self._components = Component_list()
        self._cloud_amount = cloud_amount
        self._cloud_list = arcade.SpriteList()
        self._cloud_list.sprite_list = list(map(lambda x : Cloud(self._width, self._height), range(self._cloud_amount)))
        self._components.add_component(self._cloud_list)
        self._type = None

    def add_rocket(self, rocket):
        self._rocket = rocket

    def add_missile_manager(self, word_path):
        self._missile_manager = MissileManager(self._width, self._height, target=self._rocket.right)
        self._missile_manager.add_word_manager(word_path)

    def add_component(self, component):
        self._components.add_component(component)

    def add_cloud_texture(self, texture, scale=1):
        for cloud in self._cloud_list:
            cloud.textures.append(arcade.load_texture(texture,scale=scale))
            cloud.set_texture(0)

    def start(self):
        self._state = World.STATE_STARTED

    def freeze(self):
        self._state = World.STATE_FROZEN

    def check_start_pos(self):
        if self._rocket.center_y >= self._height//2:
            self.ready()
            self._rocket.ready()

    def ready(self):
        self._ready = True

    def is_started(self):
        return self._state == World.STATE_STARTED

    def draw(self):
        if self.is_started() == True:
            self._missile_manager.draw()
        if self._ready == True:
            self._components.draw()
        self._rocket.draw()
        arcade.draw_text(str(self._rocket.get_health()),
                        self._width - 60 ,
                        self._height - 30,
                        arcade.color.BLACK, 20)

    def update(self, delta):
        if self._state == World.STATE_FROZEN:
            return
        self._rocket.update()
        self._rocket.update_animation()
        self.check_start_pos()
        self._components.update()
        self._missile_manager.update(self._type)
        self._type = 0

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            if self.is_started():
                self.freeze()
            else:
                self.start()
        else:
            self._type = key