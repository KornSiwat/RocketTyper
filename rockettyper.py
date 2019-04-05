import arcade
from models import World, ModelSprite, MenuChoiceSprite
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

routes = {
    'menu':0,
    'game':1,
    'instruction':2,
    'scoreboard':3,
}

class RocketTyperWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.current_route = routes['game']

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

        self.choice_list.append(self.rocket_menu)
        self.choice_list.append(self.start)
        self.choice_list.append(self.howToPlay)
        self.choice_list.append(self.scoreboard)

    def game_setup(self, width, height):
        self.world = World(width, height)
        
        self.rocket_sprite = ModelSprite('images/rocket.png', model=self.world.rocket)                                        
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket1.png'))

        self.timeCount = time.time()
        self.cur_texture = 0    

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

    def move(self):
        if self.cur_texture == 0:
            self.rocket_sprite.set_texture(1)
            self.cur_texture = 1
        else:
            self.rocket_sprite.set_texture(0)
            self.cur_texture = 0
        self.timeCount = time.time()

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
        self.rocket_sprite.draw()
        arcade.draw_text(str(self.world.rocket.health),
                        self.width-60 ,
                        self.height - 30,
                        arcade.color.BLACK, 20)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if not self.world.is_started():
                self.world.start()
            self.world.on_key_press(key, key_modifiers)

if __name__ == '__main__':
    window = RocketTyperWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
