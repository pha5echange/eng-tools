# eng_fam_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 29th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes genre files output from 'en_genre.py'
# Averages 'familiarity' of artists and produces values for genre, plus highest and lowest familiarity figures for each genre
# Writes results to 'results/versionNumber_eng_fam_data.txt'
# Writes run log to 'logs/versionNumber_eng_fam_log.txt'

# New version to deal with Musicbrainz ID in data files

# Run AFTER 'en_genre.py' has gathered 'genres/..'

# import packages
import os
from datetime import datetime
from collections import Counter

versionNumber = ("a01")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_fam_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
print ('\n' + 'Genre Average Familiarity | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# open file for output
resultsPath = os.path.join("results", versionNumber + '_eng_fam_data.txt')
processedResults = open(resultsPath, 'a')

for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreName, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	famValues = []

	# read lines from the file
 	for line in dataInput: 

		# split line and calculate hotttnesss total
		artist, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")
		famValues.append(float(familiarity))

	# close input file
	dataInput.close()

	artistTotal = float(len(famValues))
	famTotal = (sum(famValues))
	famAverage = (famTotal / artistTotal)
	famLow = (min(famValues))
	famHigh = (max(famValues))

	processedResults.write(str(genreName) + ',' + str(artistTotal) + ',' + str (famLow) + ',' + str(famAverage) + ',' + str(famHigh) + '\n')
	print ('Lowest familiarity for ' + str(genreName) + ' is ' + str(famLow))
	print ('Average familiarity for ' + str(genreName) + ' is ' + str(famAverage))
	print ('Highest familiarity for ' + str(genreName) + ' is ' + str(famHigh))
	print ('Artists within the genre ' + str(genreName) + ': ' + str(artistTotal))

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Genre Average Familiarity | ' + 'Version: ' + versionNumber + '\n' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/versionNumber_eng_fam_data.txt' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_eng_fam_data.txt')
