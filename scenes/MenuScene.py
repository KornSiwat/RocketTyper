import arcade
import sys

sys.path.append('..')
from models.MenuChoiceSprite import MenuChoiceSprite

choices = {
    0: 'game',
    1: 'instruction',
    2: 'scoreboard'
}

class MenuScene():
    def __init__(self,width, height, on_select):
        self._width = width
        self._height = height

        self._texture_frame_rate = 10
        self.selecting_choice = 0

        self.setup_assets()
        self.setup_choice_list()
        self.config_sprites()

        self.on_select = on_select

    def setup_assets(self):
        self.rocket_menu = MenuChoiceSprite()
        self.startChoice = MenuChoiceSprite()
        self.howToPlayChoice = MenuChoiceSprite()
        self.scoreboardChoice = MenuChoiceSprite()

        self.rocket_menu.textures.append(arcade.load_texture("images/rocket.png",scale=1.3))
        self.rocket_menu.textures.append(arcade.load_texture("images/rocket1.png",scale=1.3))
        self.startChoice.textures.append(arcade.load_texture("images/start.png"))
        self.startChoice.textures.append(arcade.load_texture("images/start1.png"))
        self.howToPlayChoice.textures.append(arcade.load_texture("images/howtoplay.png"))
        self.howToPlayChoice.textures.append(arcade.load_texture("images/howtoplay1.png"))
        self.scoreboardChoice.textures.append(arcade.load_texture("images/scoreboard.png"))
        self.scoreboardChoice.textures.append(arcade.load_texture("images/scoreboard1.png"))

    def config_sprites(self):
        self.config_sprites_texture()
        self.config_sprite_frame_rate()
        self.config_sprite_position()
        self.config_choice_selection()

    def config_sprites_texture(self):
        self.rocket_menu.set_texture(0)
        self.startChoice.set_texture(0)
        self.howToPlayChoice.set_texture(1)
        self.scoreboardChoice.set_texture(1)

    def config_sprite_frame_rate(self):
        self.rocket_menu.texture_change_frames = self._texture_frame_rate
        self.startChoice.texture_change_frames = self._texture_frame_rate
        self.howToPlayChoice.texture_change_frames = self._texture_frame_rate
        self.scoreboardChoice.texture_change_frames = self._texture_frame_rate

    def config_sprite_position(self):
        self.rocket_menu.center_x, self.rocket_menu.center_y = self._width//2, self._height//2 + 120
        self.startChoice.center_x, self.startChoice.center_y = self._width//2, self._height//2 - 90
        self.howToPlayChoice.center_x, self.howToPlayChoice.center_y = self._width//2, self._height//2 - 160
        self.scoreboardChoice.center_x, self.scoreboardChoice.center_y = self._width//2, self._height//2 - 230

    def config_choice_selection(self):
        self.rocket_menu.select()
        self.startChoice.select()
        self.howToPlayChoice.unselect()
        self.scoreboardChoice.unselect()

    def setup_choice_list(self):
        self.choice_list = arcade.SpriteList()
        self.choice_list.append(self.startChoice)
        self.choice_list.append(self.howToPlayChoice)
        self.choice_list.append(self.scoreboardChoice)

    def draw(self):
        self.rocket_menu.draw()
        self.choice_list.draw()

    def update(self):
        self.rocket_menu.update()
        self.rocket_menu.update_animation()
        self.update_choice_animation()

    def update_choice_animation(self):
        for i in range(len(self.choice_list)):
            is_selected = i == self.selecting_choice
            if is_selected:
                self.choice_list[i].update()
                self.choice_list[i].update_animation()
            else:
                self.choice_list[i].set_texture(1)

    def on_key_press(self,key):
        if key == arcade.key.DOWN:
            if self.selecting_choice < 2:
                self.selecting_choice += 1
            else:
                self.selecting_choice = 0
        elif key == arcade.key.UP:
            if self.selecting_choice > 0 :
                self.selecting_choice -= 1
            else:
                self.selecting_choice = 2
        elif key == arcade.key.ENTER:
            self.on_select(choices[self.selecting_choice])