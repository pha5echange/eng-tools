# timeslicer_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# September 20th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# REDESIGN
# Generates NEW genre files for each time-category to facilitate processing by existing methods

# Examines Echonest genre files and rewrites post-timeslice (to 'data/omegaYear/genres')
# Writes new artist numbers files based upon Omega Year of graph (to 'data/omegaYear')

# Run AFTER 'en_genre.py' (N.B. API has closed. Unzip 'genres..' zip file instead!)

# import packages
import os

versionNumber = ("a01")

emptyGenres = 0
removedGenres = []

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

print ('\n' + 'Artist Time-Slicer | ' + 'Version: ' + versionNumber + '\n')

# Get user input
print
dateIP = int(input ("Enter an Omega Year to remove artists that appear AFTER this date (or 2016 to leave data intact): "))

omegaYear = str(dateIP)

# create 'omega year' paths and subdirectories if necessary
omegaPath = str("data/" + omegaYear)
if not os.path.exists(omegaPath):
    os.makedirs(omegaPath)

omegaGenrePath = str("data/" + omegaYear + "/genres")
if not os.path.exists(omegaGenrePath):
	os.makedirs(omegaGenrePath)

# New Artist numbers file
newArtistNumsPath = os.path.join("data", omegaYear, omegaYear + '_artistNums.txt')
newArtistNums = open(newArtistNumsPath, 'w')
newArtistNums.write("Genre" + ',' + "Artists" + '\n')

# open file for writing log
logPath = os.path.join("logs", 'timeslicer_' + versionNumber + '_' + omegaYear + '_log.txt')
runLog = open(logPath, 'a')

# ..and begin..
runLog.write ('Artist Time-Slicer | ' + 'Version: ' + versionNumber + ' Omega Year: ' + omegaYear + '\n' + '\n')

# open files for reading
for index in range(len(fileNames)):

	artistCounter = 0

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")

	# New genre file
	newGenrePath = os.path.join("data", omegaYear, "genres", omegaYear + '_' + genreLabel + '.txt')
	newGenreFile = open(newGenrePath, 'w')
	
	for line in dataInput:

		# split line and append genreDates' with start date values
		artist, enid, start, end_date, familiarity, hotness, mbid = line.split(",")
		startDate = int(start)

		if dateIP != 0:
			if startDate <= dateIP:		
				newGenreFile.write(str(artist) + ',' + str(enid) + ',' + str(start) + ',' + str(end_date) + ',' + str(familiarity) + ',' + str(hotness) + ',' + str(mbid))
				artistCounter += 1

	# close input files
	dataInput.close()
	newGenreFile.close()

	if os.stat(newGenrePath).st_size == 0:
		os.remove(newGenrePath)
		emptyGenres += 1
		runLog.write('The genre ' + genreLabel + ' has no artists. The file has been removed. ' + '\n')
		removedGenres.append(genreLabel)

	if artistCounter != 0:
		newArtistNums.write(omegaYear + '_' + genreLabel + ',' + str(artistCounter) + ',' + '\n')

newArtistNums.close()

# write results of run to log file
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Removed Genres: ' + str(removedGenres) + '\n')
runLog.write ('Empty genres: ' + str(emptyGenres) + '\n')
runLog.close ()

# write results of run to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Removed Genres: ' + str(removedGenres))
print ('Empty genres: ' + str(emptyGenres))
