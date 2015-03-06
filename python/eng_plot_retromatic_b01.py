# eng_plot_retromatic_b01.py
# Version b01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 6th 2015

# Processes file 'data/retromatic.txt'
# Plots frequency distribution of genres over time
# Writes run log to 'logs/versionNumber_genreName_eng_plot_retromatic_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_eng_plot_retromatic.png'

# Ensure 'retromatic.txt' is present in the 'data' folder.

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b01")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_' + '_eng_plot_retromatic_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Retromatic Genre Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Retromatic Genre Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# define path for graphs
graphPath = os.path.join("graphs", versionNumber + '_' + "_eng_plot_retromatic.png")

# look for file in 'data' subfolder
pathname = os.path.join("data", 'retromatic.txt')
dataInput = open(pathname, "r")
	
# define dict to store the dates and values
years = {}

# read lines from the file
for line in dataInput:

	# split line and append 'instances' with start date values
	# splits on '^' as this character does not appear in the genre or artist names in the data file 
	year, genres = line.split("^")
	years.update ({int(year):int(genres)})

# close input file
dataInput.close()

xAxis = []
yAxis = []

for key, value in sorted(years.iteritems()):
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
plt.suptitle('Retromatic Genre Plot', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Genres', fontsize=12)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPath, format = 'png')

# display graph on screen - DON'T BOTHER FOR NOW
# plt.show()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_eng_plot_retromatic.png' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Graph is saved to ../graphs/versionNumber_eng_plot_retromatic.png')
