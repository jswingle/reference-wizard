class Verse():
	def __init__(self,book,chapter,verse,translation,text,time):
		self.book = book
		self.chapter = chapter
		self.verse = verse
		self.translation = translation
		self.text = text

	def __str__(self):
		full_verse = self.book + ' ' + self.chapter + ':' + self.verse + ' ' + self.translation + ' - ' + self.text
		return full_verse

	def reference(self):
		ref = self.book + ' ' + str(self.chapter) + ':' + str(self.verse)
		return ref