# eng_plot_b05.py
# Version b05
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 26th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# PLOTS BARS

# Reads single genre file output from 'en_genre.py'
# Processes [renamed and moved] file 'data/genre_2_plot.txt'
# Plots frequency distribution of artists over time
# This version allows for the input of the name of the genre being plotted
# In the future, multi-file version, this will be pulled from the filename
# Writes results to 'results/versionNumber_genreName_eng_plot_data.txt'
# Writes run log to 'logs/versionNumber_genreName_eng_plot_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_genreName_eng_plot.png'

# New version to deal with Musicbrainz ID in data files

# Run AFTER 'en_genre.py' [AND after moving and renaming a genre data file]

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b05")
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
graphPath = os.path.join("graphs", versionNumber + '_' + genreName + "_eng_plot.eps")

# open file for output
resultsPath = os.path.join("results", versionNumber + '_' + genreName + '_eng_plot_data.txt')
processedResults = open(resultsPath, 'a')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'genre_2_plot.txt')
dataInput = open(pathname, "r")
	
# define list to store the start dates
instances = []

# read lines from the file
for line in dataInput:

	# split line and append 'instances' with start date values
	artist, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")
	instances.append(int(artistStart))

# close input file
dataInput.close()

# count and print instances of clusters
countedInstances = Counter(instances)

xAxis = []
yAxis = []

for key, value in sorted(countedInstances.iteritems()):
   processedResults.write(str(key) + ',' + str(value) + '\n')
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 10)
x_high = (max(xAxis) + 10)
y_low = 0
y_high = (max(yAxis) + 5)

# plot graph
width = 3
plt.bar(xAxis, yAxis, width, color='blue')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel(genreName + ' Artist Start Year', fontsize=14)
plt.ylabel('Number of Artists', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPath, format = 'eps')

# display graph on screen - DON'T BOTHER FOR NOW
# plt.show()

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Genre: ' + genreName + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/versionNumber_genreName_eng_plot_data.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_genreName_eng_plot.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genre: ' + genreName)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_genreName_eng_plot_data.txt')
print ('Graph is saved to ../graphs/versionNumber_genreName_eng_plot.eps')
