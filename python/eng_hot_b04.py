# eng_hot_b04.py
# Version b04
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes genre files output from 'en_genre.py'
# Averages 'hotttnesss' of artists and produces values for genre hotttness, plus highest and lowest hotttnesss figures for each genre
# Writes results to 'results/eng_hot_versionNumber_data.txt'
# Writes run log to 'logs/eng_hot_versionNumber_log.txt'

# This version deals with Musicbrainz ID in data files

# Run AFTER 'en_genre.py' has gathered 'genres/..'

# import packages
import os
from datetime import datetime
from collections import Counter

versionNumber = ("b04")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'eng_hot_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open file for output
resultsPath = os.path.join("results", 'eng_hot_' + versionNumber + '_data.txt')
processedResults = open(resultsPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
print ('\n' + 'Genre Average Hotttnesss | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreName, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	hotValues = []

	# read lines from the file
 	for line in dataInput: 

		# split line and calculate hotttnesss total
		artist, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")
		hotValues.append(float(hotness))

	# close input file
	dataInput.close()

	artistTotal = float(len(hotValues))
	hotTotal = (sum(hotValues))
	hotAverage = (hotTotal / artistTotal)
	hotLow = (min(hotValues))
	hotHigh = (max(hotValues))

	processedResults.write(str(genreName) + ',' + str(artistTotal) + ',' + str (hotLow) + ',' + str(hotAverage) + ',' + str(hotHigh) + '\n')
	print ('Lowest hotttnesss for ' + str(genreName) + ' is ' + str(hotLow))
	print ('Average hotttnesss for ' + str(genreName) + ' is ' + str(hotAverage))
	print ('Highest hotttnesss for ' + str(genreName) + ' is ' + str(hotHigh))
	print ('Artists within the genre ' + str(genreName) + ': ' + str(artistTotal))

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Genre Average Hotttnesss | ' + 'Version: ' + versionNumber + '\n' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/eng_hot_versionNumber_data.txt' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/eng_hot_versionNumber_data.txt')
