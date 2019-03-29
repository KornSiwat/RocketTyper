import arcade
from models import World
import time

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()
        
class RocketTyperWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/background.png")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.rocket_sprite = ModelSprite('images/rocket.png', model=self.world.rocket)                                        
        self.rocket_sprite.append_texture(arcade.load_texture('images/rocket01.png'))   
        # self.rocket_sprite.set_texture(1)

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
        arcade.set_viewport(self.world.rocket.x - SCREEN_WIDTH // 2,
                            self.world.rocket.x + SCREEN_WIDTH // 2,
                            0, SCREEN_HEIGHT)

        arcade.start_render()
        arcade.draw_texture_rectangle(self.rocket_sprite.center_x , SCREEN_HEIGHT // 2,
                        SCREEN_WIDTH+50, SCREEN_HEIGHT, self.background)

        # arcade.draw_text("Space to Start", -100, self.height//2 , arcade.color.GREEN, 30)
        self.rocket_sprite.draw()
        arcade.draw_text(str(self.world.rocket.health),
                        self.world.rocket.x + (SCREEN_WIDTH // 2) - 60,
                        self.height - 30,
                        arcade.color.WHITE, 20)
        

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if not self.world.is_started():
                self.world.start()
            self.world.on_key_press(key, key_modifiers)
        if key == arcade.key.R:
            self.reset()

if __name__ == '__main__':
    window = RocketTyperWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()
