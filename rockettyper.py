import arcade
from models import World, ModelSprite, MenuChoice
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

        self.current_route = routes['menu']

        self.background = arcade.load_texture("images/background.png")
        self.play_route_init(width,height)
        self.menu_route_init()

    def menu_setup(self):
        self.choice_list = arcade.SpriteList()


    def play_route_init(self, width, height):
        self.world = World(width, height)
        
        self.rocket_sprite = ModelSprite('images/rocket.png', model=self.world.rocket)                                        
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket01.png'))

        self.timeCount = time.time()
        self.cur_texture = 0    


    def update(self, delta):
        self.world.update(delta)
        if time.time() - self.timeCount > 0.2:
            self.move()

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

    def menu_route(self):
        pass

    def play_route(self):
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
