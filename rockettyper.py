import arcade
from models import World, Rocket, MenuChoiceSprite, Missile
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
    def __init__(self, width, height):
        super().__init__(width, height)

        self.current_route = routes['menu']
        self.selecting_choice = 0

        self.background = arcade.load_texture("images/background.png")
        self.menu_setup()
        self.game_setup(width,height)

    def menu_setup(self):
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

    def game_setup(self, width, height):
        self.world = World(width, height)

        self.cockpit = arcade.Sprite()
        self.cockpit.center_x,self.cockpit.center_y = width//2, 50
        self.cockpit.append_texture(arcade.load_texture('images/cockpit.png'))
        self.cockpit.set_texture(0)
        
        
        self.rocket_scale = 1.3
        self.rocket_sprite = Rocket(110,-120)                                        
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket6.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket5.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket4.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket3.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket2.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket1.png', scale=self.rocket_scale))
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket.png', scale=self.rocket_scale))
        self.rocket_sprite.set_texture(0)
        self.rocket_sprite.texture_change_frames = 8
        print(self.rocket_sprite.right)

        self.test = Missile(900,400,'itest',target=self.rocket_sprite.right)
        self.test.append_texture(arcade.load_texture('images/missile.png'))
        self.test.set_texture(0)

        self.world.rocket = self.rocket_sprite

        for cloud in self.world.cloud_list:
            cloud.append_texture(arcade.load_texture('images/cloud.png'))
            cloud.set_texture(0)

    def update(self, delta):
        if self.current_route == routes['menu']:
            self.rocket_menu.update()
            self.rocket_menu.update_animation()
            for choice in self.choice_list:
                if choice.is_select == True:
                    choice.update()
                    choice.update_animation()
        elif self.current_route == routes['game']:
            self.world.update(delta)
            self.test.update()
            self.test.update_animation()

    def on_draw(self):

        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height,self.background)

        if self.current_route == routes['menu']:
            self.draw_menu()
        elif self.current_route == routes['game']:
            self.draw_game()

    def draw_menu(self):
        self.rocket_menu.draw()
        self.choice_list.draw()
            
    def draw_game(self):
        if self.world.is_ready == True:
            self.world.cloud_list.draw()
        self.rocket_sprite.draw()
        self.cockpit.draw()
        self.test.draw_with_word()
        arcade.draw_text(str(self.world.rocket.health),
                        self.width-60 ,
                        self.height - 30,
                        arcade.color.BLACK, 20)

    def update_selected_choice(self):
        for choice in self.choice_list:
            choice.unselect()
            choice.set_texture(1)
        self.choice_list[self.selecting_choice].select()

    def on_key_press(self, key, key_modifiers):

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
            if key == arcade.key.DOWN:
                self.world.rocket.move_down()
            elif key == arcade.key.UP:
                self.world.rocket.move_up()
            elif key == arcade.key.P:
                if self.world.is_started():
                    self.world.freeze()
                else:
                    self.world.start()

if __name__ == '__main__':
    window = RocketTyperWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
