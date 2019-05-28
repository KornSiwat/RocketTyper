class ReadWordFile():
    ''' class for ReadWordFile which is responsible for reading the file'''

    def __init__(self, file_name=''):
        ''' open the file from the path given by file_name parameter then read each lines to get words and categorized them and assign to categorized_word attribute '''

        with open(file_name, 'r') as Fin:
            self._raw_word = [x.strip() for x in Fin.readlines()]
        self._categorized_word = {}
        for word in self._raw_word:
            if word[0].lower() not in self._categorized_word:
                self._categorized_word[word[0].lower()] = [word]
            else:
                self._categorized_word[word[0].lower()].append(word)

    def get_categorized_list(self):
        ''' return dictionary object from categorized_word attribute '''

        return self._categorized_word