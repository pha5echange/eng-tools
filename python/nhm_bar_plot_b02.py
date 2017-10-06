# nhm_bar_plot_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 28th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Network Hybridity Metric Plotter

# Processes file 'data/nhm_plot.txt' and produces 2 charts: 
# Plots Hgraph and Mean-Hnode values (from'nhm') over time
# Plots Hnode>0.5, Progenitors (Sources), and Sinks as a % of the total graph node-number
# Saves plots as '.eps' files

# USE AFTER 'nhm_b06.py'
# Best used for temporal-category-based analysis
# edit `data/nhm_plot.txt' to define datapoints (by removing unwanted years/lines).

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b02")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'graphs' subdirectory if necessary
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# open file for writing log
logPath = os.path.join("logs", 'nhm_bar_plotter_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# define paths for graphs
#graphHPath = os.path.join("graphs", 'nhm_plotter_' + versionNumber + ".eps")
nodeHPath = os.path.join("graphs", 'nhm_h_bar_plot_' + versionNumber + ".eps")
graphPercPath = os.path.join("graphs", 'nhm_p_bar_plot_' + versionNumber + ".eps")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Network Hybridity Metric Bar Plotter - Beta | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Network Hybridity Metric Bar Plotter - Beta | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'nhm_plot.txt')
dataInput = open(pathname, "r").readlines()

# Remove the first line. Count the others. 
firstLine = dataInput.pop(0)
lineCounter = 0

# define dicts to store the dates and values
graphHyears = {}
nodeHyears = {}
nodePercs = {}
progenPercs = {}
sinkPercs = {}

# read lines from the file
for line in dataInput:

  # split line and append 'graphHyears' with start date values
  year, nodes, graphH, meanNodeH, nodePerc, percProgen, percTotalSinks = line.split(",")
  graphHyears.update ({int(year):float(graphH)})
  nodeHyears.update ({int(year):float(meanNodeH)})
  nodePercs.update ({int(year):float(nodePerc)})
  progenPercs.update ({int(year):float(percProgen)})
  sinkPercs.update ({int(year):float(percTotalSinks)})
  lineCounter += 1

# graphH Plot
# bar width
width = 4

xAxis = []
yAxis = []
adjGraphHX = []

for key, value in sorted(graphHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)
   adjGraphHX.append(int(key - 4))

# set axes values
x_low = (min(xAxis) - 10)
x_high = (max(xAxis) + 10)
y_low = 0
y_high = 0.65

plt.bar(adjGraphHX, yAxis, width, color='lightgray', edgecolor = 'black', label='Hgraph')
plt.xticks([1899, 1920, 1954, 1971, 1987, 1997, 2007, 2015],fontsize=9)

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Category Omega-Year', fontsize=12)
plt.ylabel('Hybridity', fontsize=12)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
# plt.savefig(graphHPath, format = 'eps')
# plt.clf()

# meanNodehH Plot
xAxis = []
yAxis = []
adjNodeHX = []

for key, value in sorted(nodeHyears.iteritems()):
   xAxis.append(key)
   yAxis.append(value)
   adjNodeHX.append(int(key))

# set axes values
#x_low = (min(xAxis) - 5)
#x_high = (max(xAxis) + 5)
#y_low = 0
#y_high = 1.0

# plot graph
plt.bar(adjNodeHX, yAxis, width, color='black', edgecolor = 'black', label='Mean-Hnode')

# label, plot and save image of graph
#plt.grid(zorder=0)
#plt.xlabel('Year', fontsize=14)
#plt.ylabel('Hybridity', fontsize=14)
plt.legend(loc='upper left')
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize='small') 
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(nodeHPath, format = 'eps')
plt.clf()


# GraphPerc Plot
# bar width
width = 2

# Plot Hnode > 0.5 Hybrids
xAxis = []
yAxis = []
adjNodePX = []

for key, value in sorted(nodePercs.iteritems()):
   xAxis.append(key)
   yAxis.append(value)
   adjNodePX.append(int(key - 3))

# set axes values
x_low = (min(xAxis) - 10)
x_high = (max(xAxis) + 10)
y_low = 0
y_high = 65

# plot graph
plt.bar(adjNodePX, yAxis, width, color='lightgray', edgecolor = 'black', label='Hnode>0.5')
plt.xticks([1899, 1920, 1954, 1971, 1987, 1997, 2007, 2015], fontsize=9)
# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Category Omega-Year', fontsize=12)
plt.ylabel('Percentage of Nodes', fontsize=12)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
#plt.savefig(graphPercPath, format = 'eps')
#plt.clf()

# Plot Progenitors
xAxis = []
yAxis = []
adjSourcePX = []

for key, value in sorted(progenPercs.iteritems()):
   xAxis.append(key)
   yAxis.append(value)
   adjSourcePX.append(int(key -1))

# set axes values
#x_low = (min(xAxis) - 5)
#x_high = (max(xAxis) + 5)
#y_low = 0
#y_high = 100

# plot graph
plt.bar(adjSourcePX, yAxis, width, color='gray', edgecolor = 'black', hatch='/', label='Sources')

# label, plot and save image of graph
#plt.grid(zorder=0)
#plt.xlabel('Year', fontsize=14)
#plt.ylabel('Percentage of  Nodes', fontsize=14)
#plt.legend(loc='upper left')
#leg = plt.gca().get_legend()
#ltext = leg.get_texts()
#plt.setp(ltext, fontsize='small') 
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
#plt.savefig(graphPercPath, format = 'eps')
#plt.clf()

# Plot Sinks
xAxis = []
yAxis = []
adjSinkPX = []

for key, value in sorted(sinkPercs.iteritems()):
   xAxis.append(key)
   yAxis.append(value)
   adjSinkPX.append(int(key + 1))

# set axes values
#x_low = (min(xAxis) - 5)
#x_high = (max(xAxis) + 5)
#y_low = 0
#y_high = 100

# plot graph
plt.bar(adjSinkPX, yAxis, width, color='black', edgecolor = 'black', label='Sinks')

# label, plot and save image of graph
#plt.grid(zorder=0)
#plt.xlabel('Year', fontsize=14)
#plt.ylabel('Percentage of  Nodes', fontsize=14)
plt.legend(loc='upper left')
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize='small') 
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPercPath, format = 'eps')
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
