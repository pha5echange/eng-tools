# eng_plot_artists_b05.py
# Version b05
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes file 'data/eng_multiplot_data.txt' (output by 'engmulti_plot')
# Plots frequency distribution of artists over time
# Writes run log to 'logs/eng_plot_artists_versionNumber_log.txt'
# Plots results and writes EPS to 'graphs/eng_plot_artists_versionNumber.eps'

# import packages
import os
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b05")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", 'eng_plot_artists_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open files for output
resultsPath = os.path.join("results", 'eng_plot_artists_' + versionNumber + '_data.txt')
processedResults = open(resultsPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'All Artists Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'All Artists Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'eng_multiplot_data.txt')
dataInput = open(pathname, "r")
	
# define dict to store the dates and values
years = {}
totalArtists = 0

# read lines from the file
for line in dataInput:

	# split line and update 'years'
	year, artists = line.split(",")

	totalArtists += int(artists)

	if year in years: 
		years[year] += int(artists)

	else:
		years[year] = int(artists)

# close input file
dataInput.close()

xAxis = []
yAxis = []

for key, value in sorted(years.iteritems()):

    print key, value
    processedResults.write(str(key) + ',' + str(value) + '\n')
    xAxis.append(int(key))
    yAxis.append(int(value))
print yAxis

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = (max(yAxis) + 100)

# plot graph
width = 1 
plt.bar(xAxis, yAxis, width, color='blue')

# define path for graphs
graphPath = os.path.join("graphs", 'eng_plot_artists_' + versionNumber + ".eps")

# label, plot and save image of graph
plt.grid(zorder=0)
plt.suptitle('Numbers of artists by year', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Artists', fontsize=12)
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
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Total Artists: ' + str(totalArtists) + '\n')
runLog.write ('Results are saved to ../results/eng_plot_artists_versionNumber_data.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/eng_plot_artists_versionNumber.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Total Artists: ' + str(totalArtists))
print ('Results are saved to ../results/eng_plot_artists_versionNumber_data.txt')
print ('Graph is saved to ../graphs/eng_plot_artists_versionNumber.eps')
