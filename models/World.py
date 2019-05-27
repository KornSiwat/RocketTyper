import arcade
from .Cloud import Cloud
from .ComponentList import ComponentList
from .MissileManager import MissileManager
from .MatchStat import MatchStat
import time

class World():

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

        self._components = ComponentList()
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

    def add_scoreManager(self, scoreManager):
        ''' assigning the instance of ScoreFileRW class from parameter obj to score_rw attribute '''

        self._scoreManager = scoreManager

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
            self._scoreManager.write(MatchStat(wordAmount=self._missile_count, wordPerMinute=self._missile_count/(self._time/60), totalTime=self._time))
            self._scoreManager.read()
            self._score_witten = True
        self._restart = True

    def _draw_gameover_stat(self):
        ''' draw the statistics of the match '''

        arcade.draw_text(f'Result', self._width//2 - 50, self._height//2 + 195, arcade.color.BLACK, font_size=35)
        arcade.draw_text(f'Total Words: {self._missile_count}', self._width//2 - 230, self._height//2 + 110, arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Total Time: {self._time:.2f}', self._width//2 - 230, self._height//2 + 30, arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Speed: {(self._missile_count/(self._time/60)):.2f} WPM', self._width//2 - 230, self._height//2 - 50, arcade.color.BLACK, font_size=30)
        arcade.draw_text(f'Local Best Time: {self._scoreManager.get_best().totalTime:.2f} s', self._width//2 - 230, self._height//2 - 130, arcade.color.BLACK, font_size=30)
        arcade.draw_text('Press Enter To Go Back To Menu', self._width//2 - 260, self._height//2 - 210, arcade.color.BLACK, font_size=30)

    def _draw_stat(self):
        ''' draw the stat of the game '''

        arcade.draw_text('RocketTyper', 100, 25, arcade.color.BLACK, font_size=25)
        self._draw_rocket_health()
        self._draw_missile_count()
        self._draw_time()

    def _draw_rocket_health(self):
        ''' draw the text showing the rocket health on the game screen '''

        arcade.draw_text('HEALTH', self._width//2 - 50, 25, arcade.color.BLACK, font_size=25)

    def _draw_missile_count(self):
        ''' draw the text showing the amount of missiles destroyed on the screen '''

        arcade.draw_text(str(f'Word: {self._missile_count}'), self._width//2 + 175, 25, arcade.color.BLACK, font_size=22)

    def _draw_time(self):
        ''' draw the text showing the time since the game started on the screen '''

        arcade.draw_text(str(f'Time: {self._time:.2f} s'), self._width//2 + 300, 25, arcade.color.BLACK, font_size=22)

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