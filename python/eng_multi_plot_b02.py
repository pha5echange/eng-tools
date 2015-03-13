# eng_multi_plot_b02.py
# Version b01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 13th 2015

# Processes genre files output from 'en_genre.py'
# Plots frequency distribution of artists over time
# Writes results to 'results/versionNumber_eng_multi_plot_data.txt'
# Writes run log to 'logs/versionNumber_eng_multi_plot_log.txt'
# Plots results and writes PNG to 'graphs/versionNumber_genreName_eng_multi_plot.png'

# Run AFTER 'en_genre.py' has gathered 'genres/..'

# import packages
import os
from datetime import datetime
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt

versionNumber = ("b02")

# define path to 'genres' subdirectory
fileNames = os.listdir("genres")

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
logPath = os.path.join("logs", versionNumber + '_eng_multi_plot_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Multi Genre Plotter | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Multi Genre Plotter | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# open file for output
resultsPath = os.path.join("results", versionNumber + '_eng_multi_plot_data.txt')
processedResults = open(resultsPath, 'a')

for index in range(len(fileNames)):

  # look for files in 'genres' subfolder
  pathname = os.path.join("genres", fileNames[index])
  genreFile = str(fileNames[index])
  genreName, fileExtension = genreFile.split(".")

  processedResults.write('Plotting graph for the genre: ' + genreName + '\n')
  print('Plotting graph for the genre: ' + genreName + '\n')
  
  # define path for graphs
  graphPath = os.path.join("graphs", versionNumber + '_' + genreName + "_eng_multi_plot.png")

  dataInput = open(pathname, "r")

  # define list to store the start dates
  instances = []

  # read lines from the file
  for line in dataInput:

  	# split line and append 'instances' with start date values
  	# splits on '^' as this character does not appear in the genre or artist names in the data file 
  	artist, artistStart, artistEnd, hotness = line.split("^")
  	instances.append(int(artistStart))

  # close input file
  dataInput.close()

  # count instances of clusters
  countedInstances = Counter()
  countedInstances = Counter(instances)

  xAxis = []
  yAxis = []

  for key, value in sorted(countedInstances.iteritems()):
    processedResults.write(str(key) + '^' + str(value) + '\n')
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
  plt.suptitle(genreName, fontsize=12)
  plt.xlabel('Artist Start Year', fontsize=12)
  plt.ylabel('Number of Artists', fontsize=12)
  plt.xlim(x_low, x_high)
  plt.ylim(y_low, y_high)
  plt.savefig(graphPath, format = 'png')
  plt.clf()

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/versionNumber_eng_muti_plot_data.txt' + '\n')
runLog.write ('Graph is saved to ../graphs/versionNumber_genreName_eng_multi_plot.png' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_eng_multi_plot_data.txt')
print ('Graph is saved to ../graphs/versionNumber_genreName_eng_multi_plot.png')
