import arcade

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._selected = False

    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False

    def is_selected(self):
        return self._selected
