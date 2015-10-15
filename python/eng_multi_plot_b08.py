# eng_multi_plot_b08.py
# Version b08
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 15th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes genre files output from 'en_genre.py'
# Plots frequency distribution of artists over time
# Writes stats to 'results/versionNumber_eng_multi_plot_stats_data.txt'
# Writes results to 'results/versionNumber_eng_multi_plot_data.txt'
# Writes run log to 'logs/versionNumber_eng_multi_plot_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_genreName_eng_multi_plot.png'

# New version to deal with Musicbrainz ID in data files

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

versionNumber = ("b08")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
		os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
		os.makedirs("graphs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
		os.makedirs("results")

# open files for output
logPath = os.path.join("logs", versionNumber + '_eng_multi_plot_log.txt')
runLog = open(logPath, 'a')

statsPath = os.path.join("results", versionNumber + '_' + '_eng_multi_plot_stats_data.txt')
statsResults = open(statsPath, 'a')
statsResults.write("Genre" + ',' + "Min" + ',' + "Max" + ',' + "Range" + ',' + "Median" + ',' + "Mean" + ',' + "StD" + ',' + "Var" + ',' + "Skew" + ',' + "Kurtosis" + '\n')

resultsPath = os.path.join("results", versionNumber + '_eng_multi_plot_data.txt')
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
	genreNameClean = genreName.replace("'", "")

	# processedResults.write('\n' + genreName + '\n')
	print('\n' + 'Plotting graph and calculating statistics for ' + genreName + '\n')
	
	# define path for graphs
	graphPath = os.path.join("graphs", versionNumber + '_' + genreName + "_eng_multi_plot.eps")

	dataInput = open(pathname, "r")

	# define list to store the start dates
	instances = []

	# read lines from the file
	for line in dataInput:

		# split line and append 'instances' with start date values
		# splits on '^' as this character does not appear in the genre or artist names in the data file 
		artist, artistStart, artistEnd, hotness, mbid = line.split("^")

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
		processedResults.write(str(key) + '^' + str(value) + '\n')
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
	print ("Skew: " + npSkewStr)
	print ("Kurtosis: " + npKurtStr)

	statsResults.write(genreNameClean + ',' + npMinStr + ',' + npMaxStr + ',' + npRangeStr + ',' + npMedianStr + ',' + npMeanStr + ',' + npStdStr + ',' + npVarStr + ',' + npSkewStr + ',' + npKurtStr + '\n')

# close files
statsResults.close()
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Stats are saved to ../results/versionNumber_eng_muti_plot_stats_data.txt' + '\n')
runLog.write ('Results are saved to ../results/versionNumber_eng_muti_plot_data.txt' + '\n')
runLog.write ('Graphs are saved to ../graphs/versionNumber_genreName_eng_multi_plot.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Stats are saved to ../results/versionNumber_eng_muti_plot_stats_data.txt')
print ('Results are saved to ../results/versionNumber_eng_multi_plot_data.txt')
print ('Graphs are saved to ../graphs/versionNumber_genreName_eng_multi_plot.eps')
