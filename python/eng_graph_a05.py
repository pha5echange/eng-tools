# eng_graph_a05.py
# Version a05
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 26th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Examines Echonest genre lists
# Creates a set for each genre, and adds artist info. as elements
# Finds shared artists to facilitate node-list generaton 

# Run AFTER 'en_genre.py'

# import packages
import os
import resource
from datetime import datetime

versionNumber = ("a05")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# open file for test data output
setDataPath = os.path.join("data", 'genre_sets.txt')
setData = open(setDataPath, 'w')

# open file for data output
intersectDataPath = os.path.join("data", 'genre_intersects.txt')
intersectData = open(intersectDataPath, 'w')

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_graph_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('Genre Data Node List Maker | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Node List Maker | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# create empty lists for genre set contents and labels, an empty set to hold intersectinos and a counter
setList = []
setNameList = []
intersectionSet = set()
genreCount = 0

# open files for reading
for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")

	# create set for genre, and name as `genreLabel'
	setName = genreLabel
	setName = set()

	# read lines from the file and assign each to the set as an element
	for line in dataInput:

		content = str(line.strip("\n"))
		setName.add (content)

	# close input file
	dataInput.close()

	# add genre set to setList to facilitate intersection
	setList.append(setName)

	# add genreLabel to setNameList to facilitate labelling
	setNameList.append(genreLabel)

	# increment counter
	genreCount += 1

	# write to file for testing purposes
	setData.write (str(genreCount) + ') ' + genreLabel + ': ' + str(setName) + '\n')
	# print (genreLabel + ': ' + str(setName) + '\n')

# do intersections here
setAcount = 0
setBcount = 0
intersectCount = 0
totalIntersectCount = 0
totalElementCount = 0

while setAcount < genreCount: 
	setAlabel = str(setNameList[setAcount])
	setA =set(setList[setAcount])
	
	while setBcount < genreCount:
		setBlabel = str(setNameList[setBcount])
		setB = set(setList[setBcount])

		if setBcount < setAcount:
			setBcount += 1
			totalIntersectCount += 1

		else:
			if setAlabel == setBlabel:
				setBcount +=1
				totalIntersectCount += 1

			else: 
				intersectSet = setA.intersection(setB)

				if intersectSet:
					intersectionStr = str(intersectSet)
					elementCount = len(intersectSet)

					print ('\n' + 'Intersection of ' + setAlabel + ' and ' + setBlabel + ': ' + 'Elements: ' + str(elementCount))
					# print (intersectionStr)

					intersectData.write (setAlabel + ',' + setBlabel + ',' + str(elementCount) + ',' + intersectionStr + '\n')

					intersectCount +=1
					totalIntersectCount += 1
					totalElementCount += elementCount
					setBcount += 1	

				else:
					setBcount += 1	

	else:
		setBcount = 0

	setAcount += 1

# End timing of run
endTime = datetime.now()

memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576
avK = intersectCount / genreCount
avW = totalElementCount / intersectCount

# write to log
runLog.write ('Run Information' + '\n' + '\n')
runLog.write ('Genres: ' + str(len(setList)) + '\n')
runLog.write ('V (nodes): ' + str(genreCount) + '\n')
runLog.write ('E (edges): ' + str(intersectCount) + '\n')
runLog.write ('Average K (degree): ' + str(avK) + '\n')
runLog.write ('Average W (weighting): ' + str(avW) + '\n')
runLog.write ('Total Intersections: ' + str(totalIntersectCount) + '\n')
runLog.write ('Total Co-occurrence: ' + str(totalElementCount) + '\n')
runLog.write ('Memory Used: ' + str(memUseMb) + 'Mb' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genres: ' + str(len(setList)))
print ('V (nodes): ' + str(genreCount) )
print ('E (edges): ' + str(intersectCount))
print ('Average K (degree): ' + str(avK))
print ('Average W (weighting): ' + str(avW) )
print ('Total Intersections: ' + str(totalIntersectCount))
print ('Total Co-occurrence: ' + str(totalElementCount))
print ('Memory Used: ' + str(memUseMb) + 'Mb')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
