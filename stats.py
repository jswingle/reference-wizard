def stats(verses):

	times = []
	highest = verses[0].time
	lowest = verses[0].time
	highest_verse = 0
	lowest_verse = 0

	for verse in verses:
		times.append(verse.time)

		if verse.time > highest:
			highest = round(verse.time,2)
			highest_verse = verse

		if verse.time < lowest:
			lowest = round(verse.time,2)
			lowest_verse = verse

	average = round((sum(times) / len(times)),2)

	print('The average time to recall the reference was ' + str(average) + ' seconds.')
	print('The verse you recalled the quickest was ' + highest_verse.reference() + ', in ' + str(highest) + ' seconds.')
	print('The verse you recalled the slowest was ' + lowest_verse.reference() + ', in ' + str(lowest) + ' seconds.')