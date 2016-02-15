# shm_H_plotter_a02.py
# Version a02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# February 13th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Plots data from 'Retromatic' (by Glenn McDonald)
# http://www.furia.com/page.cgi?type=log&id=389

# Processes file 'data/shm_4_plot.txt'
# Plots GraphH-values (from'shm') over time

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("a02")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", 'shm_H_plotter_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# define path for graphs
graphHPath = os.path.join("graphs", 'shm_H_plotter_' + versionNumber + ".png")
nodeHPath = os.path.join("graphs", 'shm_nodeH_plotter_' + versionNumber + ".png")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'SHM H Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'SHM H Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'shm_plot.txt')
dataInput = open(pathname, "r")
	
# define dicts to store the dates and values
graphHyears = {}
nodeHyears = {}

# read lines from the file
for line in dataInput:

	# split line and append 'graphHyears' with start date values
	year, graphH, meanNodeH = line.split(",")
	graphHyears.update ({int(year):float(graphH)})
	nodeHyears.update ({int(year):float(meanNodeH)})

# graphH Plot
xAxis = []
yAxis = []

for key, value in sorted(graphHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 2)
x_high = (max(xAxis) + 2)
y_low = 0
y_high = 1.0

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='-', color='b')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Graph Hybridity', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphHPath, format = 'png')
plt.clf()

# meanNodehH Plot
xAxis = []
yAxis = []

for key, value in sorted(nodeHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 2)
x_high = (max(xAxis) + 2)
y_low = 0
y_high = 1.0

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='-', color='r')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Mean Node Hybridity', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(nodeHPath, format = 'png')
plt.clf()

# close input file
dataInput.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
