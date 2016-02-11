# Simple Hybridity Metric
# v. a0.5
# 11th Feb. 2016
# by jmg*AT*phasechange*DOT*info

# Examines a graph and calculates node hybridty (NodeH) and graph hybridity (GraphH)

# Import packages
import os
import networkx as nx

versionNumber = ("a05")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
    os.makedirs("results")

# open file for writing log
logPath = os.path.join("logs", 'shm_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# open file for results output
resultsPath = os.path.join("results", 'shm_' + versionNumber + '.txt')
resultsFile = open(resultsPath, 'w')

# ..and begin..
runLog.write ('\n' + 'Simple Hybridity Metric DooDad | ' + 'Version: ' + versionNumber + '\n' + '\n')
print ('\n' + 'Simple Hybridity Metric DooDad | ' + 'Version: ' + versionNumber + ' | Starting' + '\n')

omegaYear = int(input ("Enter the up-to-year of this graph: "))

# Read DiGraph GEXF file to generate network
diGraphPath = os.path.join("gexf", 'shm.gexf')
diEnGraph = nx.read_gexf(diGraphPath)

# Create empty dictionary for finalNodeSig values
finalNodeSigDict = {}

# Create dictionary for artist totals and clean up unicode
nodeArtistsDict = nx.get_node_attributes(diEnGraph,'totalArtists')
for key, value in nodeArtistsDict.items():
	nodeArtistsDict[key] = int(str(value).replace("u'",""))

# Calculate graph total artists from dictionary
graphTotalArtists = float(sum(nodeArtistsDict.values()))

# Calculate NodeH values
# Examine every node
for node in diEnGraph.nodes():

	# Assign variables
	edgeSig = 0.0
	totalEdgeSig = 0.0
	nodeTotalArtists = float(nodeArtistsDict[node])
	nodeSig = nodeTotalArtists / graphTotalArtists
	nodeInDeg = diEnGraph.in_degree(node)
	inEdges = diEnGraph.in_edges(node, data=True)

	print ('\n' + str(node))
	print ("nodeInDeg for " + str(node) + " is: " + str(nodeInDeg))

	# Assign non-hybrid heuristic NodeH values if possible
	if nodeInDeg == 0 or nodeInDeg == 1:
		NodeH = 0.0

		print ("NodeH set to 0 because nodeInDeg is " + str(nodeInDeg))

	# Examine all incoming edges for significance
	if nodeInDeg > 1:
		for edge in inEdges:
			edgeStr = str(edge).replace("u'","").replace("'","").replace("(","").replace(")","").replace(" ","")
			nodeU, nodeV, edgeId, edgeWeight = edgeStr.split(",")
			inEdgeWeight = float(str(edgeWeight).replace("{","").replace("weight:","").replace("}",""))
			edgeSig = inEdgeWeight / nodeTotalArtists
			totalEdgeSig += edgeSig

	# Maximum value of NodeH is 1.0, so sort that out
	if totalEdgeSig > 1.0: 
		NodeH = 1.0 
	else: 
		NodeH = totalEdgeSig

	# Final node significance is NodeHybridity * NodeSignificance
	finalNodeSig = NodeH * nodeSig

	#Update nodeSigDict dictionary for later use
	finalNodeSigDict[node] = finalNodeSig

	print ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists))
	print ("Node significance for " + str(node) + " is: " + str(nodeSig))
	print ("NodeH for " + str(node) + " is: " + str(NodeH))
	print ("Final node significance for " + str(node) + " is: " + str(finalNodeSig))

	runLog.write ("Node total artists for " + str(node) + " is: " + str(nodeTotalArtists) + '\n')
	runLog.write ("Node significance for " + str(node) + " is: " + str(nodeSig) + '\n')
	runLog.write ("NodeH for " + str(node) + " is: " + str(NodeH) + '\n')
	runLog.write ("Final node significance for " + str(node) + " is: " + str(finalNodeSig) + '\n')

print ('\n' + "Final node sig dictionary: " + str(finalNodeSigDict))

# Calculate GraphH, the sum of all nodeSig values
GraphH = sum(finalNodeSigDict.values())

print
print ("Up to year: " + str(omegaYear))
print ("Number of nodes: " + str(nx.number_of_nodes(diEnGraph)))
print ("Graph total artists: " + str(graphTotalArtists))
print ("GraphH: " + str(sum(finalNodeSigDict.values())))
print

# Write to log
runLog.write ('\n' + "Up to year: " + str(omegaYear) + '\n')
runLog.write ("Number of nodes: " + str(nx.number_of_nodes(diEnGraph)) + '\n')
runLog.write ("Graph total artists: " + str(graphTotalArtists) + '\n')
runLog.write ("GraphH: " + str(sum(finalNodeSigDict.values())) + '\n' + '\n')
runLog.close()

# Write to results
resultsFile.write ('\n' + "Up to year: " + str(omegaYear) + '\n')
resultsFile.write ("Number of nodes: " + str(nx.number_of_nodes(diEnGraph)) + '\n')
resultsFile.write ("Graph total artists: " + str(graphTotalArtists) + '\n')
resultsFile.write ("GraphH: " + str(sum(finalNodeSigDict.values())) + '\n' + '\n')
resultsFile.close()
