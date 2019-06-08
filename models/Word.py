import arcade
from .Char import Char


class Word():
    def __init__(self, x, y, word):
        self._x = x
        self._y = y
        self._word = word
        self._char_list = list(map(lambda x: Char(x), word))
        self._current_char = self._char_list[0]
        self._completed = False
        self._selected = False

    def draw(self):
        white_text = self._word
        red_text = ''
        for char in self._char_list:
            if char.is_active() == True:
                red_text += ' '
            else:
                red_text += char.get_char()
        arcade.draw_text(white_text, self._x, self._y,
                        color=arcade.color.WHITE, font_size=16)
        arcade.draw_text(red_text, self._x, self._y,
                        color=arcade.color.RED, font_size=16)

    def update_pos(self, new_x):
        self._x = new_x

    def update_key(self, key):
        for char in self._char_list:
            if char.is_active():
                self._current_char = char
                break
        else:
            self._completed = True
        self._check_key(key)

    def _check_key(self, key):
        key_match = key == ord(self._current_char.get_char())
        if key_match:
            self._current_char.is_typed()
            self._selected = True

    def is_selected(self):
        return self._selected

    def is_completed(self):
        return self._completed

    def get_current_char(self):
        return self._current_char
