import requests
import bs4
import time

start_time = time.time()

# BibleGateway uses the full name of books in URLs, but an abbreviated version in the HTML. Chapter numbers per book also defined.

bible_books = {'Genesis':50,'Exodus':40,'Leviticus':27,'Numbers':36,'Deuteronomy':34,'Joshua':24,'Judges':21,'Ruth':4,'1 Samuel':31,'2 Samuel':24,'1 Kings':22,'2 Kings':25,'1 Chronicles':29,'2 Chronicles':36,'Ezra':10,'Nehemiah':13,'Esther':10,'Job':42,'Psalms':150,'Proverbs':31,'Ecclesiastes':12,'Song of Songs':8,'Isaiah':66,'Jeremiah':52,'Lamentations':5,'Ezekiel':48,'Daniel':12,'Hosea':14,'Joel':3,'Amos':9,'Obadiah':1,'Jonah':4,'Micah':7,'Nahum':3,'Habakkuk':3,'Zephaniah':3,'Haggai':2,'Zechariah':14,'Malachi':4,'Matthew':28,'Mark':16,'Luke':24,'John':21,'Acts':28,'Romans':16,'1 Corinthians':16,'2 Corinthians':13,'Galatians':6,'Ephesians':6,'Philippians':4,'Colossians':4,'1 Thessalonians':5,'2 Thessalonians':3,'1 Timothy':6,'2 Timothy':4,'Titus':3,'Philemon':1,'Hebrews':13,'James':5,'1 Peter':5,'2 Peter':3,'1 John':5,'2 John':1,'3 John':1,'Jude':1,'Revelation':22}

book_abbreviations = {'Genesis':'Gen','Exodus':'Exod','Leviticus':'Lev','Numbers':'Num','Deuteronomy':'Deut','Joshua':'Josh','Judges':'Judg','Ruth':'Ruth','1 Samuel':'1Sam','2 Samuel':'2Sam','1 Kings':'1Kgs','2 Kings':'2Kgs','1 Chronicles':'1Chr','2 Chronicles':'2Chr','Ezra':'Ezra','Nehemiah':'Neh','Esther':'Esth','Job':'Job','Psalms':'Ps','Proverbs':'Prov','Ecclesiastes':'Eccl','Song of Songs':'Song','Isaiah':'Isa','Jeremiah':'Jer','Lamentations':'Lam','Ezekiel':'Ezek','Daniel':'Dan','Hosea':'Hos','Joel':'Joel','Amos':'Amos','Obadiah':'Obad','Jonah':'Jonah','Micah':'Mic','Nahum':'Nah','Habakkuk':'Hab','Zephaniah':'Zeph','Haggai':'Hag','Zechariah':'Zech','Malachi':'Mal','Matthew':'Matt','Mark':'Mark','Luke':'Luke','John':'John','Acts':'Acts','Romans':'Rom','1 Corinthians':'1Cor','2 Corinthians':'2Cor','Galatians':'Gal','Ephesians':'Eph','Philippians':'Phil','Colossians':'Col','1 Thessalonians':'1Thess','2 Thessalonians':'2Thess','1 Timothy':'1Tim','2 Timothy':'2Tim','Titus':'Titus','Philemon':'Phlm','Hebrews':'Heb','James':'Jas','1 Peter':'1Pet','2 Peter':'2Pet','1 John':'1John','2 John':'2John','3 John':'3John','Jude':'Jude','Revelation':'Rev'}

chapters = [1,2]
verses_text = {}

# User selects a book and translation - at the moment, this functionality is super simplistic but very easy to expand

valid_selection = False
valid_translation = False

while not valid_selection:
    book = input('Please type the name of a book of the Bible.\n')
    if book in bible_books:
        valid_selection = True

while not valid_translation:
    translation = input('Please select a translation to use. Options are NIV, ESV, or KJV.\n')
    translation = translation.upper()
    if translation in ['NIV','ESV','KJV']:
        valid_translation = True

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

    while True:
        verse_lookup = 'text ' + book_abbreviations[book] + '-' + str(chapter) + '-' + str(verse)
        selection = soup.find_all(class_=verse_lookup)

# This loop break strategy hasn't yet been tested on chapters where the verse is only in the footnotes

        if not selection:
            break

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

        verses_text[book + ' ' + str(chapter) + ':' + str(verse)] = verse_text[:-1]

        verse += 1


# Writes the output to a text file named after the book of the Bible selected

filename = book + '.txt'

with open(filename,mode="w") as output:

    for item in verses_text.items():
        output.write(item[0] + ' ' + translation + ' - ' + item[1] + '\n')

print('It took ' + str(time.time() - start_time) + ' seconds to complete.')