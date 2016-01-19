# eng_cdr_b04.py
# Version b04
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes file 'data/date_ratios.txt'
# Writes results to 'results/eng_cdr_versionNumber.txt'
# Also writes a list of genres with numbers of artists written to 'data/eng_artistNums.txt' for use by later by 'eng_network_wd.py'
# Writes run log to 'logs/eng_cdr_versionNumber_log.txt'

# Run AFTER 'en_genre.py'

# import packages
import os
from datetime import datetime

versionNumber = ("b04")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'eng_cdr_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open file for data output
dataPath = os.path.join("data", 'eng_artistNums.txt')
artistNums = open(dataPath, 'w')

# open file for results output
resultsPath = os.path.join("results", 'eng_cdr_' + versionNumber + '.txt')
processedResults = open(resultsPath, 'w')

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# ..and begin..
runLog.write ('\n' + 'Genre Data Calc Date Ratios Results Processor | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Genre Data Calc Date Ratios Processor | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# look for file in 'data' subfolder
pathname = os.path.join("data", 'date_ratios.txt')
dataInput = open(pathname, "r")

# read lines from the file
for line in dataInput:

	# split line, calculate and write results
	genre, returned, written = line.split(",")
	floatWritten = float(written)
	floatReturned = float(returned)
	dateRatio = float(floatWritten/floatReturned * 100)
	processedResults.write(genre + ',' + str(dateRatio) + '\n')
	artistNums.write(genre + ',' + str(returned) + ',' + '\n')
	print('Genre: ' + genre + ' Percentage of artists with dates: ' + str(dateRatio))

# close input file
dataInput.close()

# close output files
processedResults.close()
artistNums.close()

# End timing of run
endTime = datetime.now()

# Write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write('Output saved to results/eng_cdr_versionNumber.txt' + '\n')
runLog.write('Artist Numbers saved to data/eng_artistNums.txt' + '\n')
runLog.close()

# Write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
print('Output saved to results/eng_cdr_versionNumber.txt')
print('Artist Numbers saved to data/eng_artistNums.txt' + '\n')
