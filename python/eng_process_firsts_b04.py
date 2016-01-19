# eng_process_firsts_b04.py
# Version b04
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Reads results from output of 'eng_first.py'
# Processes file 'data/first_instances.txt'
# Writes results to 'results/eng_process_firsts_versionNumber.txt'
# Writes run log to 'logs/eng_process_firsts_versionNumber_log.txt'
# Plots results and writes EPS to 'graphs/eng_process_firsts_versionNumber_plot.eps'

# Run AFTER 'eng_cluster.py'

# PLOTS BARS

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b04")

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
logPath = os.path.join("logs", 'eng_process_firsts_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# define path for graphs
graphPath = os.path.join("graphs", 'eng_process_firsts_' + versionNumber + "_plot.eps")

# open file for data output
resultsPath = os.path.join("results", 'eng_process_firsts_' + versionNumber + '.txt')
processedResults = open(resultsPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data First Instances Results Processor | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data First Instances Results Processor | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'first_instances.txt')
dataInput = open(pathname, "r")
	
# define list to store the start dates
instances = []

# read lines from the file
for line in dataInput:

	# split line and append 'instances' with start date values
	genre, firstInstance = line.split(",")
	instances.append(int(firstInstance))

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
y_high = (max(yAxis) + 10)

# plot graph
width = 3
plt.bar(xAxis, yAxis, width, color='blue')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year of Artist First Instance', fontsize=14)
plt.ylabel('Number of Genres', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPath, format = 'eps')

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write('Graph is saved to ../graphs/eng_process_firsts_versionNumber_plot.eps' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
print('Graph is saved to ../graphs/eng_process_firsts_versionNumber_plot.eps')
