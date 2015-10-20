# eng_graph_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 17th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Examines Echonest genre lists
# Creates a set for each genre, and adds artist info. as elements
# Finds shared artists to facilitate node-list generaton 

# Run AFTER 'en_genre.py'

# import packages
import os
import resource
from datetime import datetime

versionNumber = ("a01")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# open file for data output
setDataPath = os.path.join("data", 'genre_sets.txt')
setData = open(setDataPath, 'w')

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_graph_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data Node List Maker | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Node List Maker | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

genreCount = 0

# open files for reading
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")

	# create set for genre
	setName = genreLabel
	setName = set()
	
	# read lines from the file and assign each to the set
	for line in dataInput:

		content = str(line.strip("\n"))
		setName.add (content)

	# close input file
	dataInput.close()

	setData.write ('\n' + genreLabel + '\n' + str(setName) + '\n')
	print (genreLabel + '\n' + str(setName) + '\n')

	genreCount += 1

# End timing of run
endTime = datetime.now()

memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Genres: ' + str(genreCount) + '\n')
runLog.write ('Memory: ' + str(memUseMb) + 'Mb' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genres: ' + str(genreCount))
print ('Memory: ' + str(memUseMb) + 'Mb')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
