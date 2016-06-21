# eng_en_mb_map_a02.py
# Version a02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# June 21st 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines Echonest genre lists
# Generates an EchoNest-MusicBrainz artist ID mapping
# Writes ArtistName ^ enid ^ mbid

# import packages
import os
import sys

versionNumber = ("a02")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# ..and begin..
print ('\n' + 'EchoNest-to-MusicBrainz Artist ID Mapper | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# open file for data output
enMbMapPath = os.path.join("data", 'en_mb_map_' + versionNumber + '.txt')
enMbMap = open(enMbMapPath, 'w')

# open files for reading
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
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
