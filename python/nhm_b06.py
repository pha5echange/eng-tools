# Network Hybridity Metric
# v. b0.6
# October 28th 2016
# by jmg*AT*phasechange*DOT*info

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Examines a graph and calculates node hybridty (Hnode) and graph hybridity (Hgraph)
# Looks at all loose files in 'gexf/directed/' with a '.gexf' extension (directed-gexf files output by 'eng_network_wd')
# The filename is used as the omega-year of the graph. 

# This version utilises 'leave out the Principal Ancestor,' and sets a maximal 'Hnode' value using 'look for new artists' 
# Also counts `sink' nodes (non-zero in-degree and zero out-degree)

# Calculates artist-uniques and artist-instances for entire network.

# Works with time-sliced 'omega year' files.

# Import packages
import os
import networkx as nx
from datetime import datetime

versionNumber = ("b06")

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
plotFile.write("OmegaYear" + ',' + "Nodes" + ',' + "Hgraph" + ',' + "Mean-Hnode" + ',' + "Perc-Hnode>0.5" + ',' + "Perc-Progen" + ',' + "Perc-Sinks" + '\n')

# open file for results output
resultsPath = os.path.join("results", 'nhm_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# get list of files from gexf folder
gexfPath = 'gexf/directed'
fileNames = [f for f in os.listdir(gexfPath) if f.endswith('.gexf')]

# get files from genres folder
genreFiles = os.listdir("genres")

# ..and begin..
runLog.write ('\n' + 'Network Hybridity Metric (JG) - Beta | ' + 'Version: ' + versionNumber + '\n' + '\n')
resultsFile.write ('\n' + 'Network Hybridity Metric (JG) - Beta | ' + 'Version: ' + versionNumber + '\n')
print ('\n' + 'Network Hybridity Metric (JG) - Beta | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

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

	# Calculate graph total artist-instances from dictionary
	graphTotalArtistInstances = float(sum(nodeArtistsDict.values()))

	# Counters
	graphTotalArtists = 0
	totalHnode = 0
	progenNodes = 0
	nonHybrids = 0
	totalNonHybrids = 0
	totalSinkNodes = 0
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
		nodeUartists = []
		nodeVartists = []
		diffArtists = []
		allInArtists = []
		del nodeUartists[:]
		del nodeVartists[:]
		del diffArtists[:]
		del allInArtists[:]
		nodeUset = set()
		nodeUset.clear()
		nodeVset = set()
		nodeVset.clear()
		newVartists = set()
		newVartists.clear()
		totalEdgeWeight = 0
		diffCount = 0
		newVcount = 0
		nodeNewArtists = 0.0
		MaxHnode = 1.0
		Hnode = 0.0
		nodeTotalArtists = float(nodeArtistsDict[node])
		nodeImp = nodeTotalArtists / graphTotalArtistInstances
		nodeInDeg = diEnGraph.in_degree(node)
		nodeOutDeg = diEnGraph.out_degree(node)
		inEdges = diEnGraph.in_edges(node, data=True)

		print ('\n' + str(node))
		print ("Node in-degree for " + str(node) + " is: " + str(nodeInDeg))
		print ("Node out-degree for " + str(node) + " is: " + str(nodeOutDeg))

		runLog.write ('\n' + str(node) + '\n')	
		runLog.write ("Node in-degree for " + str(node) + " is: " + str(nodeInDeg) + '\n')
		runLog.write ("Node out-degree for " + str(node) + " is: " + str(nodeOutDeg) + '\n')

		# Get the node name and assign to 'nodeV'
		#nodeNames = nx.get_node_attributes(diEnGraph, 'label')
		#nodeV = str(nodeNames[node])
		nodeV = str(node)

		# open file 'data/omegaYear/genres/nodeV.txt' and read

		if omegaYear == 0:
			genrePath = os.path.join("genres", nodeV + '.txt')
		else:
			genrePath = os.path.join("ts_data", str(omegaYear), "genres", nodeV + '.txt')

		genreInput = open(genrePath, "r")
			
		for line in genreInput:
			vArtist, vEnid, vArtistStart, vArtistEnd, vFamiliarity, vHotness, vMbid = line.split(",")
			vMB = str(vMbid).replace("\n","")

			# make a list of MBIDs from file
			nodeVartists.append(vMB)

		# Assign non-hybrid heuristic Hnode values if possible
		# Node is an isolate, so cannot be a hybrid
		if nodeInDeg == 0 and nodeOutDeg == 0:
			nodeVset = set(nodeVartists)
			newVCount = len(nodeVset)
			newVartists = nodeVset
			nodeNewArtists = nodeTotalArtists
			MaxHnode = 0.0
			Hnode = 0.0

			# Count as an isolate and a non-hybrid
			isolates += 1
			totalNonHybrids += 1

			print ("Hnode set to 0 because node is an isolate (node in- and out-degree is 0) ")
			runLog.write ("Hnode set to 0 because node is an isolate (node in- and out-degree is 0) " + '\n')

		# Node is a progenitor
		if nodeInDeg == 0 and nodeOutDeg != 0:
			nodeVset = set(nodeVartists)
			newVCount = len(nodeVset)
			newVartists = nodeVset
			nodeNewArtists = nodeTotalArtists
			MaxHnode = 0.0
			Hnode = 0.0

			# Count as a progenitor and a non-hybrid
			progenNodes += 1
			totalNonHybrids += 1

			print ("Hnode set to 0 because genre is a progenitor (node in-degree is 0) ")
			runLog.write ("Hnode set to 0 because genre is a progenitor (node in-degree is 0) " + '\n')

		# Node MAY be a hybrid
		if nodeInDeg > 0:
			del allInArtists[:]
			newVcount = 0
			nodeVset.clear()
			newVartists.clear()

			# Examine all incoming edges
			for edge in inEdges:
				del nodeUartists[:]
				del diffArtists[:]
				nodeUset.clear()
				edgeStr = str(edge).replace("u'","").replace("'","").replace("(","").replace(")","").replace(" ","")
				nodeU, nodeV, edgeId, edgeWeight = edgeStr.split(",")
				inEdgeWeight = float(str(edgeWeight).replace("{","").replace("weight:","").replace("}",""))
				edgeImp = inEdgeWeight / nodeTotalArtists
				edgeImpList.append(edgeImp)

				# open file 'data/omegaYear/genres/nodeU' and read
				if omegaYear == 0:
					sourceGenrePath = os.path.join("genres", nodeU + '.txt')
				else:
					sourceGenrePath = os.path.join("ts_data", str(omegaYear), "genres", nodeU + '.txt')

				sourceGenreFile = open(sourceGenrePath, 'r')

				for line in sourceGenreFile:
					artist, enid, artistStart, artistEnd, familiarity, hotness, mbid = line.split(",")
					MB = str(mbid).replace("\n","") 

					# make a list of MBIDs from file
					nodeUartists.append(MB)

				allInArtists.extend(nodeUartists)

			# Remove largest group (Principal Ancestor)
			edgeImpList.remove(max(edgeImpList))

			# Calculate total edgeImp
			for i in range (len(edgeImpList)):
				totalEdgeImp += edgeImpList[i]

			# Compare nodeU and nodeV lists
			nodeVset = set(nodeVartists)
			nodeUset = set(allInArtists)
			diffArtists = list(nodeVset.difference(nodeUset))
			diffCount = len(diffArtists)
			newVartists = set(diffArtists)
			newVCount = len(newVartists)
			nodeNewArtists = float(len(newVartists))

			# Node is a non-hybrid
			if nodeInDeg == 1:
				MaxHnode = 0.0
				Hnode = 0.0

				# Count non-hybrids
				totalNonHybrids += 1

				print ("Hnode set to 0 because node in-degree is " + str(nodeInDeg))
				runLog.write ("Hnode set to 0 because node in-degree is " + str(nodeInDeg) + '\n')

			# Node is a hybrid
			if nodeInDeg > 1:
				MaxHnode = 1.0 - (nodeNewArtists / nodeTotalArtists)
				Hnode = totalEdgeImp

		# Node is a sink
		if nodeInDeg > 0 and nodeOutDeg == 0:
			# Count sink-nodes
			totalSinkNodes += 1

			print ("Node has a non-zero in-degree and an out-degree of 0. It is therefore a sink. ")
			runLog.write ("Node has a non-zero in-degree and an out-degree of 0. It is therefore a sink. " + '\n')

		# Maximum value of Hnode is MaxHnode
		if Hnode > MaxHnode: 
			Hnode = MaxHnode
			
		# Count Hnode > 0.5 hybrids 
		if Hnode > 0.5:
			totalHnode += 1

		# Increment graphTotalArtists with newVcount
		graphTotalArtists += newVCount

		# Update HnodeDict dictionary for later use
		HnodeDict[node] = Hnode

		# Final node importance is NodeHybridity * NodeImportance
		finalNodeImp = Hnode * nodeImp

		# Update finalNodeImpDict dictionary for later use
		finalNodeImpDict[node] = finalNodeImp

		print ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists))
		print ("Node new artists total for " + str(node) + " is: " + str(nodeNewArtists))
		print ("Node importance of " + str(node) + " is: " + str(nodeImp))
		print ("Hnode for " + str(node) + " is: " + str(Hnode))
		print ("Final node importance of " + str(node) + " is: " + str(finalNodeImp))
		print ("NewVCount: " + str(newVCount))
		print ("NewVartists: " + str(newVartists))

		nodeFile.write (str(node) + "," + str(nodeInDeg) + "," + str(nodeOutDeg) + "," + str(Hnode) + "," + str(nodeImp) + "," + str(finalNodeImp) + '\n')

		runLog.write ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists) + '\n')
		runLog.write ("Node new artists total for " + str(node) + " is: " + str(nodeNewArtists) + '\n')
		runLog.write ("Node importance of " + str(node) + " is: " + str(nodeImp) + '\n')
		runLog.write ("Hnode for " + str(node) + " is: " + str(Hnode) + '\n')
		runLog.write ("Final node importance of " + str(node) + " is: " + str(finalNodeImp) + '\n')
		runLog.write ("NewVCount: " + str(newVCount) + '\n')
		runLog.write ("NewVartists: " + str(newVartists) + '\n')

	nodeFile.close()

	# Calculate non-hybrids (not including isolates and progenitors)
	nonHybrids = ((totalNonHybrids - progenNodes) - isolates)

	# Calculate percentages
	percProgen = float(100 * (float(progenNodes) / float(totalGraphNodes)))
	percHnode = float(100 * (float(totalHnode) / float(totalGraphNodes)))
	percNonHybrids = float(100 * (float(nonHybrids) / float(totalGraphNodes)))
	percTotalNonHybrids = float(100 * (float(totalNonHybrids) / float(totalGraphNodes)))
	percTotalSinks = float(100 * (float(totalSinkNodes) / float(totalGraphNodes)))

	# Calculate Mean Hnode
	meanHnode = (sum(HnodeDict.values())) / float(totalGraphNodes)

	# Calculate Hgraph, the sum of all finalNodeImp values
	Hgraph = sum(finalNodeImpDict.values())

	# Write to plot file
	plotFile.write(str(omegaYear) + ',' + str(totalGraphNodes) + ',' + str(Hgraph) + ',' + str(meanHnode) + ',' + str(percHnode) + ',' + str(percProgen) + ',' + str(percTotalSinks) + '\n')

	print
	print ("Omega year: " + str(omegaYear))
	print ("Number of nodes: " + str(totalGraphNodes))
	print ("Number of progenitors (in-degree = 0): " + str(progenNodes))
	print ('Number of isolates (in- and out-degree = 0): ' + str(isolates))
	print ('Number of sinks (in-degree != 0 and out-degree = 0): ' + str(totalSinkNodes))
	print ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids))
	print ("Total number of non-hybrids: " + str(totalNonHybrids))
	print ("Number of Hnode>0.5 genres: " + str(totalHnode))
	print ("Percentage of progenitors: " + str(percProgen))
	print ("Percentage of sinks: " + str(percTotalSinks))
	print ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids))
	print ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids))
	print ("Percentage of Hnode>0.5 genres: " + str(percHnode))
	print ("Graph total artists: " + str(graphTotalArtists))
	print ("Graph total artist-instances: " + str(graphTotalArtistInstances))
	print ("Mean Node Hybridity: " + str(meanHnode))
	print ("Graph Hybridity (GraphH): " + str(Hgraph))
	print

	# Write to log
	runLog.write ('\n' + "Omega year: " + str(omegaYear) + '\n')
	runLog.write ("Number of nodes: " + str(totalGraphNodes) + '\n')
	runLog.write ("Number of progenitors (in-degree = 0): " + str(progenNodes) + '\n')
	runLog.write ('Number of isolates (in- and out-degree = 0): ' + str(isolates) + '\n')
	runLog.write ('Number of sinks (in-degree != 0 and out-degree = 0): ' + str(totalSinkNodes) + '\n')
	runLog.write ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids) + '\n')
	runLog.write ("Total number of non-hybrids: " + str(totalNonHybrids) + '\n')
	runLog.write ("Number of Hnode>0.5 genres: " + str(totalHnode) + '\n')
	runLog.write ("Percentage of progenitors: " + str(percProgen) + '\n')
	runLog.write ("Percentage of sinks: " + str(percTotalSinks) + '\n')
	runLog.write ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids) + '\n')
	runLog.write ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids) + '\n')
	runLog.write ("Percentage of Hnode>0.5 genres: " + str(percHnode) + '\n')
	runLog.write ("Graph total artists: " + str(graphTotalArtists) + '\n')
	runLog.write ("Graph total artist-instances: " + str(graphTotalArtistInstances) + '\n')
	runLog.write ("Mean Node Hybridity: " + str(meanHnode) + '\n')
	runLog.write ("Graph Hybridity (GraphH): " + str(Hgraph) + '\n')
	runLog.write ('\n' + "=============================================================" + '\n')

	# Write to results
	resultsFile.write ('\n' + "Omega year: " + str(omegaYear) + '\n')
	resultsFile.write ("Number of nodes: " + str(totalGraphNodes) + '\n')
	resultsFile.write ("Number of progenitors (in-degree = 0): " + str(progenNodes) + '\n')
	resultsFile.write ('Number of isolates (in- and out-degree = 0): ' + str(isolates) + '\n')
	resultsFile.write ('Number of sinks (in-degree != 0 and out-degree = 0): ' + str(totalSinkNodes) + '\n')
	resultsFile.write ("Number of non-Hybrids (minus progenitors and isolates): " + str(nonHybrids) + '\n')
	resultsFile.write ("Total number of non-hybrids: " + str(totalNonHybrids) + '\n')
	resultsFile.write ("Number of Hnode>0.5 genres: " + str(totalHnode) + '\n')
	resultsFile.write ("Percentage of progenitors: " + str(percProgen) + '\n')
	resultsFile.write ("Percentage of sinks: " + str(percTotalSinks) + '\n')
	resultsFile.write ("Percentage of non-hybrids (minus progenitors and isolates): " + str(percNonHybrids) + '\n')
	resultsFile.write ("Percentage of non-hybrids (includes progenitors and isolates): " + str(percTotalNonHybrids) + '\n')
	resultsFile.write ("Percentage of Hnode>0.5 genres: " + str(percHnode) + '\n')
	resultsFile.write ("Graph total artists: " + str(graphTotalArtists) + '\n')	
	resultsFile.write ("Graph total artist-instances: " + str(graphTotalArtistInstances) + '\n')
	resultsFile.write ("Mean Node Hybridity: " + str(meanHnode) + '\n')
	resultsFile.write ("Graph Hybridity (GraphH): " + str(Hgraph) + '\n')
	resultsFile.write ('\n' + "=============================================================" + '\n')

resultsFile.close()
plotFile.close()
runLog.close()

# End timing of run
endTime = datetime.now()

print('Duration of run : {}'.format(endTime - startTime))
