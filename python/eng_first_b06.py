# eng_first_b06.py
# Version b06
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# February 21st 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines Echonest genre lists
# Finds first instance of a band start date in a genre
# Reads files from 'genres' subdirectory
# Writes results to 'data/first_instamces.txt'
# Writes run log to 'logs/eng_first_versionNumber_log.txt'

# New version to deal with Musicbrainz ID in data files

# Run AFTER 'en_genre.py'

# import packages
import os
from datetime import datetime

versionNumber = ("b06")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# open file for writing log
logPath = os.path.join("logs", 'eng_first_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data First Instance Finder | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data First Instance Finder | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# open files for reading
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	
	# read first line from the file
	first_line = dataInput.readline()

	# split line and append genreDates' with start date values
	artist, start, end_date, familiarity, hotness, mbid = first_line.split(",")
	startDate = int(start)

	# close input file
	dataInput.close()

	# open file for data output
	firstInstancePath = os.path.join("data", 'first_instances.txt')
	firstInstance = open(firstInstancePath, 'a')

	# write first instance in a genre
	firstInstance.write(str(genreLabel) + ',' + str(startDate) + ',' + '\n')

	# write results of run to 'runLog'
	runLog.write('\n' + 'Genre: ' + str(genreLabel) + '\n')
	runLog.write('Artist: ' + str(artist) + '\n')
	runLog.write('First Instance: ' + str(startDate) + '\n' + '\n')

	# close file
	firstInstance.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
