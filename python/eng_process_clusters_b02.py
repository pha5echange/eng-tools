# eng_process_clusters_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# May 1st 2015

# Reads results from output of 'eng_cluster.py'
# Processes file 'data/first_cluster.txt'
# Writes results to 'results/versionNumber_eng_process_clusters.txt'
# Writes run log to 'logs/versionNumber_eng_process_clusters_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_eng_process_clusters_plot.png'

# Run AFTER 'eng_cluster.py'

# PLOTS BARS

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

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_process_clusters_log.txt')
runLog = open(logPath, 'a')

# define path for graphs
graphPath = os.path.join("graphs", versionNumber + "_eng_process_clusters_plot.png")

# open file for data output
resultsPath = os.path.join("results", versionNumber + '_eng_process_clusters.txt')
processedResults = open(resultsPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data Results Processor | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Results Processor | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'first_cluster.txt')
dataInput = open(pathname, "r")
	
# define list to store the start dates
clusters = []

# read lines from the file
for line in dataInput:

	# split line and append 'clusters' with start date values
	# splits on '^' as this character does not appear in the genre or artist names in the data file 
	genre, clusterDate, newLine = line.split("^")
	clusters.append(int(clusterDate))

# close input file
dataInput.close()

# count and print instances of clusters
countedClusters = Counter(clusters)

xAxis = []
yAxis = []

for key, value in sorted(countedClusters.iteritems()):
   processedResults.write(str(key) + '^' + str(value) + '\n')
   xAxis.append(key)
   yAxis.append(value)

# set axes values
x_low = (min(xAxis) - 10)
x_high = (max(xAxis) + 10)
y_low = 0
y_high = (max(yAxis) + 10)

# plot graph
width = 1
plt.bar(xAxis, yAxis, width, color='blue')

# label, plot and save image of graph
plt.grid(zorder=0)
plt.xlabel('Year of Inception (5 percent artist clusters)', fontsize=14)
plt.ylabel('Number of Genres', fontsize=14)
plt.xlim(x_low, x_high)
plt.ylim(y_low, y_high)
plt.savefig(graphPath, format = 'png')

# close files
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/versionNumber_eng_process_clusters.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_eng_process_clusters_plot.png' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_eng_process_clusters.txt')
print ('Graph is saved to ../graphs/versionNumber_eng_process_clusters_plot.png')
