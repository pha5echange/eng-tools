# eng_prob_b03.py
# Version b03
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Calculates probability distribution of artists against time
# Reads single genre file output from 'eng_plot.py'
# Processes [renamed and moved] file 'data/genre_freq_data.txt'
# Writes results to 'results/eng_prob_versionNumber_genreName_data.txt'
# Writes run log to 'logs/eng_prob_versionNumber_genreName_log.txt'

# Run AFTER 'eng_plot.py' [AND after moving and renaming a genre plot data file to 'genre_freq_data.txt']

# import packages
import os
from datetime import datetime
from collections import Counter

versionNumber = ("b03")
genreName = str(raw_input ("Enter the name of the genre to be plotted: "))
totalArtists = int(raw_input ("Enter the total number of artists in this genre: "))

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'eng_prob_' + versionNumber + '_' + genreName + '_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Single Genre Probability Worker-Outer | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Single Genre Probability Worker_Outer | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# open file for data output
resultsPath = os.path.join("results", 'eng_prob_' + versionNumber + '_' + genreName + '_data.txt')
processedResults = open(resultsPath, 'a')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'genre_freq_data.txt')
dataInput = open(pathname, "r")

# read lines from the file
for line in dataInput:

	# split line, calculate probs and write to processedResults
	year, freq = line.split(",")
	
	# calculate probability value here
	probValue = (float(freq) / float(totalArtists))

	# write results
	processedResults.write(str(year) + ',' + str(probValue) + '\n')

# close input file
dataInput.close()

# close file
processedResults.close()

# End timing of run
endTime = datetime.now()

# write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Genre: ' + genreName + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Results are saved to ../results/eng_prob_versionNumber_genreName_data.txt' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genre: ' + genreName)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/eng_prob_versionNumber_genreName_data.txt')
