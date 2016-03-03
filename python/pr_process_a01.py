# PageRank Processor for Hybridity Tools
# by jmg*AT*phasechange*DOT*info
# Version a01
# March 3rd 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Processes PageRank values flung out by 'eng_network_wd_...a.py' (so run AFTER thst, obviously)

# import packages
import os

versionNumber = "a01"

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for results output
resultsPath = os.path.join("results", 'pr_results_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# Get PageRank data and read
dataInputPath = os.path.join("data", 'pagerank.txt')
dataInput = open(dataInputPath, 'r')

pageRankStr = str(dataInput.read()).replace("{","").replace("u'","").replace("': ",",").replace("}", "").replace(", ","\n")

print (pageRankStr)
resultsFile.write (pageRankStr)
