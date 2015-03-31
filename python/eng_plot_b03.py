# eng_plot_b03.py
# Version b03
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 30th 2015

# Reads single genre file output from 'en_genre.py'
# Processes [renamed and moved] file 'data/genre_2_plot.txt'
# Plots frequency distribution of artists over time
# This version allows for the input of the name of the genre being plotted
# In the future, multi-file version, this will be pulled from the filename
# Writes results to 'results/versionNumber_genreName_eng_plot_data.txt'
# Writes run log to 'logs/versionNumber_genreName_eng_plot_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_genreName_eng_plot.png'
# DOES STATS

# Run AFTER 'en_genre.py' [AND after moving and renaming a genre data file]

# import packages
import os
import sys
import numpy as np
import scipy.stats as stats
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b03")
genreName = str(raw_input ("Enter the name of the genre to be plotted: "))

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_' + genreName + '_eng_plot_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Single Genre Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Single Genre Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# define path for graphs
graphPath = os.path.join("graphs", versionNumber + '_' + genreName + "_eng_plot.png")

# open files for output
resultsPath = os.path.join("results", versionNumber + '_' + genreName + '_eng_plot_data.txt')
processedResults = open(resultsPath, 'a')

statsPath = os.path.join("results", versionNumber + '_' + genreName + '_eng_plot_stats_data.txt')
statsResults = open(statsPath, 'a')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'genre_2_plot.txt')
dataInput = open(pathname, "r")
	
# define list to store the start dates
instances = []

# read lines from the file
for line in dataInput:

	# split line and append 'instances' with start date values
	# splits on '^' as this character does not appear in the genre or artist names in the data file 
	artist, artistStart, artistEnd, hotness = line.split("^")
	instances.append(int(artistStart))

# close input file
dataInput.close()

# count and print instances of clusters
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
plt.plot(xAxis, yAxis, marker='o', linestyle='-', color='b')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.suptitle('Single Genre Plot' + ' - ' + genreName, fontsize=14)
plt.xlabel('Artist Start Year', fontsize=12)
plt.ylabel('Number of Artists', fontsize=12)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPath, format = 'png')

# display graph on screen - DON'T BOTHER FOR NOW
# plt.show()

# close file
processedResults.close()

#STATS
npData = np.array([(xAxis),(yAxis)], dtype=int)
npMedian = str(np.median(npData, axis=1))
npMean = npData.mean(axis=1)
npMin = npData.min(axis=1)
npMax = npData.max(axis=1)
npStd = npData.std(axis=1, ddof=1)
npVar = npData.var(axis=1)
npSkew = stats.skew(npData, axis=1)
npKurt = stats.kurtosis(npData, axis=1)
npRange = (npMax - npMin)

print ("Data: " + str(npData))
print ("Array shape: " + str(npData.shape))
print ("Median: " + str(npMedian))
print ("Mean: " + str(npMean))
print ("StD: " + str(npStd))
print ("Skew: " + str(npSkew))
print ("Kurtosis: " + str(npKurt))

statsResults.write(str(genreName) + ' ^ ' + "Median: " + str(npMedian) + ' ^ ' + "Mean: " + str(npMean) + ' ^ ' + "Min: " + str(npMin) + ' ^ ' + "Max: " + str(npMax) + ' ^ ' + "StD: " + str(npStd) + ' ^ ' + "Var: " + str(npVar) + ' ^ ' + "Skew: " + str(npSkew) + ' ^ ' + "Kurtosis: " + str(npKurt) + ' ^ ' + "Range: " + str(npRange) + '\n')

# close file
statsResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Genre: ' + genreName + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/versionNumber_genreName_eng_plot_data.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_genreName_eng_plot.png' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genre: ' + genreName)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_genreName_eng_plot_data.txt')
print ('Graph is saved to ../graphs/versionNumber_genreName_eng_plot.png')
