# nhm_plotter_a07.py
# Version a07
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# February 25th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Plots data from 'Retromatic' (by Glenn McDonald)
# http://www.furia.com/page.cgi?type=log&id=389

# RENAMED TO 'Network Hybridity Metric Plotter'

# Processes file 'data/nhm_plot.txt' and produces 2 line-graphs: 
  # Plots GraphH and Mean-NodeH values (from'nhm') over time
  # Plots NodeH=1.0 and Progenitors as a % of the total graph node-number

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("a07")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", 'nhm_plotter_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# define paths for graphs
graphHPath = os.path.join("graphs", 'nhm_plotter_' + versionNumber + ".png")
nodeHPath = os.path.join("graphs", 'nhm_nodeH_plotter_' + versionNumber + ".png")
graphPercPath = os.path.join("graphs", 'nhm_Perc_plotter_' + versionNumber + ".png")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Network Hybridity Metric Plotter - Alpha | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Network Hybridity Metric Plotter - Alpha | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'nhm_plot.txt')
dataInput = open(pathname, "r").readlines()

# Remove the first line
firstLine = dataInput.pop(0)

# define dicts to store the dates and values
graphHyears = {}
nodeHyears = {}
nodePercs = {}
progenPercs = {}

# read lines from the file
for line in dataInput:

  # split line and append 'graphHyears' with start date values
  year, nodes, graphH, meanNodeH, nodePerc, percProgen = line.split(",")
  graphHyears.update ({int(year):float(graphH)})
  nodeHyears.update ({int(year):float(meanNodeH)})
  nodePercs.update ({int(year):float(nodePerc)})
  progenPercs.update ({int(year):float(percProgen)})

# graphH Plot
xAxis = []
yAxis = []

for key, value in sorted(graphHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = 1.0

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='dashed', color='b', marker='o')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Hybridity', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
# plt.savefig(graphHPath, format = 'png')
# plt.clf()

# meanNodehH Plot
xAxis = []
yAxis = []

for key, value in sorted(nodeHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = 1.0

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='solid', color='r', marker='x')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Hybridity', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(nodeHPath, format = 'png')
plt.clf()

# GraphPerc Plot
xAxis = []
yAxis = []

for key, value in sorted(nodePercs.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = 60

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='dashed', color='b', marker='o')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Percentage of Nodes', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
# plt.savefig(graphPercPath, format = 'png')
# plt.clf()

xAxis = []
yAxis = []

for key, value in sorted(progenPercs.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 5)
x_high = (max(xAxis) + 5)
y_low = 0
y_high = 60

# plot graph
width = 1
plt.plot(xAxis, yAxis, linestyle='solid', color='r', marker='x')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Percentage of  Nodes', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPercPath, format = 'png')
plt.clf()

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
