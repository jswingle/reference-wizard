from bibleget import select_book,select_translation,add_book
from books import bible_books,book_abbreviations
from stats import stats
import random
import time
import math

book = select_book()
print('\n')
translation = select_translation()
print('\n')

practice_set = add_book(book,translation)
random.shuffle(practice_set)

for verse in practice_set:
	start = time.time()
	input(verse.book + ' ' + str(verse.chapter) + ':' + str(verse.verse) + ' ' + verse.translation + '\nPress ENTER when you know the start of the verse.\n')
	verse.time = (time.time() - start)
	print(verse.text + '\n')

stats(practice_set)