# eng_plot_artists_b03.py
# Version b03
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 26th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes file 'data/eng_multi_plot_data.txt' (output by 'eng_multi_plot')
# Plots frequency distribution of artists over time
# Writes run log to 'logs/versionNumber_eng_plot_artists_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_eng_plot_artists.png'

# import packages
import os
from datetime import datetime
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b03")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_' + '_eng_plot_artists_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'All Artists Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'All Artists Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# define path for graphs
graphPath = os.path.join("graphs", versionNumber + "_eng_plot_artists.eps")

# open files for output
resultsPath = os.path.join("results", versionNumber + '_eng_plot_artists_data.txt')
processedResults = open(resultsPath, 'a')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'eng_multi_plot_data.txt')
dataInput = open(pathname, "r")
	
# define dict to store the dates and values
years = defaultdict(int)

# read lines from the file
for line in dataInput:

	# split line and update 'years'
	year, artists = line.split(",")
	years[year] += int (artists)
	years.update ({int(year):int(artists)})

# close input file
dataInput.close()

xAxis = []
yAxis = []

for key, value in sorted(years.iteritems()):

    print key, value
    processedResults.write(str(key) + ',' + str(value) + '\n')
    xAxis.append(int(key))
    yAxis.append(int(value))

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = (max(yAxis) + 100)

# plot graph
width = 1 
plt.bar(xAxis, yAxis, width, color='blue')

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
runLog.write ('Results are saved to ../results/versionNumber_eng_plot_artists_data.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_eng_plot_artists.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_eng_plot_artists_data.txt')
print ('Graph is saved to ../graphs/versionNumber_eng_plot_artists.eps')
