class Char():
    ''' class for character of the word attached to the missile '''

    def __init__(self,char):
        ''' create attributes of a Char instance '''

        self._char = char
        self._active = True    

    def is_typed(self):
        ''' call when the value of the character matched with the input key to change the active status of the instance '''

        self._active = False

    def is_active(self):
        ''' return whethe the char instance has been typed or not '''

        return self._active

    def get_char(self):
        ''' return the string value from the char attribute of the instance '''

        return self._char

    def __str__(self):
        ''' return the string of char attribute of the instance when the instance is called by print funcition '''

        return self._char