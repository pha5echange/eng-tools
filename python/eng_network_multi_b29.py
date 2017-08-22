# eng_network_multi_b29.py
# Version b29
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 29th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Name changed to 'eng_network_multi'

# Plots network graph from edgelist 'ts_data\OMEGAYEAR\OMEGAYEAR_wuGraphData.txt'
# Adds dates from 'data\first_clusters.txt' as node attributes
# Adds artist numbers from 'ts_data\OMEGAYEAR_artistNums.txt' as node attributes
# Removes nodes where date-cluster information is not available
# Removes self-loop edges and zero-degree nodes if required
# Removes nodes based upon 'incepDate' if required - all nodes NEWER than Omega Year are removed
# Displays using parameters from 'config/config_nw.txt'
# Writes 'data\eng_network_wd_nodeList.txt' with nodes and degrees (k), '...edgeList.txt' with neighbours
# Writes analysis files to 'results\'
# Writes gexf files to 'gexf\', including 'gexf\YEAR.gexf' for use by 'nhm.py'
# Writes image to 'networks\'
# This version incorporates PageRank
# Incorporates Artist Time Slicing
# Added 'maxDeg' metric and isolated nodes counter

# Run AFTER 'eng_nodesets.py'

# Import packages
import os
import resource
import numpy as np
import networkx as nx
import community
from networkx.algorithms.approximation import clique
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import datetime

versionNumber = ("b29")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# Create 'data' subdirectories if necessary
if not os.path.exists("data"):
	os.makedirs("data")

if not os.path.exists("data/node-edge-lists"):
	os.makedirs("data/node-edge-lists")

# Create 'gexf' subdirectories if necessary
if not os.path.exists("gexf"):
	os.makedirs("gexf")

if not os.path.exists("gexf/initial"):
	os.makedirs("gexf/initial")

if not os.path.exists("gexf/directed"):
	os.makedirs("gexf/directed")

if not os.path.exists("gexf/final"):
	os.makedirs("gexf/final")

# Create 'results' subdirectories if necessary
if not os.path.exists("results"):
	os.makedirs("results")

if not os.path.exists("results/analysis"):
	os.makedirs("results/analysis")

# Create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# Open file for writing log
logPath = os.path.join("logs", 'eng_network_multi_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "Multi-Network Thing | Version " + versionNumber + " | Starting...")
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Multi-Network Thing | Version " + versionNumber + '\n' + '\n')

# Look for subfolders in `ts_data' and generate datelist from these
dateList = []
datePath = "ts_data/"
dateList = os.listdir(datePath) 
dateSet = set(dateList)

# add 2015 to 'dateSet' 
#dateSet.add(2015)

# Get user input
#print
#dateIP = int(input ("Enter a year to remove nodes that appear AFTER this date (or 0 to leave the network intact): "))
print
selfLoopIP = int(input ("Enter 1 here to remove self-loop edges: "))
print

#omegaYear = str(dateIP)
# Uncomment the line below to facilitate optional isolate removal
#isolatedIP = int(input ("Enter 1 here to remove isolated nodes: "))

# Comment out the line below if uncommenting the line above
isolatedIP = 0

# Remove genres AFTER the Omega Year
#dateInput = open(dateInputPath, 'r')

#for date in dateSet:

#	dateIP = int(date)
#	omegaYear = str(dateIP)

#	for line in dateInput:

#		genreInput, genreDate, newline = line.split(",")
#		intGenreDate = int(genreDate)
	
#		if intGenreDate <= dateIP:
#			genreName = str(omegaYear + '_' + genreInput).replace(" ", "")
#			dateDict[genreName] = genreDate

#sortDates = OrderedDict(sorted(dateDict.items()))
'''
for key, value in sortDates.iteritems():
	cleanDateList.append(int(value))

cleanDateSet = set(cleanDateList)

# Checking stuff
print('cleanDateList: ' + str(cleanDateList) + '\n')
print('cleanDateList elements: ' + str(len(cleanDateList)) + '\n')
print('cleanDateSet: ' + str(cleanDateSet) + '\n')
print ('cleanDateSet elements: ' + str(len(cleanDateSet)))
runLog.write('\n' + 'cleanDateList: ' + str(cleanDateList) + '\n')
runLog.write('\n' + 'cleanDateList elements: ' + str(len(cleanDateList)) + '\n')
runLog.write('\n' + 'cleanDateSet: ' + str(cleanDateSet) + '\n')
runLog.write('\n' + 'cleanDateSet elements: ' + str(len(cleanDateSet)) + '\n')
# End Checking stuff
'''

for date in dateList:

	dateIP = int(date)
	omegaYear = str(date)
	incepList = []
	incepDict = {}
	sortDates = OrderedDict()
	sortArtists = OrderedDict()

	# Generate a dict, list and set containing dates (from 'data\first_cluster.txt')
	dateInputPath = os.path.join("data", 'first_cluster.txt')
	dateInput = open(dateInputPath, 'r')

	for line in dateInput: 

		genreInput, genreDate, newline = line.split(",")
		genreName = str(omegaYear + '_' + genreInput).replace(" ", "")
		incepDict[genreName] = genreDate
		incepList.append(int(genreDate))

	sortDates = OrderedDict(sorted(incepDict.items()))

	# Generate dictionary containing nodenames and artist numbers (from 'ts_data\OMEGAYEAR\_artistNums.txt')
	artistInputPath = os.path.join("ts_data", omegaYear, omegaYear + '_artistNums.txt')
	artistInput = open(artistInputPath, 'r').readlines()

	firstLine = artistInput.pop(0)

	artistDict = {}

	for line in artistInput:
		genreInput, artistNum, newline = line.split(",")
		genreName = str(genreInput).replace(" ", "")
		artistDict[genreName] = artistNum

	sortArtists = OrderedDict(sorted(artistDict.items()))

	# Checking stuff
	print ('\n' + "New Graph Omega Year: " + omegaYear)
	print ("DateList: " + str(dateList) + '\n')
	print ("DateList elements: " + str(len(dateList)) + '\n')
	print ("DateSet: " + str(dateSet) + '\n')
	print ("DateSet elements: " + str(len(dateSet)) + '\n')
	print ("SortDates: " + str(sortDates) + '\n')
	print ("SortDates elements: " + str(len(sortDates)) +'\n')
	print ("SortArtists: " + str(sortArtists) + '\n')
	print ("SortArtists elements: " + str(len(sortArtists)) +'\n')
	print

	runLog.write ('\n' + "New Graph Omega Year: " + omegaYear + '\n')
	runLog.write('\n' + "DateList: " + str(dateList) + '\n')
	runLog.write('\n' + "DateList elements: " + str(len(dateList)) + '\n')
	runLog.write('\n' + "DateSet: " + str(dateSet) + '\n')
	runLog.write('\n' + "DateSet elements: " + str(len(dateSet)) + '\n')
	runLog.write('\n' + "SortDates: " + str(sortDates) + '\n')
	runLog.write('\n' + "SortDates elements: " + str(len(sortDates)) +'\n')
	runLog.write('\n' + "SortArtists: " + str(sortArtists) + '\n')
	runLog.write('\n' + "SortArtists elements: " + str(len(sortArtists)) + '\n')
	# End Checking stuff

	# Open file to write list of nodes
	nodeListPath = os.path.join("ts_data", omegaYear, 'eng_network_multi_' + versionNumber + '_' + omegaYear + '_nodeList.txt')
	nodeListOP = open (nodeListPath, 'w') 

	# Open file to write list of edges
	edgeListPath = os.path.join("ts_data", omegaYear, 'eng_network_multi_' + versionNumber + '_' + omegaYear + '_edgeList.txt')
	edgeListOP = open (edgeListPath, 'w') 

	# Open file for writing initial gexf
	gexfPath = os.path.join("gexf/initial", 'eng_network_multi_' + versionNumber + '_' + omegaYear + '.gexf')
	gexfFile = open(gexfPath, 'w')

	# Open file for writing digraph gexf
	gexfDPath = os.path.join("gexf/directed", omegaYear + '.gexf')
	gexfDFile = open(gexfDPath, 'w')

	# Open file for writing final gexf
	gexfFinPath = os.path.join("gexf/final", 'eng_network_multi_' + versionNumber + '_' + omegaYear + '.gexf')
	gexfFinFile = open(gexfFinPath, 'w')

	# Open file for Page Rank data
	prPath = os.path.join("ts_data", omegaYear, omegaYear +'_multi_pagerank.txt')
	prFile = open(prPath, 'w')

	# Open file for analysis results
	anPath = os.path.join("results/analysis", 'eng_network_multi_' + versionNumber + '_' + omegaYear + '_analysis.txt')
	anFile = open(anPath, 'w')

	# Open file to write image
	#nwImgPath = os.path.join("networks", 'eng_network_' + versionNumber + '_' + omegaYear + '_nw.eps')
	#nwImg = open (nwImgPath, 'w')

	anFile.write ('\n' + "==========================================================================" + '\n' + '\n')
	anFile.write ("Multi-Network Thing | Version " + versionNumber + '\n' + '\n')

	# Read the edgelist and generate undirected graph
	print ('\n' + "Importing Weighted Edge List... ")
	inputPath = os.path.join("ts_data", omegaYear, omegaYear + '_wuGraph_data.txt')
	edgeList = open (inputPath, 'r')
	enGraph = nx.read_weighted_edgelist(edgeList, delimiter=',')

	# Calculate basic graph statistics
	print ('\n' + "Calculating various things... " + '\n')
	nodes = nx.number_of_nodes(enGraph)
	edges = nx.number_of_edges(enGraph)
	density = nx.density(enGraph)
	nodeList = nx.nodes(enGraph)
	nodeList.sort()
	selfLoopEdges = enGraph.number_of_selfloops()
	connections = edges - selfLoopEdges

	print ('Nodes: ' + str(nodes))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Connections (edges minus self-loops): ' + str(connections))
	print ('Density: ' + str(density))
	print ('Nodelist: ' + str(nodeList))
	print

	runLog.write ('\n' + 'Initial data: ' + '\n' + '\n')
	runLog.write ('Omega Year: ' + omegaYear + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')
	runLog.write ('Nodelist: ' + str(nodeList) + '\n')

	# Apply artist numbers of nodes as attributes
	print ('Applying total artist number attribute to nodes...' + '\n')
	runLog.write ('\n' + 'Applying total artist number attribute to nodes...' + '\n' + '\n')
	for i in nodeList:
		enGraph.node[i]['totalArtists'] = sortArtists[i]
	
	# Checking stuff
	allNodes = enGraph.nodes(data = True)
	print ("All Nodes with artist numbers: " + str(allNodes) + '\n')
	runLog.write("All Nodes with artist numbers: " + str(allNodes) + '\n' + '\n')
	# End checking stuff

	# Apply dates of nodes as attributes
	print ('Applying inception date attribute to nodes...' + '\n')
	runLog.write ('\n' + 'Applying inception date attribute to nodes...' + '\n' + '\n')
	for i in nodeList:
		try:
			enGraph.node[i]['incepDate'] = sortDates[i]
		except:
			pass
	
	# Checking stuff
	allNodes = enGraph.nodes(data = True)
	print ("All Nodes with inception dates: " + str(allNodes) + '\n')
	runLog.write("All Nodes with inception dates: " + str(allNodes) + '\n' + '\n')
	# End checking stuff

	# Discard nodes without first-cluster dates
	noDateNode = 0
	print ('Checking genre inception dates, and removing if none...' + '\n')
	runLog.write ('Checking genre inception dates, and removing if none...' + '\n')
	for i in nodeList:
		if not i in sortDates.keys():
			enGraph.remove_node(i)
			print ('Removed node ' + str(i))
			runLog.write('Removed node ' + str(i) + '\n')
			noDateNode += 1

	if noDateNode == 1:
		print ('\n' + 'Removed ' + str(noDateNode) + ' node due to no inception date.')
		runLog.write ('\n' + 'Removed ' + str(noDateNode) + ' node due to no inception date.' + '\n')

	if noDateNode > 1:
		print ('\n' + 'Removed ' + str(noDateNode) + ' nodes due to no inception dates.')
		runLog.write ('\n' + 'Removed ' + str(noDateNode) + ' nodes due to no inception dates.' + '\n')

	# Recalculate basic graph statistics
	print ('\n' + 'Recalculating various things...' + '\n')
	nodes = nx.number_of_nodes(enGraph)
	edges = nx.number_of_edges(enGraph)
	density = nx.density(enGraph)
	nodeList = nx.nodes(enGraph)
	nodeList.sort()
	selfLoopEdges = enGraph.number_of_selfloops()
	connections = edges - selfLoopEdges

	print ('Stage 1 data: ' + '\n')
	print ('Nodes: ' + str(nodes))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Connections (edges minus self-loops): ' + str(connections))
	print ('Density: ' + str(density))
	print

	runLog.write ('\n' + 'Stage 1 data: ' + '\n' + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')

	# Remove nodes where 'incepDate' attribute is NEWER than omega year ('dateIP')
	if dateIP != 0:
		print ("Removing nodes based upon omega year..." + '\n')
		runLog.write('\n' + 'Removing nodes based upon omega year...' + '\n')
		for i in nodeList:
			incepDate = nx.get_node_attributes (enGraph, 'incepDate')
			intIncep = int(incepDate[i])

			if intIncep > dateIP:
				enGraph.remove_node(i)
				print ('Removed newer node ' + str(i) + ' based upon omega year.')

	else:
		print ('No nodes removed based upon omega year.')
		runLog.write ('\n' + 'No nodes removed based upon omega year.' + '\n')

	# Recalculate basic graph statistics
	print ('\n' + 'Recalculating various things...' + '\n')
	nodes = nx.number_of_nodes(enGraph)
	edges = nx.number_of_edges(enGraph)
	density = nx.density(enGraph)
	nodeList = nx.nodes(enGraph)
	nodeList.sort()
	selfLoopEdges = enGraph.number_of_selfloops()
	connections = edges - selfLoopEdges

	print ('Nodes: ' + str(nodes))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Connections (edges minus self-loops): ' + str(connections))
	print ('Density: ' + str(density))
	print

	runLog.write ('\n' + 'Stage 2 data: ' + '\n' + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')

	# Remove self-loops if required
	selfLoopCount = 0
	if selfLoopIP == 1:
		print ('\n' + 'Checking for and removing self-loops...' + '\n')
		runLog.write('\n' + 'Checking for and removing self-loops...' + '\n')
		for u,v,data in enGraph.edges(data=True):
			if u == v:
				enGraph.remove_edge(u,v)
				print ('removed self-loop ' + str(u))
				selfLoopCount += 1
		
		if selfLoopCount == 1:
			print ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edge.')
			runLog.write ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edge.' + '\n')

		if selfLoopCount > 1:
			print ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edges.')
			runLog.write ('\n' + 'Removed ' + str(selfLoopCount) + ' self-loop edges.' + '\n')
	else:
		print ('Self-loops intact.' + '\n')
		runLog.write('\n' + 'Self-loops intact.' + '\n')

	# Remove zero degree nodes if required
	isolateCount = 0
	if isolatedIP == 1:
		print ('\n' + 'Checking for and removing isolated (zero degree) nodes...' +'\n')
		runLog.write('\n' + 'Checking for and removing isolated (zero degree) nodes...' +'\n' + '\n')
		for i in nodeList:
			if nx.is_isolate(enGraph,i):
				enGraph.remove_node(i)
				print ('Removed isolated node ' + str(i))
				runLog.write('Removed isolated node ' + str(i) + '\n')
				isolateCount += 1

		if isolateCount == 1:
			print ('\n' + "Removed " + str(isolateCount) + " isolated node. " + '\n')
			runLog.write ('\n' + "Removed " + str(isolateCount) + " isolated node. " + '\n')

		if isolateCount > 1:
			print ('\n' + "Removed " + str(isolateCount) + " isolated nodes. " + '\n')
			runLog.write ('\n' + "Removed " + str(isolateCount) + " isolated nodes. " + '\n')

	else:

		for i in nodeList:
			if nx.is_isolate(enGraph,i):
				isolateCount += 1

		if isolateCount == 1:
			print ('\n' + str(isolateCount) + ' isolated node intact.')
			runLog.write('\n' + str(isolateCount) + ' isolated node intact.' + '\n')

		if isolateCount > 1:
			print ('\n' + str(isolateCount) + ' isolated nodes intact.')
			runLog.write('\n' + str(isolateCount) + ' isolated nodes intact.' + '\n')

	# Recalculate basic graph statistics
	print ('Recalculating various things...' + '\n')
	nodes = nx.number_of_nodes(enGraph)
	edges = nx.number_of_edges(enGraph)
	density = nx.density(enGraph)
	nodeList = nx.nodes(enGraph)
	nodeList.sort()
	selfLoopEdges = enGraph.number_of_selfloops()

	print ('Nodes: ' + str(nodes))
	print ('Isolated nodes:' + str(isolateCount))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Density: ' + str(density))
	print

	runLog.write ('\n' + 'Stage 3 data: ' + '\n' + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')

	# Clean edge-labels
	print ('Cleaning edge labels...')
	labels = {}
	for u,v,data in enGraph.edges(data=True):
		labels[(u,v)] = int(data['weight'])

	# Write file with nodes and degree,for reference
	print ('\n' + 'Writing node list with degree and neighbours...' + '\n')
	for i in nodeList:
		nodeDegree = enGraph.degree(i)
		neighboursList = list(nx.all_neighbors(enGraph, i))
		nodeListOP.write(str(i) + ',' + str(nodeDegree) + ',' + str(neighboursList) +'\n')
		print ("Node " + str(i) + " degree: " + str(nodeDegree))
		print ("Neighbours: " + str(neighboursList))

	nodeListOP.close()

	# Calculate new graph-wide total artists value
	# Use artist-total node attributes
	totalArtists = 0
	totalEdgeWeight = 0
	edgeList = enGraph.edges(data=True)

	for i in nodeList:
		nodeArtists = int(sortArtists[i])
		totalArtists += nodeArtists

	for i in edgeList:
		nodesStr = str(i).replace("u'","").replace("'","").replace("(","").replace(")","").replace(" ","")
		nodeU, nodeV, edgeData = nodesStr.split(",")
		edgeWeight = float(str(edgeData).replace("{weight:","").replace("}",""))
		totalEdgeWeight += edgeWeight

	# Analysis
	print ('\n' + 'Analysing undirected graph...' + '\n')
	try:
		print ('Average clustering coefficient...' + '\n')
		avClustering = nx.average_clustering(enGraph)
	except:
		pass
	print ('Connected components...' + '\n')
	connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
	print ('Find cliques...' + '\n')
	cl = nx.find_cliques(enGraph)
	cl = sorted(list(cl), key = len, reverse = True)
	print ('Number of cliques: ' + str(len(cl)) + '\n')
	cl_sizes = [len(c) for c in cl]
	print ('Size of cliques: ' + str(cl_sizes))

	print ('\n' + 'Undirected graph data: ' + '\n')
	print ('Nodes: ' + str(nodes))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Density: ' + str(density))
	print ('Average Clustering Coefficient: ' + str(avClustering))
	print ('Number of cliques: ' + str(len(cl)))
	print ('Connected Components: ' + str(connectComp))
	print
	print (str(nx.info(enGraph)))
	print

	runLog.write ('\n' + 'Undirected graph data: ' + '\n' + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')
	runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
	runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
	runLog.write ('Connected Components: ' + str(connectComp) + '\n')
	runLog.write ('\n' + str(nx.info(enGraph)) + '\n')

	# Write undirected gexf file for use in Gephi
	print ("Writing undirected gexf file... " + '\n')
	runLog.write('\n' + "Writing undirected gexf file... " + '\n')
	nx.write_gexf(enGraph, gexfFile)
	gexfFile.close()

	# Direct graph and write gexf of this
	print ("Directing graph... " + '\n')
	runLog.write('\n' + "Directing graph..." + '\n')
	diEnGraph = nx.DiGraph()
	diEnGraph.add_nodes_from(enGraph.nodes(data=True))
	diEnGraph.add_edges_from(enGraph.edges(data=True))

	edgeList = diEnGraph.edges(data=True)
	removedNodes = 0
	for i in edgeList:
		# clean up fraking unicode string
		nodesStr = str(i).replace("u'","").replace("'","").replace("(","").replace(")","").replace(" ","")

		# display / write a list of edges
		print(nodesStr)
		edgeListOP.write(nodesStr + '\n')

		# implement calculation for edge-direction
		nodeU, nodeV, edgeData = nodesStr.split(",")
		edgeWeight = float(str(edgeData).replace("{weight:","").replace("}",""))
		nodeUdate = int(sortDates[nodeU])
		print(nodeUdate)
		nodeVdate = int(sortDates[nodeV])
		print (nodeVdate)

		if nodeUdate > nodeVdate:
			# direct from v to u
			print("Directing edge from V to U" + '\n')
			# remove the edge
			diEnGraph.remove_edge(nodeU,nodeV)
			# add a directed edge
			diEnGraph.add_edge(nodeV, nodeU, weight=edgeWeight)

		elif nodeVdate > nodeUdate:
			# direct from u to v
			print("Direct from U to V" + '\n')
			# remove the edge
			diEnGraph.remove_edge(nodeU,nodeV)
			# add a directed edge
			diEnGraph.add_edge(nodeU, nodeV,  weight=edgeWeight)

		elif nodeUdate == nodeVdate:
			# remove the edge
			diEnGraph.remove_edge(nodeU,nodeV)
			# write to a list of removed edges
			removedNodes += 1
			print("Removed edge between nodes " + str(nodeU) + " and " + str(nodeV) + " due to identical node inception dates. " + '\n')
			edgeListOP.write("Removed edge between nodes " + str(nodeU) + " and " + str(nodeV) + " due to identical node inception dates. " + '\n')

	print (str(removedNodes) + " edges removed due to identical node inception dates. " + '\n')
	runLog.write ('\n' + str(removedNodes) + " edges removed due to identical node inception dates. " + '\n')
	edgeListOP.close()

	print ("Writing directed gexf file... " + '\n')
	runLog.write('\n' + "Writing directed gexf file... " + '\n')
	nx.write_gexf(diEnGraph, gexfDFile)
	gexfDFile.close()

	# Recheck zero degree nodes
	print ('Rechecking isolated (zero degree) nodes...' +'\n')
	runLog.write('\n' + 'Rechecking isolated (zero degree) nodes...' +'\n' + '\n')

	diNodeList = nx.nodes(diEnGraph)
	diNodeList.sort()

	isolateCount = 0
	if isolatedIP == 1:

		for i in diNodeList:
			if nx.is_isolate(diEnGraph,i):
				diEnGraph.remove_node(i)
				print ('Removed isolated node ' + str(i))
				runLog.write('Removed isolated node ' + str(i) + '\n')
				isolateCount += 1

		if isolateCount == 1:
			print ("Removed " + str(isolateCount) + " isolated node. " + '\n')
			runLog.write ('\n' + "Removed " + str(isolateCount) + " isolated node. " + '\n')

		if isolateCount > 1:
			print ("Removed " + str(isolateCount) + " isolated nodes. " + '\n')
			runLog.write ('\n' + "Removed " + str(isolateCount) + " isolated nodes. " + '\n')

	else:

		for i in diNodeList:
			if nx.is_isolate(diEnGraph,i):
				isolateCount += 1

		if isolateCount == 1:
			print (str(isolateCount) + ' isolated node intact.' +'\n')
			runLog.write('\n' + str(isolateCount) + ' isolated node intact.' + '\n')

		if isolateCount > 1:
			print (str(isolateCount) + ' isolated nodes intact.' + '\n')
			runLog.write('\n' + str(isolateCount) + ' isolated nodes intact.' + '\n')


	'''
	# Plot and display graph
	# Graph plotting parameters - moved to config file 'config_nw.txt'
	print ('Reading layout config file...' + '\n')

	# Open and read 'config_nw.txt'
	nwConfigPath = os.path.join ("config", 'config_nw.txt')
	nwConfig = open(nwConfigPath, 'r').readlines()

	# Remove the first line
	firstLine = nwConfig.pop(0)

	for line in nwConfig:
		n_size, n_alpha, node_colour, n_text_size, text_font, e_thickness, e_alpha, edge_colour, l_pos, e_text_size, edge_label_colour = line.split(",")
		
	node_size = int(n_size)
	node_alpha = float(n_alpha)
	node_text_size = int(n_text_size)
	edge_thickness = int(e_thickness)
	edge_alpha = float(e_alpha)
	label_pos = float(l_pos)
	edge_text_size = int(e_text_size)

	print ('Laying out graph...' + '\n')

	#nx.draw(enGraph)
	graph_pos = nx.spring_layout(diEnGraph)
	nx.draw_networkx_nodes(diEnGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
	nx.draw_networkx_edges(diEnGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
	#nx.draw_networkx_labels(diEnGraph, graph_pos, font_size = node_text_size, font_family = text_font)
	#nx.draw_networkx_edge_labels(diEnGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_color = edge_label_colour, font_size = edge_text_size, font_family = text_font)

	# write image file
	print ('Writing image file...' + '\n')
	plt.savefig(nwImg, format = 'eps', bbox_inches='tight')
	nwImg.close()

	# display graph
	#print ('Displaying graph...' + '\n')
	#plt.show()
	'''

	# Recalculate basic graph statistics
	nodes = nx.number_of_nodes(diEnGraph)
	edges = nx.number_of_edges(diEnGraph)
	density = nx.density(diEnGraph)
	isDag = nx.is_directed_acyclic_graph(diEnGraph)

	print ('Final Directed Graph Information' + '\n')
	print ('Omega Year: ' + omegaYear)
	print ('Nodes: ' + str(nodes))
	print ('Edges: ' + str(edges))
	print ('Density: ' + str(density))
	print ('Is DAG? ' + str(isDag))
	print
	print (str(nx.info(diEnGraph)))

	anFile.write ('Nodes: ' + str(nodes) + '\n')
	anFile.write ('Edges: ' + str(edges) + '\n')
	anFile.write ('Density: ' + str(density) + '\n')
	anFile.write ('Is DAG? ' + str(isDag) + '\n')
	anFile.write ('\n' + str(nx.info(diEnGraph)) + '\n')

	runLog.write ('\n' + 'Final Directed Graph Information' + '\n' + '\n')
	runLog.write ('Omega Year: ' + omegaYear + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')
	runLog.write ('Is DAG? ' + str(isDag) + '\n')
	runLog.write ('\n' + str(nx.info(diEnGraph)) + '\n')

	prFile.write(str(nx.pagerank(diEnGraph)))
	prFile.close()

	# Render undirected version of diEnGraph to facilitate final analysis of graph characteristics
	print('\n' + "Rendering undirected verison to facilitate final analysis of graph characteristics... ")
	runLog.write('\n' + "Rendering undirected verison to facilitate final analysis of graph characteristics... " + '\n')
	newEnGraph = diEnGraph.to_undirected()

	# Analysis
	print ('\n' + 'Analysing final undirected graph...' + '\n')
	print ('Maximal degree... ' + '\n')
	degreeSeq = sorted(nx.degree(newEnGraph).values(),reverse=True)
	maxDeg = max(degreeSeq)
	print ('Maximal degree: ' + str(maxDeg) + '\n')
	anFile.write ('Maximal degree: ' + str(maxDeg) + '\n')
	print ('Average clustering coefficient...' + '\n')
	avClustering = nx.average_clustering(newEnGraph)
	print ('Connected components...' + '\n')
	connectComp = [len(c) for c in sorted(nx.connected_components(newEnGraph), key=len, reverse=True)]
	print ('Find cliques...' + '\n')
	cl = nx.find_cliques(newEnGraph)
	cl = sorted(list(cl), key = len, reverse = True)
	print ('Number of cliques: ' + str(len(cl)) + '\n')
	anFile.write ('Number of cliques: ' + str(len(cl)) + '\n')
	cl_sizes = [len(c) for c in cl]
	print ('Size of cliques: ' + str(cl_sizes))
	anFile.write ('Size of cliques: ' + str(cl_sizes) + '\n' + '\n')


	# Write undirected gexf file for use in Gephi
	print ('\n' + 'Writing final undirected gexf file...' + '\n')
	nx.write_gexf(newEnGraph, gexfFinFile)
	gexfFinFile.close()

	anFile.write ('\n' + 'Final Undirected Graph Information' + '\n' + '\n')
	anFile.write ('Date of run: {}'.format(runDate) + '\n')
	anFile.write ('Omega Year: ' + omegaYear + '\n')
	anFile.write ("Total artists in all genres: " + str(totalArtists) + '\n')
	anFile.write ("Total edge-weighting: " + str(int(totalEdgeWeight)) + '\n')
	anFile.write ('Nodes: ' + str(nodes) + '\n')
	anFile.write ('Isolated nodes: ' + str(isolateCount) + '\n')
	anFile.write ('Edges: ' + str(edges) + '\n')
	anFile.write ('Density: ' + str(density) + '\n')
	anFile.write ('Maximal degree: ' + str(maxDeg) + '\n')
	anFile.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
	anFile.write ('Number of cliques: ' + str(len(cl)) + '\n')
	anFile.write ('Connected Components: ' + str(connectComp) + '\n')
	anFile.write ('\n' + str(nx.info(newEnGraph)))
	anFile.close()

	print ('Final Undirected Graph Information' + '\n')
	print ('Omega Year: ' + omegaYear)
	#print ("Total artists in all genres: " + str(totalArtists))
	#print ("Total edge-weighting: " + str(int(totalEdgeWeight)))
	print ('Nodes: ' + str(nodes))
	print ('Isolated nodes: ' + str(isolateCount))
	print ('Edges: ' + str(edges))
	print ('Self-loops: ' + str(selfLoopEdges))
	print ('Density: ' + str(density))
	print ('Maximal degree: ' + str(maxDeg))
	print ('Average Clustering Coefficient: ' + str(avClustering))
	print ('Number of cliques: ' + str(len(cl)))
	print ('Connected Components: ' + str(connectComp))
	print
	print (str(nx.info(newEnGraph)))
	print

	runLog.write ('\n' + 'Final Undirected Graph Information' + '\n' + '\n')
	runLog.write ('Omega Year: ' + omegaYear + '\n')
	#runLog.write ("Total artists in all genres: " + str(totalArtists) + '\n')
	#runLog.write ("Total edge-weighting: " + str(int(totalEdgeWeight)) + '\n')
	runLog.write ('Nodes: ' + str(nodes) + '\n')
	runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
	runLog.write ('Edges: ' + str(edges) + '\n')
	runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
	runLog.write ('Density: ' + str(density) + '\n')
	runLog.write ('Maximal degree: ' + str(maxDeg) + '\n')
	runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
	runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
	runLog.write ('Connected Components: ' + str(connectComp) + '\n' + '\n')
	runLog.write (str(nx.info(newEnGraph)) + '\n')

	# Clear Graph
	enGraph.clear()

# End timing of run
endTime = datetime.now()

print
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
runLog.write ('\n' + '\n' + 'Date of run: {}'.format(runDate) + '\n')
runLog.write('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()
