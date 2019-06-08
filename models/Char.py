class Char():
    def __init__(self, char):
        self._char = char
        self._active = True

    def is_typed(self):
        self._active = False

    def is_active(self):
        return self._active

    def get_char(self):
        return self._char

    def __str__(self):
        return self._char
