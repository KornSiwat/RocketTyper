from models import ReadWordFile

a = ReadWordFile('word/word.txt')
print(a.raw_word)
print(a.catagorized_word)