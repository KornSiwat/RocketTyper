import arcade
# from dummy import World, Rocket, Missile, ScoreFileManager
from models.MenuChoiceSprite import MenuChoiceSprite
from models.World import World
from models.Rocket import Rocket
from models.Missile import Missile
from models.ScoreFileManager import ScoreFileManager

import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

routes = {
    'menu':0,
    'game':1,
    'instruction':2,
    'scoreboard':3,
}

choices = {
    0: 'game',
    1: 'instruction',
    2: 'scoreboard'
}

class RocketTyperWindow(arcade.Window):
    ''' Class for game window '''

    def __init__(self, width, height):
        ''' create important attribute for the game '''

        super().__init__(width, height)
        self.size_width = width
        self.size_height = height

        self.current_route = routes['menu']
        self.selecting_choice = 0

        self.background = arcade.load_texture("images/background.png")
        self.gray_background = arcade.load_texture("images/result.png")
        self.score_rw = ScoreFileManager('score.txt')
        self.score_rw.read()
        self.menu_setup()
        self.game_setup(width,height)

        self.fpscounter = Fpscounter()
        self.set_update_rate(1/60)

    def menu_setup(self):
        ''' create menu route element '''

        self.choice_list = arcade.SpriteList()

        self.rocket_menu = MenuChoiceSprite()
        self.rocket_menu.textures.append(arcade.load_texture("images/rocket.png",scale=1.3))
        self.rocket_menu.textures.append(arcade.load_texture("images/rocket1.png",scale=1.3))
        self.rocket_menu.set_texture(0)
        self.rocket_menu.texture_change_frames = 10

        self.start = MenuChoiceSprite()
        self.start.textures.append(arcade.load_texture("images/start.png"))
        self.start.textures.append(arcade.load_texture("images/start1.png"))
        self.start.set_texture(0)
        self.start.texture_change_frames = 10

        self.howToPlay = MenuChoiceSprite()
        self.howToPlay.textures.append(arcade.load_texture("images/howtoplay.png"))
        self.howToPlay.textures.append(arcade.load_texture("images/howtoplay1.png"))
        self.howToPlay.set_texture(1)
        self.howToPlay.texture_change_frames = 10

        self.scoreboard = MenuChoiceSprite()
        self.scoreboard.textures.append(arcade.load_texture("images/scoreboard.png"))
        self.scoreboard.textures.append(arcade.load_texture("images/scoreboard1.png"))
        self.scoreboard.set_texture(1)
        self.scoreboard.texture_change_frames = 10

        self.rocket_menu.center_x,self.rocket_menu.center_y = self.width//2,self.height//2 + 120
        self.start.center_x,self.start.center_y = self.width//2,self.height//2 - 90
        self.howToPlay.center_x,self.howToPlay.center_y = self.width//2,self.height//2 - 160
        self.scoreboard.center_x,self.scoreboard.center_y = self.width//2,self.height//2 - 230

        self.rocket_menu.select()
        self.start.select()
        self.howToPlay.unselect()
        self.scoreboard.unselect()

        self.choice_list.append(self.start)
        self.choice_list.append(self.howToPlay)
        self.choice_list.append(self.scoreboard)

        self.instruction = arcade.load_texture('images/instruction.png')
        self.scoreboard_bg = arcade.load_texture('images/scoreboardbg.png')

    def game_setup(self, width, height):
        ''' create gameplay route element '''

        self.world = World(width, height)

        self.cockpit = arcade.Sprite()
        self.cockpit.center_x,self.cockpit.center_y = width//2, 50
        self.cockpit.append_texture(arcade.load_texture('images/cockpit.png'))
        self.cockpit.set_texture(0)
        self.world.add_component(self.cockpit)
        
        rocket_scale = 1.3
        rocket = Rocket(110,-120)                                        
        rocket.append_texture(arcade.load_texture('images/rocket6.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket5.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket4.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket3.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket2.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket1.png', scale=rocket_scale))
        rocket.append_texture(arcade.load_texture('images/rocket.png', scale=rocket_scale))
        rocket.set_texture(0)
        rocket.texture_change_frames = 8
        self.world.add_rocket(rocket)

        self.world.add_missile_manager('word/word.txt')
        self.world.add_cloud_texture('images/cloud.png')
        self.world.add_scoreManager(self.score_rw)

    def update(self, delta):
        ''' update the value based on current route '''

        if self.current_route == routes['menu']:
            self.rocket_menu.update()
            self.rocket_menu.update_animation()
            for choice in self.choice_list:
                if choice.is_selected() == True:
                    choice.update()
                    choice.update_animation()
        elif self.current_route == routes['game']:
            self.world.update(delta)

    def on_draw(self):
        ''' render element based on route '''

        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height,self.background)

        if self.current_route == routes['menu']:
            self.draw_menu()
        elif self.current_route == routes['game']:
            self.draw_game()
        elif self.current_route == routes['instruction']:
            self.draw_instruction()
        elif self.current_route == routes['scoreboard']:
            self.draw_scoreboard()

        self.fpscounter.tick()
        fps = f"fps{self.fpscounter.fps():.2f}"
        arcade.draw_text(fps, 6,self.size_height - 18,arcade.color.BLACK)


    def draw_menu(self):
        ''' draw menu route element '''

        self.howToPlay.center_y = self.height//2 - 160
        self.scoreboard.center_y = self.height//2 - 230
        self.rocket_menu.draw()
        self.choice_list.draw()
            
    def draw_game(self):
        ''' draw gameplat route element '''

        self.world.draw()

    def draw_instruction(self):
        ''' draw instruction route element '''

        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width-250, self.height-150, self.gray_background)

        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width-250, self.height-150 ,self.instruction)

        self.howToPlay.center_y = self.size_height//2 + 205
        self.howToPlay.set_texture(0)
        self.howToPlay.draw()

    def draw_scoreboard(self):
        ''' draw scoreboard route element '''

        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width-250, self.height-150,self.gray_background)
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width-250, self.height-150 ,self.scoreboard_bg)

        self.scoreboard.center_y = self.size_height//2 + 205
        self.scoreboard.set_texture(0)
        self.scoreboard.draw()

        arcade.draw_text('No.',
                self._width//2 - 280, self._height//2 + 100,
                arcade.color.BLACK, font_size=23)
        arcade.draw_text('Words',
                self._width//2 - 200, self._height//2 + 100,
                arcade.color.BLACK, font_size=23)
        arcade.draw_text('Word Per Minute',
                self._width//2 - 75, self._height//2 + 100,
                arcade.color.BLACK, font_size=23)
        arcade.draw_text('Total Time',
                self._width//2 + 170, self._height//2 + 100,
                arcade.color.BLACK, font_size=23)
        for no, score in enumerate(self.score_rw.get_latest_five(),1):

            arcade.draw_text(f'{no}',
                    self._width//2 - 270, self._height//2 + 90 - 30*no,
                    arcade.color.BLACK, font_size=23)

            arcade.draw_text(f'{score[0]:02.2f}',
                    self._width//2 - 180, self._height//2 + 90 - 30*no,
                    arcade.color.BLACK, font_size=23)

            arcade.draw_text(f'{score[2]}',
                    self._width//2 , self._height//2 + 90 - 30*no,
                    arcade.color.BLACK, font_size=23)

            arcade.draw_text(f'{score[1]}',
                    self._width//2 + 200, self._height//2 + 90 - 30*no,
                    arcade.color.BLACK, font_size=23)

        arcade.draw_text(f'Local Best Time: {self.score_rw.get_best()[1]:.2f} s',
                self._width//2 - 320, self._height//2 - 120,
                arcade.color.BLACK, font_size=23)

        arcade.draw_text(f'World Best Time: Feature Coming Soon',
                self._width//2 - 320, self._height//2 - 160,
                arcade.color.BLACK, font_size=23)

    def update_selected_choice(self):
        ''' check the selecting menu choice and update the value to current route '''

        for choice in self.choice_list:
            choice.unselect()
            choice.set_texture(1)
        self.choice_list[self.selecting_choice].select()

    def on_key_press(self, key, key_modifiers):
        ''' passing the press key value to elements based on current route '''

        if self.current_route == routes['menu']:
            if key == arcade.key.DOWN:
                if self.selecting_choice < 2:
                    self.selecting_choice += 1
                else:
                    self.selecting_choice = 0
                self.update_selected_choice()
            elif key == arcade.key.UP:
                if self.selecting_choice > 0 :
                    self.selecting_choice -= 1
                else:
                    self.selecting_choice = 2
                self.update_selected_choice()
            elif key == arcade.key.ENTER:
                self.current_route = routes[choices[self.selecting_choice]]
                if self.current_route == routes['game']:
                    self.world.start()
        elif self.current_route == routes['game']:
            if self.world.get_restart() == True:
                if key == arcade.key.ENTER:
                    self.game_setup(self.size_width,self.size_height)
                    self.current_route = routes['menu']
            else:
                self.world.on_key_press(key,key_modifiers)
        elif self.current_route == routes['instruction']:
            if key == arcade.key.ESCAPE:
                self.current_route = routes['menu']
        elif self.current_route == routes['scoreboard']:
            if key == arcade.key.ESCAPE:
                self.current_route = routes['menu']

class Fpscounter:
    ''' class for the fps counting '''

    def __init__(self):
        import time
        import collections
        self.time = time.perf_counter
        self.frametime = collections.deque(maxlen=60)
        self.t = self.time()

    def tick(self):
        ''' count the frame when draw '''

        t = self.time()
        dt = t-self.t 
        self.frametime.append(dt)
        self.t = t   

    def fps(self):
        ''' return the current fps '''

        try:
            return 60/sum(self.frametime)
        except ZeroDivisionError:
            return 0


if __name__ == '__main__':
    window = RocketTyperWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
