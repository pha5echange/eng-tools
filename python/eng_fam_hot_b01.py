# eng_fam_hot_b01.py
# Version b01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# February 22nd 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes genre files output from 'en_genre.py'
# Averages proprietary EN metrics 'familiarity' and 'hotttnesss' of artists and produces values for genre, plus highest and lowest familiarity and hotttnesss figures for each genre
# Writes results to 'results/eng_fam_hot_versionNumber_data.txt'
# Writes run log to 'logs/eng_fam_hot_versionNumber_log.txt'

# This version deals with Musicbrainz IDs in data files

# Run AFTER 'en_genre.py' has gathered 'genres/..'

# import packages
import os
from datetime import datetime
from collections import Counter

versionNumber = ("b01")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'eng_fam_hot_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open files for output and write first line
famResultsPath = os.path.join("results", 'eng_fam_' + versionNumber + '_data.txt')
processedFamResults = open(famResultsPath, 'a')
processedFamResults.write("Genre" + ',' + "Total Artists" + ',' + "Familiarity - Low" + ',' + "Familiarity - Mean" + ',' + "Familiarity - High" + '\n')

hotResultsPath = os.path.join("results", 'eng_hot_' + versionNumber + '_data.txt')
processedHotResults = open(hotResultsPath, 'a')
processedHotResults.write("Genre" + ',' + "Total Artists" + ',' + "Hotttnesss - Low" + ',' + "Hotttnesss - Mean" + ',' + "Hotttnesss - High" + '\n')


# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
print ('\n' + 'Genre Familiarity and Hotttnesss | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreName, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	famValues = []
	hotValues = []

	# read lines from the file
 	for line in dataInput: 

		# split line and calculate totals
		artist, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")
		famValues.append(float(familiarity))
		hotValues.append(float(hotness))

	# close input file
	dataInput.close()

	# Calculate values and display/write
	artistTotal = float(len(famValues))
	famTotal = (sum(famValues))
	famAverage = (famTotal / artistTotal)
	famLow = (min(famValues))
	famHigh = (max(famValues))
	hotTotal = (sum(hotValues))
	hotAverage = (hotTotal / artistTotal)
	hotLow = (min(hotValues))
	hotHigh = (max(hotValues))

	processedFamResults.write(str(genreName) + ',' + str(artistTotal) + ',' + str (famLow) + ',' + str(famAverage) + ',' + str(famHigh) + '\n')
	print
	print ('Artists within the genre ' + str(genreName) + ': ' + str(artistTotal))
	print ('Lowest familiarity for ' + str(genreName) + ' is ' + str(famLow))
	print ('Average familiarity for ' + str(genreName) + ' is ' + str(famAverage))
	print ('Highest familiarity for ' + str(genreName) + ' is ' + str(famHigh))

	processedHotResults.write(str(genreName) + ',' + str(artistTotal) + ',' + str (hotLow) + ',' + str(hotAverage) + ',' + str(hotHigh) + '\n')
	print ('Lowest hotttnesss for ' + str(genreName) + ' is ' + str(hotLow))
	print ('Average hotttnesss for ' + str(genreName) + ' is ' + str(hotAverage))
	print ('Highest hotttnesss for ' + str(genreName) + ' is ' + str(hotHigh))

# close files
processedFamResults.close()
processedHotResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Genre Familiarity and Hotttnesss | ' + 'Version: ' + versionNumber + '\n' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
