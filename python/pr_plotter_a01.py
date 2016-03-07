# pr_plotter_a01.py
# Version a01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 7th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Pagerank Plotter

# Processes file 'results/pr_hot_fam.txt' and produces 3 plots: 
# Plots PR against Mean Familiarity
# Plots PR against Mean Hotttnesss
# Plots Mean Familiarity against Mean Hotttness

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("a01")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", 'pr_plotter_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# define paths for graphs
prFamPath = os.path.join("graphs", 'pr_fam_' + versionNumber + ".eps")
prHotPath = os.path.join("graphs", 'pr_hot_' + versionNumber + ".eps")
hotFamPath = os.path.join("graphs", 'hot_fam_' + versionNumber + ".eps")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'PageRank Plotter - Alpha | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'PageRank Plotter - Alpha | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# look for file in 'results' subfolder
pathname = os.path.join("results/", 'pr_hot_fam_results_a01.txt')
dataInput = open(pathname, "r").readlines()

# Remove the first line
firstLine = dataInput.pop(0)

# define dicts to store the dates and values
prFamDict = {}
prHotDict = {}
hotFamDict = {}

# read lines from the file
for line in dataInput:

  # split line and update dictionaries
  genre, pageRank, meanFam, meanHot, newLine = line.split(",")
  prFamDict.update ({float(meanFam):float(pageRank)})
  prHotDict.update ({float(meanHot):float(pageRank)})
  hotFamDict.update ({float(meanHot):float(meanFam)})

# prFam Plot
xAxis = []
yAxis = []

for key, value in sorted(prFamDict.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = 0
x_high = (max(xAxis) + 0.05)
y_low = 0
y_high = (max(yAxis) + 0.0005)

# plot graph
width = 1
plt.plot(xAxis, yAxis,'g,')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Mean-Familiarity', fontsize=14)
plt.ylabel('PageRank', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(prFamPath, format = 'eps', bbox_inches='tight')
plt.clf()

# prHot Plot
xAxis = []
yAxis = []

for key, value in sorted(prHotDict.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = 0
x_high = (max(xAxis) + 0.05)
y_low = 0
y_high = (max(yAxis) + 0.0005)

# plot graph
width = 1
plt.plot(xAxis, yAxis, 'b,')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Mean-Hotttnesss', fontsize=14)
plt.ylabel('PageRank', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(prHotPath, format = 'eps', bbox_inches='tight')
plt.clf()

# hotFam Plot
xAxis = []
yAxis = []

for key, value in sorted(hotFamDict.iteritems()):
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = 0
x_high = (max(xAxis) + 0.05)
y_low = 0
y_high = (max(yAxis) + 0.05)

# plot graph
width = 1
plt.plot(xAxis, yAxis,'k,')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Mean-Hotttnesss', fontsize=14)
plt.ylabel('Mean-Familiarity', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(hotFamPath, format = 'eps', bbox_inches='tight')
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
