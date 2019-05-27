import arcade
from .MenuChoiceSprite import MenuChoiceSprite
from .World import World
from .Rocket import Rocket
from .Missile import Missile
from .ScoreFileManager import ScoreFileManager
from .FpsCounter import Fpscounter
import time

import sys
sys.path.append('..')

from scenes.InstructionScene import InstructionScene
from scenes.ScoreBoardScene import ScoreBoardScene

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

        self.scoreManager = ScoreFileManager('score.txt')
        self.scoreManager.read()

        self.menu_setup()

        self.instruction_setup(width,height)

        self.scoreboard_setup(width, height)
        
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

        self.startChoice = MenuChoiceSprite()
        self.startChoice.textures.append(arcade.load_texture("images/start.png"))
        self.startChoice.textures.append(arcade.load_texture("images/start1.png"))
        self.startChoice.set_texture(0)
        self.startChoice.texture_change_frames = 10

        self.howToPlayChoice = MenuChoiceSprite()
        self.howToPlayChoice.textures.append(arcade.load_texture("images/howtoplay.png"))
        self.howToPlayChoice.textures.append(arcade.load_texture("images/howtoplay1.png"))
        self.howToPlayChoice.set_texture(1)
        self.howToPlayChoice.texture_change_frames = 10

        self.scoreboardChoice = MenuChoiceSprite()
        self.scoreboardChoice.textures.append(arcade.load_texture("images/scoreboard.png"))
        self.scoreboardChoice.textures.append(arcade.load_texture("images/scoreboard1.png"))
        self.scoreboardChoice.set_texture(1)
        self.scoreboardChoice.texture_change_frames = 10

        self.rocket_menu.center_x,self.rocket_menu.center_y = self.width//2,self.height//2 + 120
        self.startChoice.center_x,self.startChoice.center_y = self.width//2,self.height//2 - 90
        self.howToPlayChoice.center_x,self.howToPlayChoice.center_y = self.width//2,self.height//2 - 160
        self.scoreboardChoice.center_x,self.scoreboardChoice.center_y = self.width//2,self.height//2 - 230

        self.rocket_menu.select()
        self.startChoice.select()
        self.howToPlayChoice.unselect()
        self.scoreboardChoice.unselect()

        self.choice_list.append(self.startChoice)
        self.choice_list.append(self.howToPlayChoice)
        self.choice_list.append(self.scoreboardChoice)

    def game_setup(self, width, height):
        ''' create gameplay scene element '''

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
        self.world.add_scoreManager(self.scoreManager)

    def instruction_setup(self, width, height):
        self.instructionScene = InstructionScene(width, height)

    def scoreboard_setup(self, width, height):
        self.scoreboardScene = ScoreBoardScene(width, height, self.scoreManager) 

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
        ''' render scenes based on chosen route '''

        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height,self.background)

        if self.current_route == routes['menu']:
            self.draw_menu()
        elif self.current_route == routes['game']:
            self.draw_game()
        elif self.current_route == routes['instruction']:
            self.instructionScene.draw()
        elif self.current_route == routes['scoreboard']:
            self.scoreboardScene.draw()

        self.fpscounter.tick()
        fps = f"fps{self.fpscounter.fps():.2f}"
        arcade.draw_text(fps, 6,self.size_height - 18,arcade.color.BLACK)

    def draw_menu(self):
        ''' draw menu route element '''

        self.howToPlayChoice.center_y = self.height//2 - 160
        self.scoreboardChoice.center_y = self.height//2 - 230
        self.rocket_menu.draw()
        self.choice_list.draw()

    def draw_game(self):
        ''' draw gameplat route element '''

        self.world.draw()

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
