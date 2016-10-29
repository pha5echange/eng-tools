# eng_nodesets_b08.py
# Version b08
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 28th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines time-sliced Echonest 'Omega Year' genre lists (from 'ts_data/')
# Creates a set for each genre, and adds artist info. as elements
# Finds shared artists to facilitate node-list generation
# Writes weighted nodelist 

# Run AFTER 'en_genre.py'

# import packages
import os
import resource
from collections import OrderedDict
from datetime import datetime

versionNumber = ("b08")

# open file for writing log
logPath = os.path.join("logs", 'eng_nodesets_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# ..and begin..
print ('\n' + 'Genre Data Node Set Maker | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')
runLog.write ('Genre Data Node Set Maker | ' + 'Version: ' + versionNumber + '\n' + '\n')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Look for subfolders in `ts_data' and generate datelist from these
dateList = []
datePath = "ts_data/"
dateList = os.listdir(datePath) 
dateSet = set(dateList)

'''
# Generate dictionary containing nodenames and dates (from 'data\first_cluster.txt')
dateInputPath = os.path.join("data", 'first_cluster.txt')
dateInput = open(dateInputPath, 'r')

dateDict = {}
dateList = []

for line in dateInput:
	genreInput, genreDate, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	dateDict[genreName] = genreDate
	# dateList.append(genreDate)

sortDates = OrderedDict(sorted(dateDict.items()))

for key, value in sortDates.iteritems():
	dateList.append(int(value))

dateSet = set(dateList)

# add 2015 to 'dateSet' 
dateSet.add(2015)
'''

# initialise global counters
totalIntersectCount = 0
totalElementCount = 0

# Get user input
#print
#dateIP = int(input ("Enter an Omega Year to remove artists that appear AFTER this date (or 0 to leave data intact): "))
#omegaYear = str(dateIP)

for date in dateSet:

	dateIP = int(date)
	omegaYear = str(dateIP)

	# define path to 'genres' subdirectory
	omegaGenrePath = os.path.join("ts_data", omegaYear, "genres")
	fileNames = os.listdir(omegaGenrePath)

	# open files for data output
	intersectDataPath = os.path.join("ts_data", omegaYear, omegaYear + '_genre_intersects.txt')
	intersectData = open(intersectDataPath, 'w')

	# Data file for weighted, undirected graph
	wuGraphDataPath = os.path.join("ts_data", omegaYear, omegaYear + '_wuGraph_data.txt')
	wuGraphData = open(wuGraphDataPath, 'w')

	# create empty lists for genre set contents and labels, an empty set to hold intersections and a counter
	setList = []
	setNameList = []
	intersectionSet = set()
	genreCount = 0

	if dateIP != 0:
		# open files for reading
		for index in range(len(fileNames)):

			# look for files in 'genres' subfolder
			pathname = os.path.join(omegaGenrePath, fileNames[index])
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
			# setData.write (str(genreCount) + ') ' + genreLabel + ': ' + str(setName) + '\n')
			# print (genreLabel + ': ' + str(setName) + '\n')

	# do intersections here
	setAcount = 0
	setBcount = 0
	intersectCount = 0

	while setAcount < genreCount: 
		setAlabel = str(setNameList[setAcount]).replace(" ", "").replace("'","")
		setA  = set(setList[setAcount])
		
		while setBcount < genreCount:
			setBlabel = str(setNameList[setBcount]).replace(" ", "").replace("'","")
			setB  = set(setList[setBcount])

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
						elementCount = len(intersectSet)
						intersectionStr = str(intersectSet)

						print ('\n' + 'Intersection of ' + setAlabel + ' and ' + setBlabel + ': ' + 'Elements: ' + str(elementCount) + ' SetAcount: ' + str(setAcount) + ' setBcount: ' + str(setBcount))
						# print (intersectionStr)

						runLog.write ('Intersection of ' + setAlabel + ' and ' + setBlabel + ': ' + 'Elements: ' + str(elementCount) + ' SetAcount: ' + str(setAcount) + ' setBcount: ' + str(setBcount) + '\n')
						
						if setAlabel:
							# For full data file,make circumfles ('^') seperator, to avoid problems with sets() later
							intersectData.write (setAlabel + '^' + setBlabel + '^' + str(elementCount) + '^' + intersectionStr + '\n')

							# Data file for weighted, undirected graph
							wuGraphData.write (setAlabel + ',' + setBlabel + ',' + str(elementCount) + '\n')

						intersectCount += 1
						totalIntersectCount += 1
						totalElementCount += elementCount
						setBcount += 1	

					else:
						# write setA only to enable nodes with no connections
						wuGraphData.write (setAlabel + ',' + setAlabel + ',' + "0" + '\n')
						setBcount += 1	
						wuGraphData.write (setBlabel + ',' + setBlabel + ',' + "0" + '\n')

		else:
			setBcount = 0

		setAcount += 1

	# Close files
	# setData.close()
	intersectData.close()
	wuGraphData.close()

#meanK = intersectCount / genreCount
#meanW = totalElementCount / intersectCount

memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
#runLog.write ('Genres: ' + str(genreCount) + '\n')
#runLog.write ('V (nodes): ' + str(len(setList)) + '\n')
#runLog.write ('E (edges): ' + str(intersectCount) + '\n')
#runLog.write ('Mean k(degree): ' + str(meanK) + '\n')
#runLog.write ('Mean w (weighting): ' + str(meanW) + '\n')
runLog.write ('Total Intersections: ' + str(totalIntersectCount) + '\n')
runLog.write ('Total Co-occurrence: ' + str(totalElementCount) + '\n')
runLog.write ('Memory Used: ' + str(memUseMb) + 'Mb' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
#print ('Genres: ' + str(genreCount))
#print ('V (nodes): ' + str(len(setList)))
#print ('E (edges): ' + str(intersectCount))
#print ('Mean k (degree): ' + str(meanK))
#print ('Mean w (weighting): ' + str(meanW) )
print ('Total Intersections: ' + str(totalIntersectCount))
print ('Total Co-occurrence: ' + str(totalElementCount))
print ('Memory Used: ' + str(memUseMb) + 'Mb')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
