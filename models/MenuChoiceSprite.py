import arcade

class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    ''' class for the menu choice sprite'''

    def __init__(self, *args, **kwargs):
        ''' create an attribute of MenuChoice instance'''

        super().__init__(*args, **kwargs)
        self._selected = False

    def select(self):
        ''' call when the choice is chosen '''
        self._selected = True

    def unselect(self):
        ''' call when the choice is not chosen'''
        self._selected = False

    def is_selected(self):
        ''' return the status whether the instance is being selected or not '''
        return self._selected