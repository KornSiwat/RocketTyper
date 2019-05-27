import string
from random import choice

class WordManager():
    ''' class for WordManager which is responsible for managing the word and generate the word '''

    def __init__(self, word_dict, level=1):
        ''' create attributes for wordmanager instance '''

        self._level = level
        self._used = []
        self._unused = list(string.ascii_lowercase)
        self._long_word = dict()
        self._short_word = dict()
        for alphabet in word_dict:
            self._short_word[alphabet] = []
            self._long_word[alphabet] = []
            for word in word_dict[alphabet]:
                if len(word) >= 5:
                    self._long_word[alphabet].append(word)
                else:
                    self._short_word[alphabet].append(word)

    def _get_short(self):
        ''' return a dictionary object containing words with less than five characters '''

        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def _get_long(self):
        ''' return a dictionary object containing words with more than or equal to five characters '''

        result = dict()
        for alphabet in self._unused:
            result[alphabet] = self._short_word[alphabet]
        return result

    def generate(self):
        ''' return a string of word random based on level attribute and also add the string of first character of it to the used attribute and remove it from the unused attribute '''

        alphabet = choice(self._unused)
        self._used.append(alphabet)
        self._unused.remove(alphabet)
        return choice(self._short_word[alphabet] + self._long_word[alphabet] * self._level)

    def set_level(self, level):
        ''' assign the level attribute with int value from level parameter '''

        self._level = level

    def recycle(self, alphabet):
        ''' remove the string from alphabet parameter from used attribute and add it to the unused attribute '''

        self._unused.append(alphabet)
        self._used.remove(alphabet)

