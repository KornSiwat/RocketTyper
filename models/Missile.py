import arcade
from .Word import Word

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
