# en_genre_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 13th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Gets list of genres, and artists within genres, from Echonest utilising pyen
# Uses 'artist/search - genre =' method
# Results sorted by 'artist_start_year_asc'
# Gets a maximum of 1000 artists per genre (Echonest limit) with `years_active' and `hotttnesss' data
# Produces '^' seperated output, and only writes artists where 'years_active' date information is provided
# Writes each genres data to a seperate file in 'genres' subdirectory
# Writes 'data/date_ratios.txt' (percentage of returned artists with date information) to facilitate the use of 'eng_cdr.py'
# Writes run log to 'logs/versionNumber_engenre_log.txt'

# import packages
import os
import pyen
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# version
versionNumber = ("b02")

# define indexing variables for total artist responses
artistTotal = 0
artistWriteTotal = 0

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
logPath = os.path.join("logs", versionNumber + '_engenre_log.txt')
runLog = open(logPath, 'a')

# open file for writing 'calc_date_ratios'
resultsPath = os.path.join("data", 'date_ratios.txt')
dateRatios = open(resultsPath, 'w')

# get number of genres to trawl
runLog.write ('\n' + 'Echonest Genre Trawl | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Echonest Genre Trawl | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')
genreRequests = int(input ("Enter the maximum number of genres to trawl (latest total is 1370): "))

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# open and read 'apikey.txt'
apiKeyFile = open('apikey.txt', 'r')
apiKey = str(apiKeyFile.read())

# call Echonest to get 'genres' response
en = pyen.Pyen(apiKey)
response_genre = en.get('genre/list', results = [genreRequests])

# run through 'genres' writing results to 'genreArtistList'
for g in response_genre['genres']:

	# open file for writing artist data
	genresPath = os.path.join("genres", str(g['name']) + '.txt')
	genreArtistList = open(genresPath, 'w')

	# define indexing variables for genre artist responses
	startIndex = 0
	results = 0
	artistGenreCount = 0
	artistGenreWrite = 0

	# call Echonest and get 'artists' within genres
	while results < 1000: 
		response_artist = en.get('artist/search', genre = g['name'], start = startIndex, sort = ['artist_start_year-asc'], bucket = ['years_active', 'hotttnesss'], results = ['100'])

		# run through 'artists' writing results to 'genreArtistList'
		for a in response_artist['artists']:


			# Cast 'Hotttnesss' to float and store in hotNess
			hotNess = float(a['hotttnesss'])

			# Get string of 'years_active' to allow for later clean-up (to show only first start year)
			yaString = str(a['years_active'])

			# If the 'years_active' string is empty (i.e. no data) don't write the artist to the file
			if yaString == "[]":
				artistGenreCount = artistGenreCount + 1 

			else:
				# write to '^' seperated file (as circumflex/caret does not appear in any band name found so far)
				genreArtistList.write (a['name'] + '^' + yaString[12:16] + '^' + yaString[26:30] + '^' + str(hotNess) + '\n')
				artistGenreWrite = artistGenreWrite + 1
				artistGenreCount = artistGenreCount + 1

		results = results + 100
		startIndex = startIndex + 100

	artistTotal = artistTotal + artistGenreCount
	artistWriteTotal = artistWriteTotal + artistGenreWrite

	genreArtistList.close()

	runLog.write ('Genre: ' + g['name'] + ' Artists returned: ' + str(artistGenreCount) + ' Artists written: ' + str(artistGenreWrite) + '\n')
	dateRatios.write (g['name'] + '^' + str(artistGenreCount) + '^' + str(artistGenreWrite) + '\n')

	# display progress
	print ('\n' + g['name'])
	print ('Genre Artists returned: ' + str(artistGenreCount))
	print ('Genre Artists written: ' + str(artistGenreWrite) + '\n')

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
runLog.write ('Artists written: ' + str(artistWriteTotal) + '\n')
runLog.write ('Total Artists returned : ' + str(artistTotal) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n') 
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
print ('Artists written: ' + str(artistWriteTotal))
print ('Total Artists returned : ' + str(artistTotal))
print ('Duration of run : {}'.format(endTime - startTime)) 
print ('Genre data is saved to ../genres/')
print ('Also writes ..data/date_ratios.txt to facilitate the use of eng_cdr.py')
