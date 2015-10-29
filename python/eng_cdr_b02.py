# eng_cdr_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 26th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Processes file 'data/date_ratios.txt'
# Writes results to 'results/versionNumber_eng_cdr.txt'
# Writes run log to 'logs/versionNumber_eng_cdr_log.txt'

# Run AFTER 'en_genre.py'

# import packages
import os
from datetime import datetime

versionNumber = ("b02")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_cdr_log.txt')
runLog = open(logPath, 'a')

# open file for data output
resultsPath = os.path.join("results", versionNumber + '_eng_cdr.txt')
processedResults = open(resultsPath, 'a')

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
	print('Genre: ' + genre + ' Percentage of artists with dates: ' + str(dateRatio))

# close input file
dataInput.close()

# close output file
processedResults.close()

# End timing of run
endTime = datetime.now()

# Write to log
runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Version: ' + versionNumber + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write('Output saved to results/versionNumber_calc_date_ratios.txt' + '\n')
runLog.close()

# Write to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print('Duration of run : {}'.format(endTime - startTime))
print('Output saved to results/versionNumber_calc_date_ratios.txt')