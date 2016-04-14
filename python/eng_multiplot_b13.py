# eng_multiplot_b13.py
# Version b13
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# April 9th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes genre files output from 'en_genre.py'
# Plots frequency distribution of artists over time
# Writes stats to 'results/eng_multiplot_stats_versionNumber_data.txt'
# Writes results to 'results/eng_multiplot_versionNumber_data.txt'
# Also writes 'data/eng_multiplot_data.txt' (for use by 'eng_plot_artists')
# Writes run log to 'logs/eng_multiplot_versionNumber_log.txt'
# Plots results and writes EPS to 'graphs/eng_multiplot_versionNumber_genreName.eps'

# This version deals with Musicbrainz ID in data files

# Run AFTER 'en_genre.py' has gathered 'genres/..'

# import packages
import os
import sys
import numpy as np
import scipy.stats as stats
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b13")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
		os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
		os.makedirs("data")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs/multi"):
		os.makedirs("graphs/multi")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
		os.makedirs("results")

# open files for output
logPath = os.path.join("logs", 'eng_multiplot_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

statsPath = os.path.join("results", 'eng_multiplot_stats_' + versionNumber + '_data.txt')
statsResults = open(statsPath, 'a')
statsResults.write("Genre" + ',' + "Min" + ',' + "Max" + ',' + "Range" + ',' + "Median" + ',' + "Mean" + ',' + "StD" + ',' + "Var" + ',' + "Skew" + ',' + "Kurtosis" + '\n')

# Write 'data/eng_multi_plot_data.txt' (for use by 'eng_plot_artists')
dataPath = os.path.join("data", 'eng_multiplot_data.txt')
dataOP = open(dataPath, 'w')

resultsPath = os.path.join("results", 'eng_multiplot_' + versionNumber + '_data.txt')
processedResults = open(resultsPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Multi Genre Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Multi Genre Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

for index in range(len(fileNames)):

	# look for files in 'genres' subfolder
	pathname = os.path.join("genres", fileNames[index])
	genreFile = str(fileNames[index])
	genreName, fileExtension = genreFile.split(".")

	# processedResults.write('\n' + genreName + '\n')
	print('\n' + 'Plotting graph and calculating statistics for ' + genreName + '\n')

	# define path for graphs
	graphPath = os.path.join("graphs/multi", 'eng_multiplot_' + versionNumber + '_' + genreName + '.eps')

	dataInput = open(pathname, "r")

	# define list to store the start dates
	instances = []

	# read lines from the file
	for line in dataInput:

		# split line and append 'instances' with start date values
		artist, enid, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")

		if artistStart == " ": 
			artistStart = 0

		if artistStart == 0: 
			artistStart = 0

		else:
			instances.append(int(artistStart))
			
	# close input file
	dataInput.close()

	# count instances of clusters
	countedInstances = Counter()
	countedInstances = Counter(instances)

	xAxis = []
	yAxis = []

	for key, value in sorted(countedInstances.iteritems()):
		processedResults.write(str(key) + ',' + str(value) + '\n')
		dataOP.write(str(key) + ',' + str(value) + '\n')
		xAxis.append(key)
		yAxis.append(value)

	# set axes values
	x_low = (min(xAxis) - 10)
	x_high = (max(xAxis) + 10)
	y_low = 0
	y_high = (max(yAxis) + 10)

	# plot graph
	width = 1
	plt.bar(xAxis, yAxis, width, color='blue')

	# label, plot and save image of graph
	plt.grid(zorder=0)
	plt.suptitle(genreName, fontsize=12)
	plt.xlabel('Artist Start Year', fontsize=12)
	plt.ylabel('Number of Artists', fontsize=12)
	plt.xlim(x_low, x_high)
	plt.ylim(y_low, y_high)
	plt.savefig(graphPath, format = 'eps')
	plt.clf()

	#STATS
	npData = np.array([(xAxis)], dtype=int)
	npMin = npData.min(axis=1)
	npMax = npData.max(axis=1)
	npRange = str(npMax - npMin)
	npMedian = str(np.median(npData, axis=1))
	npMean = str(npData.mean(axis=1))
	npStd = str(npData.std(axis=1, ddof=1))
	npVar = str(npData.var(axis=1))
	npSkew = str(stats.skew(npData, axis=1))
	npKurt = str(stats.kurtosis(npData, axis=1))

	npMinInterStr = str(npMin)
	npMinStr = (npMinInterStr.strip('[]'))
	npMaxInterStr = str(npMax)
	npMaxStr = (npMaxInterStr.strip('[]'))
	npRangeStr = (npRange.strip('[]'))
	npMedianStr = (npMedian.strip('[]'))
	npMeanStr = (npMean.strip('[]'))
	npStdStr = (npStd.strip('[]'))
	npVarStr = (npVar.strip('[]'))
	npSkewStr = (npSkew.strip('[]'))
	npKurtStr = (npKurt.strip('[]'))

	print ("Data: " + str(npData))
	print ("Array shape: " + str(npData.shape))
	print ("Min: " + npMinStr)
	print ("Max: " + npMaxStr)
	print ("Range: " + npRangeStr)    
	print ("Median: " + npMedianStr)
	print ("Mean: " + npMeanStr)
	print ("StD: " + npStdStr)
	print ("Var: " + npVarStr)
	print ("Skew: " + npSkewStr)
	print ("Kurtosis: " + npKurtStr)

	statsResults.write(genreName + ',' + npMinStr + ',' + npMaxStr + ',' + npRangeStr + ',' + npMedianStr + ',' + npMeanStr + ',' + npStdStr + ',' + npVarStr + ',' + npSkewStr + ',' + npKurtStr + '\n')

# close files
statsResults.close()
processedResults.close()
dataOP.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Stats are saved to ../results/eng_multiplot_stats_versionNumber_data.txt' + '\n')
runLog.write ('Results are saved to ../results/eng_multiplot_versionNumber_data.txt' + '\n')
runLog.write ('Data file (for use by eng_plot_artists) is saved to ../data/eng_multiplot_data.txt' + '\n')
runLog.write ('Graphs are saved to ../graphs/multi/eng_multiplot_versionNumber_genreName.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Stats are saved to ../results/eng_multiplot_stats_versionNumber_data.txt')
print ('Results are saved to ../results/eng_multiplot_versionNumber_data.txt')
print ('Data file (for use by eng_plot_artists) is saved to ../data/eng_multiplot_data.txt')
print ('Graphs are saved to ../graphs/multi/eng_multiplot_versionNumber_genreName.eps')
