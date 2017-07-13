# eng_MBdate_a06.py
# Version a06
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# July 13th 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines Echonest genre lists
# Checks start-dates against MusicBrainz <begin> tags
# Writes corrected genre files
# REMOVES artists with no date information in MusicBrainz

# import packages
import os
from datetime import datetime

appName = ("eng_MBdate_")
versionNumber = ("a06")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
	os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
	os.makedirs("data")

# Define path to MusicBrainz XML artist file
xmlPath = os.path.join("data", 'mb_artist_xml.txt')

# open file for writing log
logPath = os.path.join("logs", appName + versionNumber + '_log.txt')
runLog = open(logPath, 'w')

# open files for writing dictionaries
mbDictPath = os.path.join("data", "mbDict_" + versionNumber + "_.txt")
mbDictFile = open(mbDictPath, 'w')

enDictPath = os.path.join("data", "enDict_" + versionNumber + "_.txt")
enDictFile = open(enDictPath, 'w')

genreDictPath = os.path.join("data", "genreDict_" + versionNumber + "_.txt")
genreDictFile = open(genreDictPath, 'w')

# create 'datadGenres' subdirectory if necessary
#if not os.path.exists("datedGenres"):
#	os.makedirs("datedGenres")

#dateCheckCounter = 0

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
#runLog.write ('\n' + 'Genre Data Date Checker | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Date Checker | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# Read XML file into dictionary {xMbId:begin}
mbDict = {}
with open(xmlPath) as xmlFile:
	for line in xmlFile:
		xMbId, mbType, begin, mbCountry, mbTag = line.split("^")
		mbType = mbType.strip()
		begin = begin.strip()
		xMbId = xMbId.strip()

		if mbType == "Person":
			try:
				strChars = len(begin)
				begin = begin[:4]
				beginInt = int(begin)
				if strChars > 4:
					personBegin = beginInt + 20
				else:
					personBegin = beginInt
				begin = str(personBegin)
			except:
				pass

		mbDict[xMbId] = begin

print
print(mbDict)
mbDictFile.write(str(mbDict))
print

# Read EN genre files into dictionary {mbid:start}
enDict = {}
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	dataInput = open(pathname, "r")

	#datedGenrePath = os.path.join("datedGenres", fileNames[index])
	#datedGenreFile = open(datedGenrePath, 'a')
	
	# read lines from file
	for line in dataInput:
		artist, enid, start, end_date, familiarity, hotness, mbid = line.split(",")
		mbid = mbid.strip()

		if mbid in mbDict:
			enDict[mbid] = start
			print ("Written: " + str(mbid))
			runLog.write (str(mbid) + '\n')
		else:
			print ("Not written: " + str(mbid))
			runLog.write ("Not written: " + str(mbid) + '\n')

print
print(enDict)
enDictFile.write(str(enDict))
print

# Compare the dictionaries
print
print("Comparing dictionaries... ")
print ("MB Dictionary Entries: " + str(len(mbDict)))
print ("EN Dictionary Entries: " + str(len(enDict)))
print("Returns '0' if both dictionaries are equal, '-1' if mbDict < enDict, and '1' if mbDict > enDict")
print(cmp(mbDict, enDict))
print

# Create updated dictionary
genreDictCounter = 0
genreDict = {}

print ("Iterating through... See you tmrw... ")

for key, value in mbDict.iteritems():
	for key, value in enDict.iteritems(): 
		try:
			if mbDict[key] == "":
				genreDict[key] = enDict[key]
			else:
				genreDict[key] = mbDict[key]

			genreDictCounter += 1
			print(str(genreDictCounter))

		except:
			pass
print
print (genreDict)
genreDictFile.write(str(genreDict))
print

# Recompare the dictionaries
print
print("Recomparing dictionaries... ")
print ("MB Dictionary Entries: " + str(len(mbDict)))
print ("EN Dictionary Entries: " + str(len(enDict)))
print ("Genre (generated) Dictionary: " + str(len(genreDict)))

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ("MB Dictionary Entries: " + str(len(mbDict)) + '\n')
runLog.write ("EN Dictionary Entries: " + str(len(enDict)) + '\n')
runLog.write ("Genre (generated) Dictionary: " + str(len(genreDict)) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ("MB Dictionary Entries: " + str(len(mbDict)))
print ("EN Dictionary Entries: " + str(len(enDict)))
print ("Genre (generated) Dictionary: " + str(len(genreDict)))
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
