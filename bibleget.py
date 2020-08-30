import requests
import bs4
import time
from books import bible_books,book_abbreviations
from verse import Verse

start_time = time.time()

# User selects a book and translation - at the moment, this functionality is super simplistic but very easy to expand

def select_book():

	valid_selection = False

	while not valid_selection:
	    book = input('Please type the name of a book of the Bible.\n')
	    if book in bible_books:
	        valid_selection = True

	return book

def select_translation():

	valid_translation = False

	while not valid_translation:
	    translation = input('Please select a translation to use. Options are NIV, ESV, or KJV.\n')
	    translation = translation.upper()
	    if translation in ['NIV','ESV','KJV']:
	        valid_translation = True

	return translation

def add_book(book,translation):

	chapters = []
	verses = []

	chapters.extend(range(1,(bible_books[book] + 1)))

	for chapter in chapters:

	    url = 'https://www.biblegateway.com/passage/?search=' + book + '+' + str(chapter) + '&version=' + translation
	    html = requests.get(url)
	    soup = bs4.BeautifulSoup(html.text,'lxml')

	# We don't want section titles, but in the HTML they are labeled similarly as the main text, so we get rid of them first

	    section_headers = soup.find_all('h3')
	    for section in section_headers:
	        section.decompose()

	    verse = 1
	    missed_verse = False

	    while True:
	        verse_lookup = 'text ' + book_abbreviations[book] + '-' + str(chapter) + '-' + str(verse)
	        selection = soup.find_all(class_=verse_lookup)

	# Checks for more than one missed verse in a row before breaking to next chapter. This covers vss. that are only in the footnotes.

	        if not selection:
	        	if missed_verse:
	        		break
	        	missed_verse = True
	        	verse += 1
	        	continue

	# Some verses use multiple "Matt-1-1" tags, so verse_text needs to be defined as a blank string outside the upcoming loop

	        verse_text = ''

	        for item in selection:

	            for span in item('span'):

	# These two if statements keep .decompose() from deleting red letter text or the divine name LORD

	                if 'class="woj' not in str(span):
	                    if 'class="small-caps' not in str(span):
	                        span.decompose()

	            for sup in item('sup'):
	                sup.decompose()

	# Here we do += to ensure all HTML tags attached to one verse get added together as part of one verse.

	            verse_text += item.getText() + ' '

	        verses.append(Verse(book,chapter,verse,translation,verse_text[:-1],0))

	        verse += 1

	return verses