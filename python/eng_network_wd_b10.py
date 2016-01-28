# eng_network_wd_b10.py
# Version b10
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 28th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'data\wuGraphData.txt'
# Adds dates from 'data\first_clusters.txt' as node attributes
# Adds artist numbers from 'data\eng_artistNums.txt' as node attributes
# Removes nodes where date-cluster information is not available
# Removes self-loop edges and zero-degree nodes if required
# Removes nodes based upon 'incepDate' if required - a date is requested and all nodes NEWER than this are removed
# Displays using parameters from 'config_nw.txt'
# Writes 'results\eng_network_wd_nodeList.txt' with nodes and degrees (k)
# Writes analysis file to 'results\'
# Writes Laplacian Spectrum results to 'results\'
# Writes image to 'networks\'

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

versionNumber = ("b10")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("data"):
	os.makedirs("data")

# Create 'gexf' subdirectory if necessary
if not os.path.exists("gexf"):
	os.makedirs("gexf")

# Create 'results' subdirectory if necessary
if not os.path.exists("results"):
	os.makedirs("results")

# Create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# Open file for writing log
logPath = os.path.join("logs", 'eng_network_wd_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + 'Weighted Directed Network Thing | Version ' + versionNumber + ' | Starting...')

# Get user input
print
dateIP = int(input ("Enter a year to remove nodes that appear AFTER this date (or 0 to leave the network intact): "))
selfLoopIP = int(input ("Enter 1 here to remove self-loop edges: "))
isolatedIP = int(input ("Enter 1 here to remove isolated nodes: "))

# Open file to write list of nodes
nodeListPath = os.path.join("data", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file to write list of edges
edgeListPath = os.path.join("data", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '_edgeList.txt')
edgeListOP = open (edgeListPath, 'w') 

# Open file for writing gexf
gexfPath = os.path.join("gexf", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '.gexf')
gexfFile = open(gexfPath, 'w')

# Open file for writing digraph gexf
gexfDPath = os.path.join("gexf", 'eng_network_digraph_wd_' + versionNumber + '_' + str(dateIP) + '.gexf')
gexfDFile = open(gexfDPath, 'w')

# Open file for analysis results
anPath = os.path.join("results", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '_analysis.txt')
anFile = open(anPath, 'w')

# Open file to write Laplacian Spectrum Numpy array
lsPath = os.path.join("data", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '_laplacian.txt')
lsFile = open(lsPath, 'w')

# Open file to write image
# nwImgPath = os.path.join("networks", 'eng_network_wd_' + versionNumber + '_' + str(dateIP) + '_nw.png')
# nwImg = open (nwImgPath, 'w')

runLog.write ('Weighted Directed Network Thing | Version ' + versionNumber + '\n' + '\n')
anFile.write ('Weighted Directed Network Thing | Version ' + versionNumber + '\n' + '\n')

# Read the edgelist and generate undirected graph
print ('\n' + 'Importing Weighted Edge List...')
inputPath = os.path.join("data", 'wuGraph_data.txt')
edgeList = open (inputPath, 'r')
enGraph = nx.read_weighted_edgelist(edgeList, delimiter=',')
edgeList.close()

# Calculate basic graph statistics
print ('\n' + 'Calculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
nodeList.sort()
selfLoopEdges = enGraph.number_of_selfloops()
connections = edges - selfLoopEdges
avClustering = nx.average_clustering(enGraph)
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopEdges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Number of cliques: ' + str(len(cl)))
print ('Connected Components: ' + str(connectComp) + '\n')
print
print (str(nx.info(enGraph)))
print

runLog.write ('Initial data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')

# Generate dictionary containing nodenames and artist numbers (from 'data\eng_artistNums.txt')
artistInputPath = os.path.join("data", 'eng_artistNums.txt')
artistInput = open(artistInputPath, 'r')

artistDict = {}

for line in artistInput:
	genreInput, artistNum, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	artistDict[genreName] = artistNum

sortArtists = OrderedDict(sorted(artistDict.items()))
anFile.write('Sorted artist numbers: ' + str(sortArtists) + '\n' + '\n')

# Apply artist numbers of nodes as attributes
print ('Applying total artist number attribute to nodes...' + '\n')
nx.set_node_attributes (enGraph, 'totalArtists', sortArtists)

# Generate dictionary containing nodenames and dates (from 'data\first_cluster.txt')
dateInputPath = os.path.join("data", 'first_cluster.txt')
dateInput = open(dateInputPath, 'r')

dateDict = {}

for line in dateInput:
	genreInput, genreDate, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	dateDict[genreName] = genreDate

sortDates = OrderedDict(sorted(dateDict.items()))
anFile.write('Sorted genre dates: ' + str(sortDates) + '\n' + '\n')

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

# Recalculate basic graph statistics
print ('\n' + 'Recalculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
nodeList.sort()
selfLoopEdges = enGraph.number_of_selfloops()
connections = edges - selfLoopEdges
avClustering = nx.average_clustering(enGraph)
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopEdges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Number of cliques: ' + str(len(cl)))
print ('Connected Components: ' + str(connectComp))
print
print (str(nx.info(enGraph)))
print

runLog.write ('\n' + 'Stage 1 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')

# Apply dates of nodes as attributes
print ('\n' + 'Applying inception date attribute to nodes...' + '\n')
runLog.write ('\n' + 'Applying inception date attribute to nodes...' + '\n')
nx.set_node_attributes (enGraph, 'incepDate', sortDates)

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
selfLoopEdges = enGraph.number_of_selfloops()
connections = edges - selfLoopEdges
avClustering = nx.average_clustering(enGraph)
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Self-loops: ' + str(selfLoopEdges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Number of cliques: ' + str(len(cl)))
print ('Connected Components: ' + str(connectComp))
print
print (str(nx.info(enGraph)))
print

runLog.write ('\n' + 'Stage 2 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')

# Remove self-loops
if selfLoopIP == 1:
	print ('\n' + 'Checking for and removing self-loops...' + '\n')
	runLog.write('\n' + 'Checking for and removing self-loops...' + '\n')
	for u,v,data in enGraph.edges(data=True):
		if u == v:
			enGraph.remove_edge(u,v)
			print ('removed self-loop ' + str(u))
else:
	print ('Self-loops intact.' + '\n')
	runLog.write('\n' + 'Self-loops intact.' + '\n')

# Recalculate basic graph statistics
print ('\n' + 'Recalculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
nodeList.sort()
selfLoopEdges = enGraph.number_of_selfloops()
avClustering = nx.average_clustering(enGraph)
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)

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

runLog.write ('\n' + 'Stage 3 data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Self-loops: ' + str(selfLoopEdges) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Number of cliques: ' + str(len(cl)) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')

# Remove zero degree nodes
if isolatedIP == 1:
	print ('\n' + 'Checking for and removing isolated (zero degree) nodes...' +'\n')
	runLog.write('\n' + 'Checking for and removing isolated (zero degree) nodes...' +'\n')
	for i in nodeList:
		if nx.is_isolate(enGraph,i):
			enGraph.remove_node(i)
			print ('Removed isolated node ' + str(i))
			runLog.write('Removed isolated node ' + str(i) + '\n')
else:
	print ('Isolated nodes intact.')
	runLog.write('\n' + 'Isolated nodes intact.' + '\n')

# Clean edge-labels
print ('\n' + 'Cleaning edge labels...')
labels = {}
for u,v,data in enGraph.edges(data=True):
	labels[(u,v)] = int(data['weight'])

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list with degree and neighbours...')
for i in nodeList:
	nodeDegree = enGraph.degree(i)
	neighboursList = list(nx.all_neighbors(enGraph, i))
	nodeListOP.write(str(i) + ',' + str(nodeDegree) + ',' + str(neighboursList) +'\n')
	print ("Node " + str(i) + " degree: " + str(nodeDegree))
	print ("Neighbours: " + str(neighboursList))

nodeListOP.close()

# Analysis
print ('\n' + 'Analysing final undirected graph...' + '\n')
print ('Average clustering coefficient...' + '\n')
avClustering = nx.average_clustering(enGraph)
print ('Laplacian spectrum...' + '\n')
eigenArray = nx.laplacian_spectrum(enGraph)
print ('Connected components...' + '\n')
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
print ('Find cliques...' + '\n')
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)
print ('Number of cliques: ' + str(len(cl)) + '\n')
cl_sizes = [len(c) for c in cl]
print ('Size of cliques: ' + str(cl_sizes))

# Write undirected gexf file for use in Gephi
print ('\n' + 'Writing undirected gexf file...' + '\n')
nx.write_gexf(enGraph, gexfFile)
gexfFile.close()

np.savetxt (lsFile, eigenArray)
lsFile.close()

# Write directed graph and then gexf of this
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
		print("Removed edge between nodes " + str(nodeU) + " and " + str(nodeV) + " due to identical node inception dates. ")
		edgeListOP.write("Removed edge between nodes " + str(nodeU) + " and " + str(nodeV) + " due to identical node inception dates. " + '\n')

print (str(removedNodes) + " edges removed due to identical node inception dates. " + '\n')

# print ('\n' + 'Writing directed gexf file...' + '\n')
nx.write_gexf(diEnGraph, gexfDFile)
gexfDFile.close()

edgeListOP.close()

'''
# Plot and display graph
# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('Reading layout config file...' + '\n')

# Open and read 'config_nw.txt'
nwConfig = open('config_nw.txt').readlines()

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
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)
nx.draw_networkx_edge_labels(enGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_color = edge_label_colour, font_size = edge_text_size, font_family = text_font)

# write image file
print ('Writing image file...' + '\n')
plt.savefig(nwImg, format = 'png')
nwImg.close()

# display graph
print ('Displaying graph...' + '\n')
plt.show()
''' 

# Recalculate basic graph statistics
nodes = nx.number_of_nodes(diEnGraph)
edges = nx.number_of_edges(diEnGraph)
density = nx.density(diEnGraph)

# Memory use
memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576

# End timing of run
endTime = datetime.now()

print ('\n' + 'Final Run Information' + '\n')
print ('User-entered date: ' + str(dateIP))
print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Density: ' + str(density))
print
print (str(nx.info(diEnGraph)))
print
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Memory Used: ' + str(memUseMb) + 'Mb')


runLog.write ('\n' + 'Final Run Information' + '\n' + '\n')
runLog.write ('User-entered date: ' + str(dateIP) + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('\n' + 'Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Memory Used: ' + str(memUseMb) + 'Mb')
runLog.close()

anFile.write ('\n' + 'Date of run: {}'.format(runDate) + '\n')
anFile.write ('Nodes: ' + str(nodes) + '\n')
anFile.write ('Edges: ' + str(edges) + '\n')
anFile.write ('Density: ' + str(density) + '\n')
anFile.close()
