# eng_MBdate_a15.py
# Version a15
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# Aug 22nd 2017

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines Echonest genre lists
# Checks start-dates against MusicBrainz XML <begin> tags
# Gets country-of-origin information for each artist
# Writes corrected genre files, and *Dict.txt files for verification
# REMOVES artists with no date information (or `????'' date information) in MusicBrainz
# Checks for MB ID changes in returns, and corrects (replaces with newest MBID)

# import packages
import os
from datetime import datetime

appName = ("eng_MBdate_")
versionNumber = ("a15")

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

# open file for writing `missing'
missPath = os.path.join("data", appName + versionNumber + '_enDict_missing.txt')
enMiss = open(missPath, 'w')

# open files for writing dictionaries
mbDictPath = os.path.join("data", "mbDict_" + versionNumber + ".txt")
mbDictFile = open(mbDictPath, 'w')

countryDictPath = os.path.join("data", "countryDict_" + versionNumber + ".txt")
countryDictFile = open(countryDictPath, 'w')

compDictPath = os.path.join("data", "compDict_" + versionNumber + ".txt")
compDictFile = open(compDictPath, 'w')

enDictPath = os.path.join("data", "enDict_" + versionNumber + ".txt")
enDictFile = open(enDictPath, 'w')

genreDictPath = os.path.join("data", "genreDict_" + versionNumber + ".txt")
genreDictFile = open(genreDictPath, 'w')

# create 'datedGenres' subdirectory if necessary
if not os.path.exists("MbGenres"):
	os.makedirs("MbGenres")

#dateCheckCounter = 0

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data Date Correcter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Date Correcter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# Dict for ID comparison
compDict = {}

# Dict for Countries
countryDict = {}

# Read MusicBrainz XML file into dictionary {xMbId:begin}
mbDict = {}
with open(xmlPath) as xmlFile:
	for line in xmlFile:
		origID, xMbId, mbType, begin, mbCountry, mbTag = line.split("^")
		origID = origID.strip()
		mbType = mbType.strip()
		begin = begin.strip()
		xMbId = xMbId.strip()
		mbCountry = mbCountry.strip()

		# Populate compDict for later changed-ID repairs 
		if origID != xMbId:
			compDict[origID] = xMbId
			print ("Written to compDict: " + str(xMbId))
			runLog.write ("Written to compDict " + str(origID) + ':' + str(xMbId) + '\n')

		# Fix up dates
		if not begin:
			strChars = 0
		else:
			strChars = len(begin)
			begin = begin[:4]
			if begin == "????":
				strChars = 0
			else:
				try:
					beginInt = int(begin)
				except:
					pass

		# Fix up dates for `Person'
		if mbType == "Person":
			try:
				if strChars > 4:
					personBegin = beginInt + 20
					# Deal with those born less than 20 years ago
					if personBegin >= 2017:
						personBegin = 2015
				else:
					personBegin = beginInt

				begin = str(personBegin)
			except:
				pass

		# Populate mbDict and countryDict
		if strChars != 0:
			mbDict[xMbId] = begin
			print ("Written to mbDict: " + str(xMbId))
			runLog.write ("Written to mbDict: " + str(xMbId) + '\n')
			if mbCountry:
				countryDict[xMbId] = mbCountry
				print ("Written to countryDict: " + str(xMbId) + ":" + str(mbCountry))
				runLog.write ("Written to countryDict: " + str(xMbId) + ":" + str(mbCountry) + '\n')
			else:
				print ("country info. missing - not written: " + str(xMbId))
				runLog.write ("country info. missing - not written: " + str(xMbId) + '\n')
		else:
			print ("date info. missing - not written: " + str(xMbId))
			runLog.write ("date info. missing - not written: " + str(xMbId) + '\n')

runLog.write('\n' + '\n')
print
print(mbDict)
mbDictFile.write(str(mbDict)  + '\n' + str(len(mbDict)))
print(countryDict)
countryDictFile.write(str(countryDict)  + '\n' + str(len(countryDict)))
print(compDict)
compDictFile.write(str(compDict)  + '\n' + str(len(compDict)))
print

# Read EN genre files into dictionary {mbid:start}
enDict = {}
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	dataInput = open(pathname, "r")
	
	# read lines from file
	for line in dataInput:
		artist, enid, start, end_date, familiarity, hotness, mbid = line.split(",")
		mbid = mbid.strip()

		if mbid in mbDict:
			enDict[mbid] = start
			print ("Written EN MBID to enDict: " + str(mbid))
			runLog.write ("Written EN MBID to enDict: " + str(mbid) + '\n')
		elif mbid in compDict:
			newKey = compDict[mbid]
			enDict[newKey] = start
			print ("Written repaired MBID to enDict: " + str(xMbId))
			runLog.write ("Written repaired MBID to enDict: " + str(xMbId) + '\n')
		else:
			print ("mbid missing from mbDict - not written: " + str(mbid))
			runLog.write ("mbid missing from mbDict - not written: " + str(mbid) + '\n')

runLog.write('\n' + '\n')
print
print(enDict)
enDictFile.write(str(enDict) + '\n' + str(len(enDict)))
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

print ("Iterating through... ")

for key, value in mbDict.iteritems():
	if key in enDict:
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
genreDictFile.write(str(genreDict) + '\n' + str(len(genreDict)))
print

# Find missing artists
diff = set(mbDict.keys()) - set(enDict.keys())
if diff:
	print >> enMiss, diff
else:
	print >> enMiss, "No missing artists."
	print ("No missing artists.")
	print

# Read EN genre files, fix dates from genreDict, and write new `datedGenre' files
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	dataInput = open(pathname, "r")

	datedGenrePath = os.path.join("MbGenres", fileNames[index])
	datedGenreFile = open(datedGenrePath, 'a')
	
	# read lines from file
	for line in dataInput:
		artist, enid, start, end_date, familiarity, hotness, mbid = line.split(",")
		mbid = mbid.strip()

		if mbid in genreDict:
			try:
				country = str(countryDict[mbid])
			except:
				country = ""
			print >> datedGenreFile, artist + ',' + enid + ',' +  str(genreDict[mbid]) + ',' +  end_date + ',' + country + ',' + familiarity + ',' +  hotness + ',' +  mbid
			print ("Written " + str(mbid) + " to file 'MbGenres/" + fileNames[index])
			runLog.write (str(mbid) + '\n')
		else:
			print ("Not written: " + str(mbid))
			runLog.write ("Not written: " + str(mbid) + '\n')

	datedGenreFile.close()

# Check for and remove empty datedGenre files

# define path to 'datedGenres' directory
datedFiles = os.listdir("MbGenres")

for index in range(len(datedFiles)):
	datedPath = os.path.join("MbGenres", datedFiles[index])
	if os.stat(datedPath).st_size == 0:
		os.remove(datedPath)

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ("MB Dictionary Entries: " + str(len(mbDict)) + '\n')
runLog.write ("EN Dictionary Entries: " + str(len(enDict)) + '\n')
runLog.write ("Country Dictionary Entries: " + str(len(countryDict)) + '\n')
runLog.write ("ID comparison Dictionary: " + str(len(compDict)) + '\n')
runLog.write ("Genre (generated) Dictionary: " + str(len(genreDict)) + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()

# write to screen
print
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ("MB Dictionary Entries: " + str(len(mbDict)))
print ("EN Dictionary Entries: " + str(len(enDict)))
print ("Country Dictionary Entries: " + str(len(countryDict)))
print ("ID comparison Dictionary: " + str(len(compDict)))
print ("Genre (generated) Dictionary: " + str(len(genreDict)))
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
