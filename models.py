import arcade.key
from random import randint,choice
import time
import string

SPEED = 7

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    ''' class for the menu choice sprite'''

    def __init__(self, *args, **kwargs):
        ''' create an attribute of MenuChoice instance'''

        super().__init__(*args, **kwargs)
        self._selected = False

    def select(self):
        ''' call when the choice is chosen '''
        self._selected = True

    def unselect(self):
        ''' call when the choice is not chosen'''
        self._selected = False

    def is_selected(self):
        ''' return the status whether the instance is being selected or not '''
        return self._selected

class Cloud(arcade.Sprite):
    ''' class for cloud element'''

    INSTANCE_NUMBER = 0

    def __init__(self, width, height, *args, **kwargs):
        ''' create attributes of cloud instance '''

        super().__init__(*args, **kwargs)
        self._screen_height = height
        self._screen_width = width
        self._speed = SPEED
        self.center_x = randint(0, self._screen_width)
        self.center_y = self._screen_height + (self.INSTANCE_NUMBER * 300)

        Cloud.INSTANCE_NUMBER += 1

    def update(self):
        ''' update the position of the cloud instance '''

        self.center_y -= self._speed
        if self.out_of_screen():
            self._reuse()

    def out_of_screen(self):
        ''' check the position of the cloud instance and return True if the cloud is out of the screen '''

        if self.center_y + self.top < 0:
            return True
        return False

    def _reuse(self):
        ''' call when the cloud instance is out of the screen to random the x position of the cloud and release it from the top of the screen '''

        self.center_x = randint(100, self._screen_width)
        self.center_y = self._screen_height + 300

class Rocket(arcade.AnimatedTimeSprite):
    ''' class for Rocket Sprite '''

    def __init__(self, x, y, *args, **kwargs):
        ''' create attributes of rocket instance '''

        super().__init__(*args, **kwargs)
        self.center_x = x
        self.center_y = y
        self._health = 100
        self._ready = False
        self._speed = SPEED
        self._active = True

    def update(self):
        ''' update the texture of the rocket and check the position and move it based on the current status '''

        self.update_animation()
        if self._ready == False:
            self._move_up()
        if self.is_over() == True and self._out_of_screen() == False:
            self._move_down()
        self._check_dead()

    def update_health(self, damage):
        ''' subtract the current health of the rocket with the damage parameter '''

        self._health -= damage

    def get_health(self):
        ''' return the current health of the rocket '''

        if self._active == True:
            return self._health
        else:
            return 0

    def is_over(self):
        ''' return the status of the rocket '''

        if self._active == False:
            return True
        else:
            return False

    def ready(self):
        ''' call when the rocket is at its ready position '''

        self._ready = True

    def _out_of_screen(self):
        ''' check the position of the rocket and returns true if it is in the screen else returns false '''

        if self.top > 0:
            return False
        return True

    def _check_dead(self):
        ''' check and update the active status of the rocket based on its health '''

        if self._health <= 0:
            self._active = False

    def _move_up(self):
        ''' move the rocket in upward direction '''

        self.center_y += self._speed

    def _move_down(self):
        ''' move the rocket in downward direction '''

        self.center_y -= self._speed

class Missile(arcade.Sprite):
    ''' class for Missile Sprite '''

    def __init__(self, x, y, word='',target=0, damage=10, speed=1, *args, **kwargs):
        ''' create attributes of missile instance '''

        super().__init__(*args, **kwargs)
        self.append_texture(arcade.load_texture('images/missile.png'))
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self._target = target - 10
        self._distance = 60
        self._first_alphabet = word[0]
        self._word = Word(self.right , self.center_y - 5, word)
        self._selected = False
        self._active = True
        self._hit = True
        self._damage = damage
        self._speed = speed

    def is_selected(self):
        ''' return the status whether the missile is being typed '''

        return self._selected

    def explode(self):
        ''' change the missile status to indicate that it is needed to be destroyed '''

        self._active = False
        self._selected = False

    def draw_with_word(self):
        ''' draw the missile sprite and the word attached to it '''

        self.draw()
        self._word.draw()

    def update_pos(self):
        ''' update the missile position '''

        if self.left >= self._target:
            self.center_x -= self._speed
            self._word.update_pos(self.center_x + self._distance)
            self.check_word()
        else:
            self.explode()

    def update_key(self, key):
        ''' pass in the pressed key to the word update function of word instance '''

        self._word.update_key(key)

    def check_word(self):
        ''' check if the word attached to the missile has been typed and also if it is completed '''

        if self._word.is_selected() == True:
            self._selected = True
        if self._word.is_completed() == True:
            self._hit = False
            self.explode()

    def is_active(self):
        ''' check and return if the missile is active or not '''

        return self._active

    def get_damage(self):
        ''' return the damage of the missile '''

        if self._hit == True:
            return self._damage
        return 0

    def get_first_alphabet(self):
        ''' return the first alphabet of the word attached to the missile '''

        return self._first_alphabet

class Word():
    ''' class for the word attached to the back of the missile '''

    def __init__(self,x ,y, word):
        ''' create attributes of Word instance '''

        self._x = x
        self._y = y
        self._word = word
        self._char_list = list(map(lambda x: Char(x), word))
        self._current_char = self._char_list[0]
        self._completed = False
        self._selected = False

    def draw(self):
        ''' draw the word on the screen with different color for the typed character and the untyped '''

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
        ''' update the posion of the text to be drawn '''

        self._x = new_x

    def update_key(self, key):
        ''' check if the active character matched with the key parameter by using check_key function and also check if the word is completed '''

        for char in self._char_list:
            if char.is_active() == True:
                self._current_char = char
                break
        else:
            self._completed = True
        self._check_key(key)

    def _check_key(self, key):
        ''' convert the first untyped character of the word from string to unicode to compare with the value from key parameter
        and call is_typed function of that character instance if the value matched the change the status of word selected to True
        '''

        if key == ord(self._current_char.get_char()):
            self._current_char.is_typed()
            self._selected = True

    def is_selected(self):
        ''' return the status whether the word is being typing or not '''

        return self._selected

    def is_completed(self):
        ''' return the status whether all the character of the word has been typed or not '''

        return self._completed

    def get_current_char(self):
        ''' return the character instance that is waiting to be typed '''

        return self._current_char

    def print_word(self):
        ''' show the word in the command line '''

        for char in self._char_list:
            print(char)

class Char():
    ''' class for character of the word attached to the missile '''

    def __init__(self,char):
        ''' create attributes of a Char instance '''

        self._char = char
        self._active = True    

    def is_typed(self):
        ''' call when the value of the character matched with the input key to change the active status of the instance '''

        self._active = False

    def is_active(self):
        ''' return whethe the char instance has been typed or not '''

        return self._active

    def get_char(self):
        ''' return the string value from the char attribute of the instance '''

        return self._char

    def __str__(self):
        ''' return the string of char attribute of the instance when the instance is called by print funcition '''

        return self._char

class MissileManager():
    ''' class for the missile manager of the game which is responsible the for the missile deployment, missile destroy '''

    def __init__(self, width, height, target=0, level=1, missile_height=100):
        ''' create the attributes for the missile manager instance '''

        self._target = target
        self._attack_zone_x = [target, width]
        self._attack_zone_y = [150, height]
        self._level = level
        self._slot_list = []
        for y_pos in range(self._attack_zone_y[1],200, -(missile_height)):
            self._slot_list.append(Slot(self._attack_zone_x, y_pos-50, self._target))
        self._wait_time = 3
        self._deploy_amount = 1
        self._current_slot = None
        self._damage = 0
        self._missile_count = 0
        self._timer = time.time()

    def add_word_manager(self, path):
        ''' use the path parameter to create the word manager instance then assign it to the word_manager attribute of the instance '''

        self._word_manager = WordManager(ReadWordFile(path).get_list())
        for slot in self._slot_list:
            slot.add_word_manager(self._word_manager)
    
    def draw(self):
        ''' call draw method of each slots '''

        for slot in self._slot_list:
            slot.draw()

    def update(self, key):
        ''' call methods to update value and status of attributes '''

        self._check_deploy_time()
        self._update_pos()
        self._key_handle(key)
        self._update_damage()
        self._update_missile_count()
        self._update_level()

    def _update_pos(self):
        ''' call an update posiotion funcition of slot that has a missile '''

        for slot in self._get_used_slot():
            slot.update_pos()

    def _key_handle(self,key):
        ''' check whether there is any selecting missile. 
        if there exist a selected slot, the key parameter will be passed to the update_key function of the selected slot
        else the key will be pass to slots to check it is matched with any of the slot in order to assign new slot to the current_slot attribute (selected slot)
        '''

        if self._current_slot == None or self._current_slot.is_selected() == False:
            for slot in self._get_used_slot():
                slot.update_key(key)
                if slot.is_selected() == True:
                    self._current_slot = slot
                    key = 0
                    break
        elif self._current_slot.is_use() == True:
            self._current_slot.update_key(key)

    def _update_damage(self):
        ''' get the damage value from each slots to update to damage attribute of the instance then reset damage of each slots to zero '''

        for slot in self._slot_list:
            self._damage += slot.get_damage()
            slot.reset_damage()

    def _update_missile_count(self):
        ''' get the destroyed missile amount from each slots to update the missile count attribute of the instance,
        then reset the missile count amount of each slots to zero.
        '''

        for slot in self._slot_list:
            self._missile_count += slot.get_missile_count()
            slot.reset_missile_count()

    def _check_deploy_time(self):
        ''' check whether it is time to deploy the missile or not based on the wait_time attribute
        if the time since the time in timer attribute is more than the value of wait_tume attribute deploy function will be called
        '''

        if time.time() - self._timer >= self._wait_time:
            self._deploy()
            self._timer = time.time()

    def _deploy(self):
        '''
        random a slot from a list of free slot (if there is a free slot) then call the create missile function and pass in the word
        which is from generate function of word_manager attribute
        '''

        for _ in range(self._deploy_amount):
            if self.have_free_slot() == True:
                    choice(self._get_free_slot()).create_missile(self._word_manager.generate())

    def _get_free_slot(self):
        '''
        return a list of free slots which can be indicated by their is_use() method that return false
        '''

        return [slot for slot in self._slot_list if slot.is_use() == False]

    def _get_used_slot(self):
        '''
        return a list of used slots which can be indicated by their is_use() method that return true
        '''

        return [slot for slot in self._slot_list if slot.is_use() == True]

    def have_free_slot(self):
        ''' return true if there is a free slot and return false if there is none '''

        for slot in self._slot_list:
            if slot.is_use() == False:
                return True
        return False

    def get_damage(self):
        ''' return the int value of the damage attribute of the instance '''

        return self._damage

    def reset_damage(self):
        ''' reset the value of the damage attribute by assigning the value to zero '''

        self._damage = 0 

    def get_missile_count(self):
        ''' return the int value of the missile_count attribute of the instance '''

        return self._missile_count
    
    def reset_missile_count(self):
        ''' reset the value of the missile_count attribute by assigning the value to zero '''

        self._missile_count = 0

    def _update_level(self):
        ''' update the value of attributes based on the level attribute.
        The game will be more difficult as the level attribute incrases.
        '''

        if self._level == 2:
            self._wait_time = 2
            self._deploy_amount = 2
        elif self._level == 3:
            self._deploy_amount = 3
        elif self._level == 4:
            self._deploy_amount = 4
            for slot in self._slot_list:
                if slot.get_level() != self._level:
                    slot._increase_missile_speed()
                    slot.set_level(self._level)
            self._word_manager.set_level(2)
        elif self._level == 5:
            self._deploy_amount = 5
            self._word_manager.set_level(3)
        elif self._level == 7:
            self._deploy_amount = 5
            self._word_manager.set_level(4)
        elif self._level == 8:
            self._deploy_amount = 5
            self._word_manager.set_level(5)
            for slot in self._slot_list:
                if slot.get_level() != self._level:
                    slot._increase_missile_speed()
                    slot.set_level(self._level)
        elif self._level == 11:
            for slot in self._slot_list:
                if slot.get_level() != self._level:
                    slot._increase_missile_speed()
                    slot.set_level(self._level)
        elif self._level == 13:
            for slot in self._slot_list:
                if slot.get_level() != self._level:
                    slot._increase_missile_speed()
                    slot.set_level(self._level)
        elif self._level == 15:
            for slot in self._slot_list:
                if slot.get_level() != self._level:
                    slot._increase_missile_speed()
                    slot.set_level(self._level)

    def increase_level(self):
        ''' increase the value of the level attribute by one if its value is less than ten '''

        if self._level < 15:
            self._level += 1

class Slot():
    ''' class for slots in the missile manager which each instance has its own y position and responsible for missile in the x range of position '''

    def __init__(self, x, y, target, level=1):
        ''' create attributes for slot instance '''

        self._word_manager = None
        self._in_use = False
        self._selected = False
        self._x_points = x
        self._y_pos = y
        self._missile = None
        self._wait_pixel = 0
        self._target = target
        self._damage = 0
        self._missile_count = 0
        self._missile_speed = 1
        self._level = level

    def add_word_manager(self, word_managaer):
        ''' assign the word_manager parameter to word_manager attribute '''

        self._word_manager = word_managaer

    def create_missile(self, word):
        ''' create the missile which the position, the target coordinate, and the speed based on attributes of instance
        and the word from word parameter then reassign the value of the in_use attribute with True to indicate that the slot instance
        has a missile in it.
        '''

        self._missile = Missile(self._x_points[1], self._y_pos, word=word, target=self._target, speed=self._missile_speed)
        self._in_use = True

    def draw(self):
        ''' call a draw function of the missile instance if there is a missile instance binding to missile attribute '''

        if self._missile != None:
            self._missile.draw_with_word()

    def update_pos(self):
        ''' call functions to update position and check the status of the missile instance binding to missile attribute '''

        self._missile.update_pos()
        self.check_missile_status()

    def update_key(self, key):
        ''' call update_key and pass in the key parameter to the missile instance binding to missile attribute
        in order to check whether the key pressed matched with char of the missile.
        '''

        self._missile.update_key(key)

    def is_use(self):
        ''' return whether the instance is currently having a missile or not '''
        return self._in_use

    def is_selected(self):
        ''' return whether the missile of instance has been matched with the key pressed or not '''

        return self._selected

    def check_missile_status(self):
        ''' check the value from the missile instance an update the value of attributes
        if the missile has been selected the selected instace will be reassign to True
        and if the missile status is not active the delete_missile function will be called
        '''

        if self._missile.is_selected() == True:
            self._selected = True
        if self._missile.is_active() == False:
            self._delete_missile()

    def _delete_missile(self):
        ''' 
        Add a value from missile get_damage method to the damage attribute
        If the damage from get_damage method is zero, it means that the missile is set to inactive by typing in the word completely 
        so missile_count attribute will be added by one.
        Then the first of alphabet of the word attached to the missile will be pass to recycle method of the word manager attribute
        to make the word starts with recycled alphabet able to be generated again.
        Lastly, reassign the value of missile releted attribute to be as there is no missile.
        '''
        self._damage += self._missile.get_damage()
        if self._missile.get_damage() == 0:
            self._missile_count += 1
        self._word_manager.recycle(self._missile.get_first_alphabet())
        self._missile = None
        self._in_use = False
        self._selected = False

    def _increase_missile_speed(self):
        ''' Increase the missile_speed attribute by half which make the missile that will be created move faster '''
        self._missile_speed += 0.5

    def set_level(self, level):
        ''' Assign a value from level parameter to the level attribute '''

        self._level = level

    def get_level(self):
        ''' return an int value of the level attribute '''

        return self._level

    def get_damage(self):
        ''' return an int value of the damage attribute '''

        return self._damage

    def reset_damage(self):
        ''' reset the value of the damage attribute by reassigining its value to zero. '''

        self._damage = 0

    def get_missile_count(self):
        ''' return an int value of the missile_count attribute '''

        return self._missile_count

    def reset_missile_count(self):
        ''' reset the value of the missile_count attribute by reassigining its value to zero. '''

        self._missile_count = 0


class ReadWordFile():
    ''' class for ReadWordFile which is responsible for reading the file'''

    def __init__(self, file_name=''):
        ''' open the file from the path given by file_name parameter then read each lines to get words and categorized them and assign to categorized_word attribute '''

        with open(file_name, 'r') as Fin:
            self._raw_word = [x.strip() for x in Fin.readlines()]
        self._categorized_word = {}
        for word in self._raw_word:
            if word[0].lower() not in self._categorized_word:
                self._categorized_word[word[0].lower()] = [word]
            else:
                self._categorized_word[word[0].lower()].append(word)

    def get_list(self):
        ''' return dictionary object from categorized_word attribute '''

        return self._categorized_word

class WordManager():
    ''' class for WordManager which is responsible for managing the word and generate the word '''

    def __init__(self, word_dict, level=1):
        ''' create attributes for wordmanager instance '''

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
        ''' return a dictionary object containing words with less than five characters '''

        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def _get_long(self):
        ''' return a dictionary object containing words with more than or equal to five characters '''

        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def generate(self):
        ''' return a string of word random based on level attribute and also add the string of first character of it to the used attribute and remove it from the unused attribute '''

        alphabet = choice(self._unused)
        self._used.append(alphabet)
        self._unused.remove(alphabet)
        return choice(self._short_word[alphabet] + self._long_word[alphabet] * self._level)

    def set_level(self, level):
        ''' assign the level attribute with int value from level parameter '''

        self._level = level

    def recycle(self, alphabet):
        ''' remove the string from alphabet parameter from used attribute and add it to the unused attribute '''

        self._unused.append(alphabet)
        self._used.remove(alphabet)

class Component_list():
    ''' class for component_list which is responsible for containing, drawing, and updating the components of the gameplay screen. '''

    def __init__(self):
        ''' create attribute of component_list instance '''

        self._components = []

    def draw(self):
        ''' call draw method of each elements in components attribute if it is not empty '''

        if len(self._components) > 0:
            [component.draw() for component in self._components]

    def add_component(self, component):
        ''' append the component parameter to the list binding to component attribute'''

        self._components.append(component)

    def update(self):
        ''' call update method of rach elements in components attribute if it isv not empty '''

        if len(self._components) > 0:
            [component.update() for component in self._components]
            [component.update_animation() for component in self._components]

class ScoreFileRW():
    ''' class for ScoreFileRw which is responsible for reading and writing the score file '''

    def __init__(self,name):
        ''' create attributes of and ScoreFileRW instance '''

        self.file_name = name
        self.score_list = []

    def read(self):
        ''' open the file from the path stored in file_name attribute and read and split them by the colon and convert the data type from
        string to float and store them as a nested list which each lists contains the stats of the match played
        '''

        with open( self.file_name , 'r') as file:
            file = file.readlines()
            score_list = [x.strip().split(',') for x in file if len(x) > 1]
        for line in score_list:
            for i in range(len(line)):
                line[i] = float(line[i])
        self.score_list = score_list

    def write(self, score_lst):
        '''open the file from the path stored in file_name attribute and append the string containing the stats from score_lst parameter to the last line of the text file '''

        with open( self.file_name, 'a') as file:
            file.write(f'\n{score_lst[0]},{score_lst[1]:.2f},{score_lst[2]:.2f}')

    def get_score(self):
        ''' return the list from score_list attribute '''

        return self.score_list

    def get_best(self):
        ''' return the list containing the stats of the match that has the longest play time '''

        return sorted(self.score_list,key=lambda x: x[1], reverse=True)[0]

    def get_latest_five(self):
        ''' return the list containg the stats list of lastest five match '''

        result = self.score_list[::-1]
        return result[0:5]

class World:
    ''' class for world which is responsible for everything in each match of the game '''

    STATE_FROZEN = 1
    STATE_STARTED = 2

    def __init__(self, width, height, cloud_amount=5):
        ''' 
        Create attributes for world instance.
        Set the width and height attributes based on width and height parameter.
        Set the amount of cloud instance to be created based on cloud_amount parameter which has the value of five by default
        ''' 

        self._width = width
        self._height = height

        self._rocket = None
        self._missile_count = 0
        self._time = 0
        self._next_level_time = 10
        self._ready = False
        self._gameover = False
        self._score_witten = False
        self._restart = False

        self._state = World.STATE_FROZEN

        self._components = Component_list()
        self._cloud_amount = cloud_amount
        self._cloud_list = arcade.SpriteList()
        self._cloud_list.sprite_list = list(map(lambda x : Cloud(self._width, self._height), range(self._cloud_amount)))
        self._type = None

    def add_rocket(self, rocket):
        ''' assign the instance of rocket from rocket parameter to rocket attribute '''

        self._rocket = rocket

    def add_missile_manager(self, word_path):
        ''' 
        create a MissileManager instance inputing the width,height,target based on the world instance attribute and assign it to the missile_manager attribute
        then call tha add_word_manager method and pass in the word_path parameter.
        '''

        self._missile_manager = MissileManager(self._width, self._height, target=self._rocket.right)
        self._missile_manager.add_word_manager(word_path)

    def add_score_rw(self,obj):
        ''' assigning the instance of ScoreFileRW class from parameter obj to score_rw attribute '''

        self._score_rw = obj

    def add_component(self, component):
        ''' call the add_component method of the components attribute which is binded to component_list instance and pass in the component parameter '''

        self._components.add_component(component)

    def add_cloud_texture(self, texture, scale=1):
        '''
        add texture from texture parameter to each cloud instances in cloud_list attribute 
        and set their texture to zero.
        '''

        for cloud in self._cloud_list:
            cloud.textures.append(arcade.load_texture(texture,scale=scale))
            cloud.set_texture(0)

    def start(self):
        ''' assign the value of state attribute to indicate that the game is started '''

        self._state = World.STATE_STARTED

    def freeze(self):
        ''' assign the value of state attribute to indicate that the game is freezed '''

        self._state = World.STATE_FROZEN

    def check_start_pos(self):
        ''' 
        check if the rocket is in the position that is ready to play or not.
        if the rocket is in the ready position, the ready method of the world and rocket instance will be called
        '''

        if self._rocket.center_y >= self._height//2 and self._is_ready() == False:
            self._world_ready()
            self._rocket.ready()

    def _world_ready(self):
        ''' assiging the ready attribute to True and assign the time at the moment to start_time attribute '''

        self._ready = True
        self._start_time = time.time()

    def is_started(self):
        ''' return whether the game is started or not '''

        return self._state == World.STATE_STARTED

    def draw(self):
        ''' draw components of the gameplay based on the situation of the game '''

        if self._is_over() == False:
            self._cloud_list.draw()
        self._rocket.draw()
        if self._is_over() == False:
            arcade.draw_rectangle_filled(self._width//2, 35, 305, 55, color=arcade.color.WHITE)
            arcade.draw_rectangle_filled(self._width//2, 35/100*self._rocket.get_health(), 305, 60/100*self._rocket.get_health(), color=arcade.color.ORANGE_RED)
            self._components.draw()
            self._draw_stat()
            self._missile_manager.draw()
        if self._is_over() == True and self._rocket._out_of_screen() == True:
            self._draw_gameover()

    def _draw_gameover(self):
        ''' store the stats of the match played into the file and call the method to draw the game stats '''

        result = arcade.load_texture('images/result.png')
        arcade.draw_texture_rectangle(self._width//2 , self._height//2 ,self._width-250, self._height-150,result)
        self._draw_gameover_stat()
        if self._score_witten == False:
            self._score_rw.write([self._missile_count, self._time, self._missile_count/(self._time/60)])
            self._score_rw.read()
            self._score_witten = True
        self._restart = True

    def _draw_gameover_stat(self):
        ''' draw the statistics of the match '''

        arcade.draw_text(f'Result',
                self._width//2 - 50, self._height//2 + 195,
                arcade.color.BLACK, font_size=35)
        arcade.draw_text(f'Total Words: {self._missile_count}',
                self._width//2 - 230, self._height//2 + 110,
                arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Total Time: {self._time:.2f}',
                self._width//2 - 230, self._height//2 + 30,
                arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Speed: {(self._missile_count/(self._time/60)):.2f} WPM',
                self._width//2 - 230, self._height//2 - 50,
                arcade.color.BLACK, font_size=30)

        arcade.draw_text(f'Local Best Time: {self._score_rw.get_best()[1]:.2f} s',
                self._width//2 - 230, self._height//2 - 130,
                arcade.color.BLACK, font_size=30)

        arcade.draw_text('Press Enter To Go Back To Menu',
                self._width//2 - 260, self._height//2 - 210,
                arcade.color.BLACK, font_size=30)

    def _draw_stat(self):
        ''' draw the stat of the game '''

        arcade.draw_text('RocketTyper',
                100, 25,
                arcade.color.BLACK, font_size=25)
        self._draw_rocket_health()
        self._draw_missile_count()
        self._draw_time()

    def _draw_rocket_health(self):
        ''' draw the text showing the rocket health on the game screen '''

        arcade.draw_text('HEALTH',
                self._width//2 - 50, 25,
                arcade.color.BLACK, font_size=25)

    def _draw_missile_count(self):
        ''' draw the text showing the amount of missiles destroyed on the screen '''

        arcade.draw_text(str(f'Word: {self._missile_count}'),
                self._width//2 + 175, 25,
                arcade.color.BLACK, font_size=22)

    def _draw_time(self):
        ''' draw the text showing the time since the game started on the screen '''

        arcade.draw_text(str(f'Time: {self._time:.2f} s'),
                self._width//2 + 300, 25,
                arcade.color.BLACK, font_size=22)

    def update(self, delta):
        ''' call the update method of components of the game based on the state attribute '''

        if self._state == World.STATE_FROZEN:
            return
        self._rocket.update()
        self._rocket.update_animation()
        self.check_start_pos()
        if self._is_over() == False:
            self._components.update()
            self._cloud_list.update()
            self._missile_manager.update(self._type)
            self._type = 0
        if self._is_ready() == True and self._is_over() == False:
            self._update_health()
            self._update_missile_count()
            self._update_time()
            self._update_level()
        self._check_gameover()

    def _check_gameover(self):
        ''' check if the rocket is broken then update the value of gameover attribute '''

        if self._rocket.is_over() == True:
            self._gameover = True

    def _update_level(self):
        ''' check the time passed and increase the difficulty based on it '''

        if self._time >= self._next_level_time:
            self._missile_manager.increase_level()
            self._next_level_time += 10

    def _update_time(self):
        ''' compute the time passed by subtracting the current time with the starting time then assign the value to time attribute '''

        self._time = time.time() - self._start_time

    def _update_missile_count(self):
        ''' check and update the missile_count attribute by getting value from the missile_manager then reset it to zero '''

        self._missile_count += self._missile_manager.get_missile_count()
        self._missile_manager.reset_missile_count()
    
    def _update_health(self):
        ''' check and get the damage which came from the destroyed and hitted missiles from missile manager
        and pass it to the method update health of the rocket to update the rocket health
        '''

        self._rocket.update_health(self._missile_manager.get_damage())
        self._missile_manager.reset_damage()

    def _is_over(self):
        ''' return whether the game is over or not '''

        return self._gameover

    def _is_ready(self):
        ''' return whether the game is ready or not '''

        return self._ready

    def get_restart(self):
        ''' return whether the game is ready for restart or not '''

        return self._restart

    def on_key_press(self, key, key_modifiers):
        ''' 
        assign the int value from the key parameter to the type attribute
        [ type is shorten for key typed ]
        '''
        self._type = key