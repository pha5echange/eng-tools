# eng_network_single_b29.py
# Version b29
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# May 10th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Name changed to 'eng_network_single'

# Plots network graph from edgelist 'data\OMEGAYEAR_wuGraphData.txt'
# Adds dates from 'data\first_clusters.txt' as node attributes
# Adds artist numbers from 'data\OMEGAYEAR_artistNums.txt' as node attributes
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
# Added 'maxDeg' metric and 'isolated nodes' counter
# This version writes a list of nodes in the Largest Connected Component to 'ts_data' and a GEXF of the LCC

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

if not os.path.exists("gexf/lcc"):
	os.makedirs("gexf/lcc")

# Create 'results' subdirectories if necessary
if not os.path.exists("results"):
	os.makedirs("results")

if not os.path.exists("results/analysis"):
	os.makedirs("results/analysis")

# Create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# Open file for writing log
logPath = os.path.join("logs", 'eng_network_single_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "Single-Network Thing | Version " + versionNumber + " | Starting...")
runLog.write ("==========================================================================" + '\n' + '\n')
runLog.write ("Single-Network Thing | Version " + versionNumber + '\n' + '\n')

# Get user input
print
dateIP = int(input ("Enter an omega year for this graph (or 0 to leave the network intact): "))
omegaYear = str(dateIP)

# Uncomment the line below to facilitate optional self-loop removal
#selfLoopIP = int(input ("Enter 1 here to remove self-loop edges: "))
# Auto-remove self-loops - comment out the line below if self-loop removal is optional
selfLoopIP = 1

# Uncomment the line below to facilitate optional isolate removal
#isolatedIP = int(input ("Enter 1 here to remove isolated nodes: "))
# Do not remove isolated nodes - comment out the line below if isolate removal is optional
isolatedIP = 0

# Generate dictionary containing nodenames and dates (from 'data\first_cluster.txt')
dateInputPath = os.path.join("data", 'first_cluster.txt')
dateInput = open(dateInputPath, 'r')

dateDict = {}

for line in dateInput:
	genreInput, genreDate, newline = line.split(",")
	
	# Remove genres AFTER the Omega Year
	intGenreDate = int(genreDate)
	
	if intGenreDate <= dateIP:
		genreName = str(omegaYear + '_' + genreInput).replace(" ", "")
		dateDict[genreName] = genreDate

sortDates = OrderedDict(sorted(dateDict.items()))

# Generate dictionary containing nodenames and artist numbers (from 'data\OMEGAYEAR\_artistNums.txt')
artistInputPath = os.path.join("ts_data", omegaYear, omegaYear + '_artistNums.txt')
artistInput = open(artistInputPath, 'r').readlines()

firstLine = artistInput.pop(0)

artistDict = {}

for line in artistInput:
	genreInput, artistNum, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	artistDict[genreName] = artistNum

sortArtists = OrderedDict(sorted(artistDict.items()))

# Open file to write list of nodes
nodeListPath = os.path.join("ts_data", omegaYear, 'eng_network_' + versionNumber + '_' + omegaYear + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file for writing LCC nodes
lccPath = os.path.join("ts_data", omegaYear, 'eng_network_' + versionNumber + '_' + omegaYear + '_lcc.txt')
lccOP = open(lccPath, 'w')

# Open file to write list of edges
edgeListPath = os.path.join("ts_data", omegaYear, 'eng_network_' + versionNumber + '_' + omegaYear + '_edgeList.txt')
edgeListOP = open (edgeListPath, 'w') 

# Open file for writing initial gexf
gexfPath = os.path.join("gexf/initial", 'eng_network_' + versionNumber + '_' + omegaYear + '.gexf')
gexfFile = open(gexfPath, 'w')

# Open file for writing digraph gexf
gexfDPath = os.path.join("gexf/directed", omegaYear + '.gexf')
gexfDFile = open(gexfDPath, 'w')

# Open file for writing final gexf
gexfFinPath = os.path.join("gexf/final", 'eng_network_final_' + versionNumber + '_' + omegaYear + '.gexf')
gexfFinFile = open(gexfFinPath, 'w')

# OPen file for writing LCC gexf
gexfLccPath = os.path.join("gexf/lcc", 'eng_lcc_' + versionNumber + '_' + omegaYear + '.gexf')
gexfLccFile = open(gexfLccPath, 'w')

# Open file for Page Rank data
prPath = os.path.join("ts_data", omegaYear, omegaYear +'_pagerank.txt')
prFile = open(prPath, 'w')

# Open file for analysis results
anPath = os.path.join("results/analysis", 'eng_network_' + versionNumber + '_' + omegaYear + '_analysis.txt')
anFile = open(anPath, 'w')

# Open file to write image
nwImgPath = os.path.join("networks", 'eng_network_' + versionNumber + '_' + omegaYear + '_nw.eps')

anFile.write ('\n' + "==========================================================================" + '\n' + '\n')
anFile.write ("Single-Network Thing | Version " + versionNumber + '\n' + '\n')

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
selfLoopTotal = enGraph.number_of_selfloops()
#selfLoops = enGraph.selfloop_edges()
connections = edges - selfLoopTotal

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Number of self-loops: ' + str(selfLoopTotal))
#print ('Self-loop edges: ' + str(selfLoops))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print

runLog.write ('Initial data: ' + '\n' + '\n')
runLog.write ('User-entered date: ' + str(dateIP) + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
#runLog.write ('Self-loop edges: ' + str(selfLoops) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

# Apply artist numbers of nodes as attributes
print ('Applying total artist number attribute to nodes...' + '\n')
runLog.write ('\n' + 'Applying total artist number attribute to nodes...' + '\n')
nx.set_node_attributes (enGraph, 'totalArtists', sortArtists)
	
# Discard nodes without first-cluster dates
noDateNode = 0
print ('Checking genre inception dates, and removing if none...' + '\n')
for i in nodeList:
	if not i in sortDates.keys():
		enGraph.remove_node(i)
		print ('Removed node ' + str(i))
		noDateNode += 1

if noDateNode == 1:
	print ('\n' + 'Removed ' + str(noDateNode) + ' node due to no inception date.')
	runLog.write ('\n' + 'Removed ' + str(noDateNode) + ' node due to no inception date.' + '\n')

if noDateNode > 1:
	print ('\n' + 'Removed ' + str(noDateNode) + ' nodes due to no inception dates.')
	runLog.write ('\n' + 'Removed ' + str(noDateNode) + ' nodes due to no inception dates.' + '\n')

# Apply dates of nodes as attributes
print ('Applying inception date attribute to nodes...' + '\n')
runLog.write ('\n' + 'Applying inception date attribute to nodes...' + '\n')
nx.set_node_attributes (enGraph, 'incepDate', sortDates)

# Recalculate basic graph statistics
print ('\n' + 'Recalculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
nodeList.sort()
selfLoopTotal = enGraph.number_of_selfloops()
connections = edges - selfLoopTotal

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print

runLog.write ('\n' + 'Stage 1 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

# Remove nodes where 'incepDate' attribute is NEWER than user input ('dateIP')
if dateIP != 0:
	runLog.write('\n' + 'Removing nodes based upon user date input...' + '\n')
	for i in nodeList:
		incepDate = nx.get_node_attributes (enGraph, 'incepDate')
		intIncep = int(incepDate[i])
		if intIncep > dateIP:
			enGraph.remove_node(i)
			print ('Removed newer node ' + str(i) + ' based upon user date input.')
else:
	print ('No nodes removed based upon user date input.')
	runLog.write ('\n' + 'No nodes removed based upon user date input.' + '\n')

# Recalculate basic graph statistics
print ('\n' + 'Recalculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
nodeList.sort()
selfLoopTotal = enGraph.number_of_selfloops()
connections = edges - selfLoopTotal

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print

runLog.write ('\n' + 'Stage 2 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

# Remove self-loops
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

# Remove zero degree nodes
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
selfLoopTotal = enGraph.number_of_selfloops()

print ('Nodes: ' + str(nodes))
print ('Isolated nodes:' + str(isolateCount))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Density: ' + str(density))
print

runLog.write ('\n' + 'Stage 3 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
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
print ('Average clustering coefficient...' + '\n')
avClustering = nx.average_clustering(enGraph)
print ('Connected components...' + '\n')
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
print ('Find cliques...' + '\n')
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)
print ('Number of cliques: ' + str(len(cl)) + '\n')
cl_sizes = [len(c) for c in cl]
#print ('Size of cliques: ' + str(cl_sizes))

print ('\n' + 'Undirected graph data: ' + '\n')
print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
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
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
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
#print ('Writing image file...' + '\n')
plt.savefig(nwImgPath, format = 'eps', bbox_inches='tight')

# display graph
print ('Displaying graph...' + '\n')
plt.show()

# Clear plot
plt.clf()

# Recalculate basic graph statistics
nodes = nx.number_of_nodes(diEnGraph)
edges = nx.number_of_edges(diEnGraph)
nodeList = nx.nodes(diEnGraph)
nodeList.sort()
density = nx.density(diEnGraph)
isDag = nx.is_directed_acyclic_graph(diEnGraph)

# Count sources and sinks
sourceCount = 0
sinkCount = 0
for i in nodeList:
	outDeg = diEnGraph.out_degree(i)
	inDeg = diEnGraph.in_degree(i)
	if outDeg == 0 and inDeg >= 1: 
		sinkCount += 1

	elif inDeg == 0 and outDeg >= 1:
		sourceCount += 1

print ('Final Directed Graph Information' + '\n')
print ('User-entered date: ' + str(dateIP))
print ('Nodes: ' + str(nodes))
print ('Isolated nodes: ' + str(isolateCount))
print ('Source nodes: ' + str(sourceCount))
print ('Sink nodes: ' + str(sinkCount))
print ('Edges: ' + str(edges))
print ('Density: ' + str(density))
print ('Is DAG? ' + str(isDag))
print
print (str(nx.info(diEnGraph)))

anFile.write ('Nodes: ' + str(nodes) + '\n')
anFile.write ('Isolated nodes: ' + str(isolateCount) + '\n')
anFile.write ('Source nodes: ' + str(sourceCount) + '\n')
anFile.write ('Sink nodes: ' + str(sinkCount) + '\n')
anFile.write ('Edges: ' + str(edges) + '\n')
anFile.write ('Density: ' + str(density) + '\n')
anFile.write ('Is DAG? ' + str(isDag) + '\n')
anFile.write ('\n' + str(nx.info(diEnGraph)) + '\n')

runLog.write ('\n' + 'Final Directed Graph Information' + '\n' + '\n')
runLog.write ('User-entered date: ' + str(dateIP) + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
runLog.write ('Source nodes: ' + str(sourceCount) + '\n')
runLog.write ('Sink nodes: ' + str(sinkCount) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Is DAG? ' + str(isDag) + '\n')
runLog.write ('\n' + str(nx.info(diEnGraph)) + '\n')

prFile.write(str(nx.pagerank(diEnGraph)))
prFile.close()

# Render undirected version of diEnGraph to facilitate final analysis of graph characteristics
print('\n' + "Rendering undirected version to facilitate final analysis of graph characteristics... ")
runLog.write('\n' + "Rendering undirected version to facilitate final analysis of graph characteristics... " + '\n')
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
#print ('Size of cliques: ' + str(cl_sizes))
anFile.write ('Size of cliques: ' + str(cl_sizes) + '\n' + '\n')

# Find LCC nodes, print to screen and and write to file
largeCC = max(nx.connected_components(newEnGraph), key=len)
print
print ("Nodes in LCC: ")
print
print (largeCC)
lccOP.write(str(largeCC))
lccOP.write('\n' + '\n' + "There are " + str(len(largeCC)) + " nodes in the LCC of this graph." + '\n')
lccOP.close()
print
print ("There are " + str(len(largeCC)) + " nodes in the LCC of this graph.")
print

# Render GEXF file of LCC
print
print ("Writing gexf file of LCC... " + '\n')
runLog.write('\n' + "Writing gexf file of LCC... " + '\n')
lccSub = max(nx.connected_component_subgraphs(newEnGraph), key=len)
nx.write_gexf(lccSub, gexfLccFile)
gexfLccFile.close()

# Analysis of LCC
print ('\n' + 'Analysing LCC...' + '\n')
lccNodes = nx.number_of_nodes(lccSub)
lccEdges = nx.number_of_edges(lccSub)
lccDegreeSeq = sorted(nx.degree(lccSub).values(),reverse=True)
lccMaxDeg = max(lccDegreeSeq)
lccDensity = nx.density(lccSub)
lccAvClustering = nx.average_clustering(lccSub)
lccCl = nx.find_cliques(lccSub)
lccCl = sorted(list(lccCl), key = len, reverse = True)
lccCl_sizes = [len(c) for c in lccCl]

print ('LCC Nodes: ' + str(lccNodes))
anFile.write('LCC Nodes: ' + str(lccNodes) + '\n')
print ('LCC Edges: ' + str(lccEdges))
anFile.write('LCC Edges: ' + str(lccEdges) + '\n')
print ('LCC Density: ' + str(lccDensity))
anFile.write('LCC Density: ' + str(lccDensity) + '\n')
print ('Maximal degree of LCC: ' + str(lccMaxDeg) + '\n')
anFile.write ('Maximal degree of LCC: ' + str(lccMaxDeg) + '\n')
print ('ACC of LCC: ' + str(lccAvClustering))
anFile.write('ACC of LCC: ' + str(lccAvClustering) + '\n')
print ('Number of cliques in LCC: ' + str(len(lccCl)) + '\n')
anFile.write ('Number of cliques in LCC: ' + str(len(lccCl)) + '\n' + '\n')
print ('Size of LCC cliques: ' + str(lccCl_sizes))
anFile.write ('Size of LCC cliques: ' + str(lccCl_sizes) + '\n')
print

# Write undirected gexf file for use in Gephi
print ('\n' + 'Writing final undirected gexf file...' + '\n')
nx.write_gexf(newEnGraph, gexfFinFile)
gexfFinFile.close()

# End timing of run
endTime = datetime.now()

anFile.write ('\n' + 'Final Undirected Graph Information' + '\n' + '\n')
anFile.write ('Date of run: {}'.format(runDate) + '\n')
anFile.write ('Omega Year: ' + omegaYear + '\n')
#anFile.write ("Total artists in all genres: " + str(totalArtists) + '\n')
#anFile.write ("Total edge-weighting: " + str(int(totalEdgeWeight)) + '\n')
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
print ('User-entered date: ' + str(dateIP))
print ('Omega Year: ' + omegaYear)
#print ("Total artists in all genres: " + str(totalArtists))
#print ("Total edge-weighting: " + str(int(totalEdgeWeight)))
print ('Nodes: ' + str(nodes))
print ('Isolated nodes: ' + str(isolateCount))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopTotal))
print ('Density: ' + str(density))
print ('Maximal degree: ' + str(maxDeg))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Number of cliques: ' + str(len(cl)))
print ('Connected Components: ' + str(connectComp))
print
print (str(nx.info(newEnGraph)))
print
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))

runLog.write ('\n' + 'Final Undirected Graph Information' + '\n' + '\n')
runLog.write ('Omega Year: ' + omegaYear + '\n')
#runLog.write ("Total artists in all genres: " + str(totalArtists) + '\n')
#runLog.write ("Total edge-weighting: " + str(int(totalEdgeWeight)) + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Isolated nodes:' + str(isolateCount) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopTotal) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Maximal degree: ' + str(maxDeg) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n' + '\n')
runLog.write (str(nx.info(newEnGraph)))
runLog.write ('\n' + '\n' + 'Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.close()