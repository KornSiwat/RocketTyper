import arcade
from .Char import Char

class Word():
    ''' class for the word attached to the back of the missile '''

    def __init__(self,x ,y, word):
        ''' create attributes of Word instance '''

        self._x = x
        self._y = y
        self._word = word
        self._char_list = list(map(lambda x: Char(x), word))
        self._current_char = self._char_list[0]
        self._completed = False
        self._selected = False

    def draw(self):
        ''' draw the word on the screen with different color for the typed character and the untyped '''

        white_text = self._word
        red_text = ''
        for char in self._char_list:
            if char.is_active()== True:
                red_text += ' '
            else:
                red_text += char.get_char()
        arcade.draw_text(white_text, self._x, self._y, color=arcade.color.WHITE, font_size=16)
        arcade.draw_text(red_text, self._x, self._y, color=arcade.color.RED, font_size=16)

    def update_pos(self, new_x):
        ''' update the posion of the text to be drawn '''

        self._x = new_x

    def update_key(self, key):
        ''' check if the active character matched with the key parameter by using check_key function and also check if the word is completed '''

        for char in self._char_list:
            if char.is_active() == True:
                self._current_char = char
                break
        else:
            self._completed = True
        self._check_key(key)

    def _check_key(self, key):
        ''' convert the first untyped character of the word from string to unicode to compare with the value from key parameter
        and call is_typed function of that character instance if the value matched the change the status of word selected to True
        '''

        if key == ord(self._current_char.get_char()):
            self._current_char.is_typed()
            self._selected = True

    def is_selected(self):
        ''' return the status whether the word is being typing or not '''

        return self._selected

    def is_completed(self):
        ''' return the status whether all the character of the word has been typed or not '''

        return self._completed

    def get_current_char(self):
        ''' return the character instance that is waiting to be typed '''

        return self._current_char

    def print_word(self):
        ''' show the word in the command line '''

        for char in self._char_list:
            print(char)