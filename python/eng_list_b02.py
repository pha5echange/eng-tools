# eng_list_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# February 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Gets list of genres from Echonest utilising pyen
# Uses 'genre/list' method
# Reads API Key from 'apikey.txt'
# Writes to 'lists/datestamp_versionNumber_eng_list.txt' subdirectory

# import packages
import os
import pyen
from datetime import datetime

# deal with unicode error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# version
versionNumber = ("b02")

# create 'lists' subdirectory if necessary
if not os.path.exists("lists"):
    os.makedirs("lists")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# open and read 'apikey.txt'
apiKeyPath = os.path.join("config", 'apikey.txt')
apiKeyFile = open(apiKeyPath, 'r')
apiKey = str(apiKeyFile.read())

# open file for writing data
listPath = os.path.join("lists", str(runDate) + '_' + versionNumber + '_eng_list.txt')
genreList = open(listPath, 'w')

print ('\n' + 'Echonest Genre List | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

# call Echonest to get 'genres' response
en = pyen.Pyen(apiKey)
response = en.get('genre/list', results = ['2000'])

for g in response['genres']:
	genreList.write(str(g['name']) + '\n')
	print g['name']

# End timing of run
endTime = datetime.now()

# write results of run to file
genreList.write ('\n' + 'Echonest Genre List | Run Information' + '\n' + '\n')
genreList.write ('Version: ' + versionNumber + '\n')
genreList.write ('Date of run: {}'.format(runDate) + '\n')
genreList.write ('API Key: ' + apiKey + '\n')
genreList.write ('Genres returned: ' + str(len(response['genres'])) + '\n')
genreList.write ('Duration of run : {}'.format(endTime - startTime) + '\n') 
genreList.write ('Data is saved to ../lists/')
genreList.close ()

# close file
genreList.close()

# write results of run to screen
print ('\n' + 'Run Information' + '\n')
print ('Version: ' + versionNumber)
print ('Date of run: {}'.format(runDate))
print ('API Key: ' + apiKey)
print ('Genres returned: ' + str(len(response['genres'])))
print ('Duration of run : {}'.format(endTime - startTime)) 
print ('Data is saved to ../lists/' + '\n')
