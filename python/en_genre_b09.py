# en_genre_b09.py
# Version b09
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 28th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Gets list of genres, and artists within genres, from Echonest utilising pyen
# Uses 'artist/search - genre =' method
# Results sorted by 'artist_start_year_asc'
# Gets a maximum of 1000 artists per genre (Echonest limit) with `years_active', `familiarity' and `hotttnesss' 
# Also grabs and writes MusicBrainzID - discards artists without this
# Produces ',' seperated output
# Writes each genres' data to a seperate file in 'genres/..' subdirectory
# Deletes empty files (i.e. those without artists with dates and MBID), but logs their presence
# Writes 'data/date_ratios.txt' (percentage of returned artists with date information) to facilitate the use of 'eng_cdr.py'
# Writes run log to 'logs/en_genre_versionNumber_log.txt'

# import packages
import os
import pyen
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# version
versionNumber = ("b09")

# define indexing variables for total artist responses
artistTotal = 0
artistWriteTotal = 0
emptyGenres = 0

# create 'genres' subdirectory if necessary
if not os.path.exists("genres"):
    os.makedirs("genres")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# open file for writing run info
logPath = os.path.join("logs", 'en_genre_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open file for writing 'calc_date_ratios'
resultsPath = os.path.join("data", 'date_ratios.txt')
dateRatios = open(resultsPath, 'w')

# get number of genres to trawl
runLog.write ('\n' + 'Echonest Genre Trawler | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Echonest Genre Trawler | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')
genreRequests = int(input ("Enter the maximum number of genres to trawl (last EN total was 1383): "))

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# open and read 'apikey.txt'
apiKeyFile = open('apikey.txt', 'r')
apiKey = str(apiKeyFile.read())

# call Echonest to get 'genres' response
en = pyen.Pyen(apiKey)
response_genre = en.get('genre/list', results = [genreRequests])

# Initiate 'removedGenres' list
removedGenres = []

# run through 'genres' writing results to 'genreArtistList'
for g in response_genre['genres']:

	# clean response and define name of genre
	genreName = str(g['name']).replace(",", "").replace(" ", "").replace("'","")

	# fix the `zouglou' problem
	if genreName.endswith('u'):
		genreName = genreName[:-1]

	# open file for writing artist data	
	genresPath = os.path.join("genres", genreName + '.txt')
	genreArtistList = open(genresPath, 'w')

	# define indexing variables for genre artist responses
	startIndex = 0
	results = 0
	artistGenreCount = 0
	artistGenreWrite = 0

	# call Echonest and get 'artists' within genres
	while results < 1000: 
		response_artist = en.get('artist/search', genre = g['name'], start = startIndex, sort = ['artist_start_year-asc'], bucket = ['years_active', 'familiarity', 'hotttnesss', 'id:musicbrainz'], results = ['100'])

		# run through 'artists' writing results to 'genreArtistList'
		for a in response_artist['artists']:

			# Cast floats (or try to)
			try:
				famiLiar = float(a['familiarity'])
			except:
				famiLiar = 0.0
				continue

			try:	
				hotNess = float(a['hotttnesss'])
			except:
				hotNess = 0.0
				continue

			# Retrieve MusicBrainz ID from the insanity and cast to string
			try:
				MbRetList = (a['foreign_ids'])
				MbRetStr = ''.join(map(str, MbRetList))
				junkA, junkB, junkC, junkD, notJunk = MbRetStr.split(":")
				cleanedNotJunk = notJunk.strip ("}'")
				MbID = str(cleanedNotJunk)
			except:
				MbID = str('')
				continue

			# Cast 'years_active' to string to allow for later clean-up (to show only first start year)
			yaString = str(a['years_active'])

			# If the 'years_active' string is empty (i.e. no data) don't write the artist to the file. Increment artistGenreCount (to note totals) but don't increment artistGenreWrite (to facilitate 'cdr.py').
			if yaString == "[]":
				artistGenreCount = artistGenreCount + 1 

			else:
				artistName = str(a['name']).replace(",", "")
				genreArtistList.write (artistName + ',' + yaString[12:16] + ',' + yaString[26:30] + ',' + str(famiLiar) + ',' + str(hotNess) + ',' + MbID + '\n')
				artistGenreWrite += 1
				artistGenreCount += 1

		results += 100
		startIndex += 100

	artistTotal = artistTotal + artistGenreCount
	artistWriteTotal = artistWriteTotal + artistGenreWrite

	genreArtistList.close()

	runLog.write ('Genre: ' + genreName + ' Artists returned: ' + str(artistGenreCount) + ' Artists written: ' + str(artistGenreWrite) + '\n')

	# display progress
	print ('\n' + genreName)
	print ('Genre Artists returned: ' + str(artistGenreCount))
	print ('Genre Artists written: ' + str(artistGenreWrite))

	# write to 'date_ratios.txt' if not empty
	if artistGenreWrite != 0:
		dateRatios.write (genreName + ',' + str(artistGenreCount) + ',' + str(artistGenreWrite) + '\n')

	# delete the genre file if it is empty
	if os.stat(genresPath).st_size == 0:
    		os.remove(genresPath)
    		emptyGenres += 1
    		runLog.write('The genre ' + genreName + ' has returned no artists. The file has been removed. ' + '\n')
    		removedGenres.append(genreName)

# End timing of run
endTime = datetime.now()

# close 'date_ratios' file
dateRatios.close()

# write results of run to log file
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('API Key: ' + apiKey + '\n')
runLog.write ('Genres requested: ' + str(genreRequests) + '\n')
runLog.write ('Genres returned: ' + str(len(response_genre['genres'])) + '\n')
runLog.write ('Artists with date information: ' + str(artistWriteTotal) + '\n')
runLog.write ('Empty genres: ' + str(emptyGenres) + '\n')
runLog.write ('Removed Genres: ' + str(removedGenres) + '\n')
runLog.write ('Total Artists returned: ' + str(artistTotal) + '\n')
runLog.write ('Duration of run: {}'.format(endTime - startTime) + '\n') 
runLog.write ('Genre data is saved to ../genres/' + '\n')
runLog.write ('Also writes ..data/date_ratios.txt to facilitate the use of eng_cdr.py' + '\n')
runLog.close ()

# write results of run to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('API Key: ' + apiKey)
print ('Genres requested: ' + str(genreRequests))
print ('Genres returned: ' + str(len(response_genre['genres'])))
print ('Artists with date information: ' + str(artistWriteTotal))
print ('Empty genres: ' + str(emptyGenres))
print ('Removed Genres: ' + str(removedGenres))
print ('Total Artists returned: ' + str(artistTotal))
print ('Duration of run: {}'.format(endTime - startTime)) 
print ('Genre data is saved to ../genres/')
print ('Also writes ..data/date_ratios.txt to facilitate the use of eng_cdr.py')
