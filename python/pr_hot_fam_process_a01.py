# PageRank, Familiarity, Hotttnesss Processor for Hybridity Tools
# by jmg*AT*phasechange*DOT*info
# Version a01
# March 6th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Reads 'fam_hot' and 'pagerank' data, orders and writes to new file

# import packages
import os

versionNumber = "a01"

# open file for results output
resultsPath = os.path.join("results", 'pr_hot_fam_results_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')
resultsFile.write("Genre" + "," + "PageRank" + "," + "Mean Familiarity" + "," + "Mean Hotttness" + '\n')

# Get PageRank data and read
prInputPath = os.path.join("results", 'pr_results_a01.txt')
prInput = open(prInputPath, 'r').readlines()

prDict = {}

for line in prInput:

	genreName, pageRank, newLine = line.split(",")
	prDict.update({str(genreName):float(pageRank)})

print (prDict)

# Get Fam_Hot data and read
fhInputPath = os.path.join("results", 'eng_fam_hot_b03_data.txt')
fhInput = open(fhInputPath, 'r').readlines()

firstLine = fhInput.pop(0)

for line in fhInput:

	genre, totalArtists, loFam, meanFam, hiFam, loHot, meanHot, hiHot, newLine = line.split(",")

	if genre in prDict.keys():

		prValue = prDict[genre]
		resultsFile.write(str(genre) + "," + str(prValue) + "," + str(meanFam) + ","  + str(meanHot) + "," + '\n')

