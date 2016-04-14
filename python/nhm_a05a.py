# Network Hybridity Metric
# v. a0.5a
# March 16th 2016
# by jmg*AT*phasechange*DOT*info

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# This version utilises Dr. C. Rhodes 'leave out the biggest one' concept.

# Examines a graph and calculates node hybridty (Hnode) and graph hybridity (Hgraph)
# This version looks at all loose files in 'gexf/directed/' with a '.gexf' extension. 
# These should be directed-gexf files output by 'eng_network_wd'
# The filename is used as the omega-year of the graph. 

# Import packages
import os
import networkx as nx
from datetime import datetime

versionNumber = ("a05a")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'data' subdirectories if necessary
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data/node-edge-lists"):
    os.makedirs("data/node-edge-lists")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'nhm_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open file for plot - file output
plotPath = os.path.join("data", 'nhm_plot.txt')
plotFile = open(plotPath, 'w')
plotFile.write("OmegaYear" + ',' + "Nodes" + ',' + "Hgraph" + ',' + "Mean-Hnode" + ',' + "Perc-Hnode>0.5" + ',' + "Perc-Progen" + '\n')

# open file for results output
resultsPath = os.path.join("results", 'nhm_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# get list of files from gexf folder
gexfPath = 'gexf/directed'
fileNames = [f for f in os.listdir(gexfPath) if f.endswith('.gexf')]

# ..and begin..
runLog.write ('\n' + 'Network Hybridity Metric - Alpha | ' + 'Version: ' + versionNumber + '\n' + '\n')
resultsFile.write ('\n' + 'Network Hybridity Metric - Alpha | ' + 'Version: ' + versionNumber + '\n')
print ('\n' + 'Network Hybridity Metric - Alpha | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

for index in range(len(fileNames)):

	# Read DiGraph GEXF file to generate network
	diGraphPath = os.path.join("gexf/directed", fileNames[index])
	diGraphFile = str(fileNames[index])
	diGraphYear, fileExtension = diGraphFile.split(".")
	omegaYear = int(diGraphYear)
	diEnGraph = nx.read_gexf(diGraphPath)


	# open file for node results output
	nodeDataPath = os.path.join("data/node-edge-lists", 'nhm_nodes_' + versionNumber + "_" + str(omegaYear) + '.txt')
	nodeFile = open(nodeDataPath, 'a')
	nodeFile.write ("Genre" + "," + "In-Degree" + "," + "Out-Degree" + "," + "Hnode" + "," + "Node Imp" + "," + "Final Node Imp" + '\n')


	# Create empty dictionaries for Hnode and finalNodeImp values
	HnodeDict = {}
	finalNodeImpDict = {}

	# Create dictionary for artist totals and clean up unicode
	nodeArtistsDict = nx.get_node_attributes(diEnGraph,'totalArtists')
	for key, value in nodeArtistsDict.items():
		nodeArtistsDict[key] = int(str(value).replace("u'",""))

	# Calculate graph total artists from dictionary
	graphTotalArtists = float(sum(nodeArtistsDict.values()))

	# Counters
	totalHnode = 0
	progenNodes = 0
	nonHybrids = 0
	totalNonHybrids = 0
	isolates = 0

	# Get node count for graph
	totalGraphNodes = nx.number_of_nodes(diEnGraph)

	# Calculate Hnode values
	# Examine every node
	for node in diEnGraph.nodes():

		# Assign variables
		edgeImp = 0.0
		edgeImpList = []
		totalEdgeImp = 0.0
		nodeTotalArtists = float(nodeArtistsDict[node])
		nodeImp = nodeTotalArtists / graphTotalArtists
		nodeInDeg = diEnGraph.in_degree(node)
		nodeOutDeg = diEnGraph.out_degree(node)
		inEdges = diEnGraph.in_edges(node, data=True)

		print ('\n' + str(node))
		print ("Node in-degree for " + str(node) + " is: " + str(nodeInDeg))
		print ("Node out-degree for " + str(node) + " is: " + str(nodeOutDeg))

		runLog.write ('\n' + str(node) + '\n')	
		runLog.write ("Node in-degree for " + str(node) + " is: " + str(nodeInDeg) + '\n')
		runLog.write ("Node out-degree for " + str(node) + " is: " + str(nodeOutDeg) + '\n')

		# Assign non-hybrid heuristic Hnode values if possible
		# Node is an isolate, so cannot be a hybrid
		if nodeInDeg == 0 and nodeOutDeg == 0:
			Hnode = 0.0

			# Count as an isolate and a non-hybrid
			isolates += 1
			totalNonHybrids += 1

			print ("Hnode set to 0 because node is an isolate (node in- and out-degree is 0) ")
			runLog.write ("Hnode set to 0 because node is an isolate (node in- and out-degree is 0) " + '\n')

		# Node is a progenitor
		if nodeInDeg == 0 and nodeOutDeg != 0:
			Hnode = 0.0

			# Count as a progenitor and a non-hybrid
			progenNodes += 1
			totalNonHybrids += 1

			print ("Hnode set to 0 because genre is a progenitor (node in-degree is 0) ")
			runLog.write ("Hnode set to 0 because genre is a progenitor (node in-degree is 0) " + '\n')

		if nodeInDeg == 1:
			Hnode = 0.0

			# Count non-hybrids
			totalNonHybrids += 1

			print ("Hnode set to 0 because node in-degree is " + str(nodeInDeg))
			runLog.write ("Hnode set to 0 because node in-degree is " + str(nodeInDeg) + '\n')

		# Examine all incoming edges for importance
		if nodeInDeg > 1:
			for edge in inEdges:
				edgeStr = str(edge).replace("u'","").replace("'","").replace("(","").replace(")","").replace(" ","")
				nodeU, nodeV, edgeId, edgeWeight = edgeStr.split(",")
				inEdgeWeight = float(str(edgeWeight).replace("{","").replace("weight:","").replace("}",""))
				edgeImp = inEdgeWeight / nodeTotalArtists
				edgeImpList.append(edgeImp)

			print
			print ("Complete list of edge importance: ")
			print (edgeImpList)
			print

			# Remove largest group, as per CR's instructions
			edgeImpList.remove(max(edgeImpList))

			print
			print ("Edge importance list after removal of largest: ")
			print (edgeImpList)
			print

			# Calculate totalEdgeImp
			for i in range (len(edgeImpList)):
				totalEdgeImp += edgeImpList[i]

		# Maximum value of Hnode is 1.0, so sort that out
		if totalEdgeImp > 1.0: 
			Hnode = 1.0 
		else: 
			Hnode = totalEdgeImp

		# Count Hnode > 0.5 hybrids 
		if Hnode > 0.5:
			totalHnode += 1

		# Update HnodeDict dictionary for later use
		HnodeDict[node] = Hnode

		# Final node importance is NodeHybridity * NodeImportance
		finalNodeImp = Hnode * nodeImp

		# Update finalNodeImpDict dictionary for later use
		finalNodeImpDict[node] = finalNodeImp

		print ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists))
		print ("Node importance of " + str(node) + " is: " + str(nodeImp))
		print ("Hnode for " + str(node) + " is: " + str(Hnode))
		print ("Final node importance of " + str(node) + " is: " + str(finalNodeImp))

		nodeFile.write (str(node) + "," + str(nodeInDeg) + "," + str(nodeOutDeg) + "," + str(Hnode) + "," + str(nodeImp) + "," + str(finalNodeImp) + '\n')

		runLog.write ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists) + '\n')
		runLog.write ("Node importance of " + str(node) + " is: " + str(nodeImp) + '\n')
		runLog.write ("Hnode for " + str(node) + " is: " + str(Hnode) + '\n')
		runLog.write ("Final node importance of " + str(node) + " is: " + str(finalNodeImp) + '\n')

	nodeFile.close()

	# Calculate non-hybrids (not including isolates and progenitors)
	nonHybrids = ((totalNonHybrids - progenNodes) - isolates)

	# Calculate percentages
	percProgen = float(100 * (float(progenNodes) / float(totalGraphNodes)))
	percHnode = float(100 * (float(totalHnode) / float(totalGraphNodes)))
	percNonHybrids = float(100 * (float(nonHybrids) / float(totalGraphNodes)))
	percTotalNonHybrids = float(100 * (float(totalNonHybrids) / float(totalGraphNodes)))

	# Calculate Mean Hnode
	meanHnode = (sum(HnodeDict.values())) / float(totalGraphNodes)

	# Calculate Hgraph, the sum of all finalNodeImp values
	Hgraph = sum(finalNodeImpDict.values())

	# Write to plot file
	plotFile.write(str(omegaYear) + ',' + str(totalGraphNodes) + ',' + str(Hgraph) + ',' + str(meanHnode) + ',' + str(percHnode) + ',' + str(percProgen) + '\n')

	print
	print ("Omega year: " + str(omegaYear))
	print ("Number of nodes: " + str(totalGraphNodes))
	print ("Number of progenitors (in-degree = 0): " + str(progenNodes))
	print ('Number of isolates (in- and out-degree = 0): ' + str(isolates))
	print ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids))
	print ("Total number of non-hybrids: " + str(totalNonHybrids))
	print ("Number of Hnode>0.5 genres: " + str(totalHnode))
	print ("Percentage of progenitors: " + str(percProgen))
	print ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids))
	print ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids))
	print ("Percentage of Hnode>0.5 genres: " + str(percHnode))
	print ("Graph total artists: " + str(graphTotalArtists))
	print ("Mean Node Hybridity: " + str(meanHnode))
	print ("Graph Hybridity (GraphH): " + str(Hgraph))
	print

	# Write to log
	runLog.write ('\n' + "Omega year: " + str(omegaYear) + '\n')
	runLog.write ("Number of nodes: " + str(totalGraphNodes) + '\n')
	runLog.write ("Number of progenitors (in-degree = 0): " + str(progenNodes) + '\n')
	runLog.write ('Number of isolates (in- and out-degree = 0): ' + str(isolates) + '\n')
	runLog.write ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids) + '\n')
	runLog.write ("Total number of non-hybrids: " + str(totalNonHybrids) + '\n')
	runLog.write ("Number of Hnode>0.5 genres: " + str(totalHnode) + '\n')
	runLog.write ("Percentage of progenitors: " + str(percProgen) + '\n')
	runLog.write ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids) + '\n')
	runLog.write ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids) + '\n')
	runLog.write ("Percentage of Hnode>0.5 genres: " + str(percHnode) + '\n')
	runLog.write ("Graph total artists: " + str(graphTotalArtists) + '\n')
	runLog.write ("Mean Node Hybridity: " + str(meanHnode) + '\n')
	runLog.write ("Graph Hybridity (GraphH): " + str(Hgraph) + '\n')
	runLog.write ('\n' + "=============================================================" + '\n')

	# Write to results
	resultsFile.write ('\n' + "Omega year: " + str(omegaYear) + '\n')
	resultsFile.write ("Number of nodes: " + str(totalGraphNodes) + '\n')
	resultsFile.write ("Number of progenitors (in-degree = 0): " + str(progenNodes) + '\n')
	resultsFile.write ('Number of isolates (in- and out-degree = 0): ' + str(isolates) + '\n')
	resultsFile.write ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids) + '\n')
	resultsFile.write ("Total number of non-hybrids: " + str(totalNonHybrids) + '\n')
	resultsFile.write ("Number of Hnode>0.5 genres: " + str(totalHnode) + '\n')
	resultsFile.write ("Percentage of progenitors: " + str(percProgen) + '\n')
	resultsFile.write ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids) + '\n')
	resultsFile.write ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids) + '\n')
	resultsFile.write ("Percentage of Hnode>0.5 genres: " + str(percHnode) + '\n')
	resultsFile.write ("Graph total artists: " + str(graphTotalArtists) + '\n')
	resultsFile.write ("Mean Node Hybridity: " + str(meanHnode) + '\n')
	resultsFile.write ("Graph Hybridity (GraphH): " + str(Hgraph) + '\n')
	resultsFile.write ('\n' + "=============================================================" + '\n')

resultsFile.close()
plotFile.close()
runLog.close()

# End timing of run
endTime = datetime.now()

print('Duration of run : {}'.format(endTime - startTime))
