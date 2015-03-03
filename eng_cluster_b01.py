# eng_cluster_b01.py
# Version b01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 2nd 2015

# Examines Echonest genre lists
# Finds clusters of start dates in files 
# A cluster could, for example, equal 5% of the total number of artists
# This version takes user-input to define a cluster
# Notes first cluster
# Reads files from 'genres' subdirectory
# Writes results to 'data/cluster_results.txt'
# Writes first cluster to 'data/first_cluster.txt'
# Writes run log to 'logs/versionNumber_eng_cluster_log.txt'

# Run AFTER 'en_genre.py'

# import packages
import os
from datetime import datetime

versionNumber = ("b01")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_cluster_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data Cluster Finder | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Cluster Finder | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

clusterInput = int(input ("Enter the percentage of the total that equates to a cluster: "))

# open files for reading
for index in range(len(fileNames)):

	# define lists to store the start dates and clusterNumbered dates in
	genreStartDates = []
	artistNames = []
	clusterDates = []

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreLabel, fileExtension = genreFile.split(".")
	dataInput = open(pathname, "r")
	
	# read lines from the file
	for line in dataInput:

		# split line and append genreStartDates' with start date values
		# splits on '^' as this character does not appear in the genre or artist names in the data file 
		artist, start, end_date = line.split("^")
		startDate = int(start)
		artistNames.append(artist)
		genreStartDates.append(startDate)

	# close input file
	dataInput.close()

	# open file for data output
	clusterDataPath = os.path.join("data", 'cluster_results.txt')
	clusterData = open(clusterDataPath, 'a')
	firstClusterPath = os.path.join("data", 'first_cluster.txt')
	firstCluster = open(firstClusterPath, 'a')

	# do comparison
	index = 0
	clusterNumber = 1
	maxIndex = len(genreStartDates)

	# variable for deciding what a cluster is - at least 3 artists in this instance, or a percentage of the total
	divisor = int (100 / clusterInput)
	minClusterSize = int(maxIndex / divisor)
	if minClusterSize < 3:
		minClusterSize = 3

	clusters = set()

	while (index + 1) < maxIndex:
		if genreStartDates[index] == genreStartDates [index + 1]:
			clusterNumber = clusterNumber + 1

			runLog.write('\n' + 'Match found: ' + str(genreStartDates[index]) + '\n')
			runLog.write('Genre: ' + str(genreLabel) + '\n')
			runLog.write('Index: ' + str(index) + ' and ' + str(index + 1) + '\n')
			runLog.write('Artists: ' + str(artistNames[index]) + ' and ' + str(artistNames[index + 1]) + '\n')
			runLog.write('Cluster Number: ' + str(clusterNumber) + '\n' + '\n')

			print
			print('Match found: ' + str(genreStartDates[index]))
			print('Genre: ' + str(genreLabel))
			print('Index: ' + str(index) + ' and ' + str(index + 1))
			print('Artists: ' + str(artistNames[index]) + ' and ' + str(artistNames[index + 1]))
			print('Cluster Number: ' + str(clusterNumber))
			print

			# check for a cluster of 'minClusterSize'
			if clusterNumber >= minClusterSize:
				clusterDates.append(genreStartDates[index])

				runLog.write('\n' + 'Cluster found - ' + 'Date: ' + str(genreStartDates[index]) + '\n')
				runLog.write('Genre: ' + str(genreLabel) + '\n')
				runLog.write('Index: ' + str(index) + '\n')
				runLog.write('Cluster Number: ' + str(clusterNumber) + '\n' + '\n')
			
				print
				print('Cluster found - ' + 'Date: ' + str(genreStartDates[index]))
				print('Genre: ' + str(genreLabel))
				print('Index: ' + str(index))
				print('Cluster Number: ' + str(clusterNumber))
				print

		# if not a match, then reset cluster number to '1' and mark as 'no match'
		else:
			clusterNumber = 1
			runLog.write('\n' + 'No match: ' + str(genreStartDates[index]) + ' and ' + str(genreStartDates[index + 1]) + '\n')
			runLog.write('Genre: ' + str(genreLabel) + '\n')
			runLog.write('Index: ' + str(index) + ' and ' + str(index + 1) + '\n' )
			runLog.write('Artists: ' + str(artistNames[index]) + ' and ' + str(artistNames[index + 1]) + '\n')
			runLog.write('Cluster Number: ' + str(clusterNumber) + '\n' + '\n')
		
			print
			print('No match: ' + str(genreStartDates[index]) + ' and ' + str(genreStartDates[index + 1]))
			print('Genre: ' + str(genreLabel))
			print('Index: ' + str(index) + ' and ' + str(index + 1))
			print('Artists: ' + str(artistNames[index]) + ' and ' + str(artistNames[index + 1]))
			print('Cluster Number: ' + str(clusterNumber))
			print

		# move index along one place to try the next match
		index = index + 1

	# add clusterDates to a set to remove duplicate entries
	clusters = set(clusterDates)

	# if 'clusters' is not empty, sort 'clusterDates' and get first element, then write results to files
	if clusters:
		clusterDates.sort()
		firstClust = clusterDates[0]
		clusterData.write(str(genreLabel) + '^' + str(sorted(clusters)) + '\n')
		firstCluster.write(str(genreLabel) + '^' + str(firstClust) + '^' + '\n')

	# if 'clusters' is empty, clear out 'clusters' and set 'firstCLust' to null
	else:
		clusters = set()
		firstClust = []

	# write results of run to 'runLog'
	runLog.write('\n' + 'Genre: ' + str(genreLabel) + '\n')
	runLog.write('Index: ' + str(index) + '\n')
	runLog.write('MaxIndex: ' + str(maxIndex) + '\n')
	runLog.write('Cluster Number: ' + str(clusterNumber) + '\n')
	runLog.write('Minimum Cluster Size: ' + str(minClusterSize) + '\n')
	runLog.write('Clusters Found: ' + str(len(clusters)) + '\n')
	runLog.write('Cluster Dates Found: ' + str(sorted(clusters)) + '\n')
	runLog.write('First Cluster: ' + str(firstClust) + '\n' + '\n')

	# close files
	clusterData.close()
	firstCluster.close()

	print
	print('Genre: ' + str(genreLabel))
	print('Index: ' + str(index))
	print('MaxIndex: ' + str(maxIndex))
	print('Cluster Number: ' + str(clusterNumber))
	print('Minimum Cluster Size: ' + str(minClusterSize))
	print('Clusters Found: ' + str(len(clusters)))
	print('Cluster Dates Found: ' + str(sorted(clusters)))
	print('First Cluster: ' + str(firstClust))
	print

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Percentage of artists that equates to a cluster: ' + str(clusterInput) + '%' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Percentage of artists that equates to a cluster: ' + str(clusterInput) + '%')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
