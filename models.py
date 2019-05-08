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
            self._reuse()

    def out_of_screen(self):
        if self.center_y + self.top < 0:
            return True
        return False

    def _reuse(self):
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
        self._active = True

    def update(self):
        self.update_animation()
        if self._ready == False:
            self._move_up()
        if self._active == False:
            self._move_down()
        self._check_dead()

    def update_health(self, damage):
        self._health -= damage

    def get_health(self):
        return self._health

    def ready(self):
        self._ready = True

    def _check_dead(self):
        if self._health <= 0:
            self._active = False

    def _move_up(self):
        self.center_y += self._speed

    def _move_down(self):
        self.center_y -= self._speed

class Missile(arcade.Sprite):
    def __init__(self, x, y, word='',target=0, damage=10,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_texture(arcade.load_texture('images/missile.png'))
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self._target = target - 10
        self._distance = 60
        self._word = Word(self.right , self.center_y - 5, word)
        self._first_alphabet = ord(self._word.get_current_char().get_char())
        self._selected = False
        self._active = True
        self._hit = True
        self._damage = damage
        self._speed = 0.5

    def is_selected(self):
        return self._selected

    def explode(self):
        self._active = False
        self._selected = False
        print('boom')

    def draw_with_word(self):
        self.draw()
        self._word.draw()

    def update_pos(self):
        if self.left >= self._target:
            self.center_x -= self._speed
            self._word.update_pos(self.center_x + self._distance)
            self.check_word()
        else:
            self.explode()

    def update_key(self, key):
        self._word.update_key(key)

    def check_word(self):
        if self._word.is_selected() == True:
            self._selected = True
        if self._word.is_completed() == True:
            self._hit = False
            self.explode()

    def is_active(self):
        return self._active

    def get_damage(self):
        if self._hit == True:
            return self._damage
        return 0

class Word():
    def __init__(self,x ,y, word):
        self._x = x
        self._y = y
        self._word = word
        self._char_list = list(map(lambda x: Char(x), word))
        self._current_char = self._char_list[0]
        self._completed = False
        self._selected = False

    def draw(self):
        white_text = self._word
        red_text = ''
        for char in self._char_list:
            if char.is_active()== True:
                red_text += ' '
            else:
                red_text += char.get_char()
        arcade.draw_text(white_text, self._x, self._y, color=arcade.color.WHITE, font_size=16)
        arcade.draw_text(red_text, self._x, self._y, color=arcade.color.RED, font_size=16)

    def update_pos(self, new_x):
        self._x = new_x

    def update_key(self, key):
        for char in self._char_list:
            if char.is_active() == True:
                self._current_char = char
                break
        else:
            self._completed = True
        self._check_key(key)

    def _check_key(self, key):
        if key == ord(self._current_char.get_char()):
            self._current_char.is_typed()
            self._selected = True

    def is_selected(self):
        return self._selected

    def is_completed(self):
        return self._completed

    def get_current_char(self):
        return self._current_char

    def print_word(self):
        for char in self._char_list:
            print(char)

class Char():
    def __init__(self,char):
        self._char = char
        self._active = True    

    def is_typed(self):
        self._active = False

    def is_active(self):
        return self._active

    def get_char(self):
        return self._char

    def __str__(self):
        return self._char

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
        self._damage = 0
        self._missile_count = 0

    def add_word_manager(self, path):
        self._word_manager = WordManager(ReadWordFile(path).get_list())
    
    def draw(self):
        for slot in self._slot_list:
            slot.draw()

    def update(self, key):
        self._check_deploy_time()
        self._update_pos()
        self._key_handle(key)
        self._update_damage()
        self._update_missile_count()

    def _update_pos(self):
        for slot in self._get_used_slot():
            slot.update_pos()

    def _key_handle(self,key):
        if self._current_slot == None or self._current_slot.is_selected() == False:
            for slot in self._get_used_slot():
                slot.update_key(key)
                if slot.is_selected() == True:
                    self._current_slot = slot
                    break
        elif self._current_slot.is_use() == True:
            self._current_slot.update_key(key)

    def _update_damage(self):
        for slot in self._slot_list:
            self._damage += slot.get_damage()
            slot.reset_damage()

    def _update_missile_count(self):
        for slot in self._slot_list:
            self._missile_count += slot.get_missile_count()
            slot.reset_missile_count()

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

    def get_damage(self):
        return self._damage

    def reset_damage(self):
        self._damage = 0 

    def get_missile_count(self):
        return self._missile_count
    
    def reset_missile_count(self):
        self._missile_count = 0

class Slot():
    def __init__(self, x, y, target):
        self._in_use = False
        self._selected = False
        self._x_points = x
        self._y_pos = y
        self._missile = None
        self._wait_pixel = 0
        self._target = target
        self._damage = 0
        self._missile_count = 0

    def create_missile(self, word):
        self._missile = Missile(self._x_points[1], self._y_pos, word=word, target=self._target)
        self._in_use = True

    def draw(self):
        if self._missile != None:
            self._missile.draw_with_word()
            if self._missile.is_active() == False:
                self._missile = None

    def update_pos(self):
        self._missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        self._missile.update_key(key)

    def is_use(self):
        return self._in_use

    def is_selected(self):
        return self._selected

    def check_missile_status(self):
        if self._missile.is_selected() == True:
            self._select = True
        if self._missile.is_active() == False:
            self.delete_missile()

    def delete_missile(self):
        self._damage += self._missile.get_damage()
        self._missile = None
        self._in_use = False
        self._selected = False
        self._missile_count += 1

    def get_damage(self):
        return self._damage

    def reset_damage(self):
        self._damage = 0

    def get_missile_count(self):
        return self._missile_count

    def reset_missile_count(self):
        self._missile_count = 0

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
    def __init__(self, word_dict, level=0):
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

    def increase_level(self):
        self._level += 1

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
        self._missile_count = 0
        self._time = 0
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
        self._start_time = time.time()

    def is_started(self):
        return self._state == World.STATE_STARTED

    def draw(self):
        if self.is_started() == True:
            self._components.draw()
            self._missile_manager.draw()
        # if self._ready == True:
        self._rocket.draw()
        self.draw_stat()

    def draw_stat(self):
        self._draw_rocket_health()
        self._draw_missile_count()

    def _draw_rocket_health(self):
        arcade.draw_text(str(self._rocket.get_health()),
                self._width//2 - 50, 30,
                arcade.color.BLACK, font_size=33)

    def _draw_missile_count(self):
        arcade.draw_text(str(f'Word: {self._missile_count}'),
                self._width//2 + 180, 25,
                arcade.color.BLACK, font_size=22)

    def update(self, delta):
        if self._state == World.STATE_FROZEN:
            return
        self._rocket.update()
        self._rocket.update_animation()
        self.check_start_pos()
        self._components.update()
        self._missile_manager.update(self._type)
        self._type = 0

    def update_missile_count(self):
        self._missile_count += self._missile_manager.get_missile_count()
        self._missile_manager.reset_missile_count()
    
    def update_health(self):
        self._rocket.update_health(self._missile_manager.get_damage())
        self._missile_manager.reset_damage()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            if self.is_started():
                self.freeze()
            else:
                self.start()
        else:
            self._type = key