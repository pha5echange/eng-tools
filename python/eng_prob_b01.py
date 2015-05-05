# eng_prob_b01.py
# Version b01
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# March 2nd 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Calculates probability distribution of artists against time
# Reads single genre file output from 'eng_plot.py'
# Processes [renamed and moved] file 'data/genre_freq_data.txt'
# Writes results to 'results/versionNumber_genreName_eng_prob_data.txt'
# Writes run log to 'logs/versionNumber_genreName_eng_prob_log.txt'

# GRAB THE TOTAL FROM THE LOGS IN THE NEXT VERSION!

# Run AFTER 'eng_plot.py' [AND after moving and renaming a genre plot data file to 'genre_freq_data.txt']

# import packages
import os
from datetime import datetime
from collections import Counter

versionNumber = ("b01")
genreName = str(raw_input ("Enter the name of the genre to be plotted: "))
totalArtists = int(raw_input ("Enter the total number of artists in this genre: "))

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_' + genreName + '_eng_prob_log.txt')
runLog = open(logPath, 'a')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Single Genre Probability Worker-Outer | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Single Genre Probability Worker_Outer | ' + 'Version: ' + versionNumber + ' | Starting' + '\n' +'\n')

# open file for data output
resultsPath = os.path.join("results", versionNumber + '_' + genreName + '_eng_prob_data.txt')
processedResults = open(resultsPath, 'a')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'genre_freq_data.txt')
dataInput = open(pathname, "r")

# read lines from the file
for line in dataInput:

	# split line, calculate probs and write to processedResults
	# splits on '^' as this character does not appear in the genre or artist names in the data file 
	year, freq = line.split("^")
	
	# calculate probability value here
	probValue = (float(freq) / float(totalArtists))

	# write results
	processedResults.write(str(year) + '^' + str(probValue) + '\n')

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
runLog.write ('Results are saved to ../results/versionNumber_genreName_eng_prob_data.txt' + '\n')
runLog.close()

# write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Genre: ' + genreName)
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Results are saved to ../results/versionNumber_genreName_eng_prob_data.txt')
