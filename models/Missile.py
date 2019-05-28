import arcade
from .Word import Word

class Missile(arcade.Sprite):
    def __init__(self, x, y, word, target, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.append_texture(arcade.load_texture('images/missile.png'))
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.missile_target = target
        self.distance_from_missile = 60
        self.first_alphabet = word[0]
        self.word = Word(self.right , self.center_y - 5, word)
        self.selected = False
        self.active = True
        self.hit = True
        self.speed = speed

    def is_selected(self):
        return self.selected

    def explode(self):
        self.active = False
        self.selected = False

    def draw_with_word(self):
        self.draw()
        self.word.draw()

    def update_position(self):
        reach_rocket = self.left < self.missile_target
        if not reach_rocket:
            self.center_x -= self.speed
            self.word.update_pos(self.center_x + self.distance_from_missile)
            self.check_word()
        else:
            self.explode()

    def update_key(self, key):
        self.word.update_key(key)

    def check_word(self):
        if self.word.is_selected():
            self.selected = True

        if self.word.is_completed():
            self.hit = False
            self.explode()

    def do_damage(self):
        return self.hit

    def is_active(self):
        return self.active

    def get_first_alphabet(self):
        return self.first_alphabet
