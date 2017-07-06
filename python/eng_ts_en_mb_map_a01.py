# eng_ts_en_mb_map_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# July 6th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines TimeSliced Echonest genre lists
# Generates an Omega Year specific EchoNest-MusicBrainz artist ID mapping
# Writes ArtistName ^ enid ^ mbid

# import packages
import os
import sys

versionNumber = ("a01")
appName = ("eng_ts_en_mb_map_")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# ..and begin..
print ('\n' + 'EchoNest-to-MusicBrainz Artist ID Mapper | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# Get user input
print
dateIP = int(input ("Enter an Omega Year for this mapping (or 2015 for full map): "))
omegaYear = str(dateIP)

# define path to 'genres' subdirectory
fileNamesPath = os.path.join("ts_data", omegaYear, "genres")
fileNames = os.listdir(fileNamesPath)

# open file for data output
enMbMapPath = os.path.join("data", omegaYear + '_en_mb_map_' + versionNumber + '.txt')
enMbMap = open(enMbMapPath, 'w')

# open files for reading
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("ts_data", omegaYear, "genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	
	for line in dataInput:

		# split line and append genreDates' with start date values
		artist, enid, start, end_date, familiarity, hotness, mbid = line.split(",")
		enMbMap.write(str(artist) + '^' + str(enid) + '^' + str(mbid))

	# close input file
	dataInput.close()

# close file
enMbMap.close()

# Remove duplicates
lines = open(enMbMapPath, 'r').readlines()
lines_set = set(lines)
out = open(enMbMapPath, 'w')

for line in sorted(lines_set):
	out.write(line)

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ("OMega Year: " + omegaYear)
