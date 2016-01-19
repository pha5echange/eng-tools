# eng_network_wd_b07.py
# Version b07
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# January 14th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'data\wuGraphData.txt'
# Adds dates from 'data\first_clusters.txt' as node attributes
# Adds artist numbers from 'data\eng_artistNums.txt' as node attributes
# Removes nodes where date-cluster information is not available
# Removes self-loop edges and zero-degree nodes if required
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

versionNumber = ("b07")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# Create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

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

# Open file for writing gexf
gexfPath = os.path.join("gexf", 'eng_network_wd_' + versionNumber + '.gexf')
gexfFile = open(gexfPath, 'w')

# Open file for writing digraph gexf
gexfDPath = os.path.join("gexf", 'eng_network_digraph_wd_' + versionNumber + '.gexf')
gexfDFile = open(gexfDPath, 'w')

# Open file to write list of nodes
nodeListPath = os.path.join("results", 'eng_network_wd_' + versionNumber + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file for analysis results
anPath = os.path.join("results", 'eng_network_wd_' + versionNumber + '_analysis.txt')
anFile = open(anPath, 'w')

# Open file to write Laplacian Spectrum Numpy array
lsPath = os.path.join("results", 'eng_network_wd_' + versionNumber + '_laplacian.txt')
lsFile = open(lsPath, 'w')

# Open file to write image
nwImgPath = os.path.join("networks", 'eng_network_wd_' + versionNumber + '_' + str(startTime) + '_nw.png')
nwImg = open (nwImgPath, 'w')

# Begin
print ('\n' + 'Weighted Directed Network Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Weighted Directed Network Thing | Version ' + versionNumber + '\n' + '\n')
anFile.write ('Weighted Directed Network Thing | Version ' + versionNumber + '\n' + '\n')

# Get user input
print
selfLoopIP = int(input ("Enter 0 here to remove self-loop edges: "))
isolatedIP = int(input ("Enter 0 here to remove isolated nodes: "))

# Read the edgelist
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

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density) + '\n')

runLog.write ('Initial data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

# Generate dictionary containing nodenames and artist numbers (from 'data\eng_artistNums.txt')
artistInputPath = os.path.join("data", 'eng_artistNums.txt')
artistInput = open(artistInputPath, 'r')

artistDict = {}

for line in artistInput:
	genreInput, artistNum, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	artistDict[genreName] = artistNum

sortArtists = OrderedDict(sorted(artistDict.items()))
print sortArtists
anFile.write('Sorted artist numbers: ' + str(sortArtists) + '\n' + '\n')

# Apply artist numbers of nodes as attributes
print ('\n' + 'Applying artist number attribute to nodes...')
nx.set_node_attributes (enGraph, 'artists', sortArtists)

# Generate dictionary containing nodenames and dates (from 'data\first_cluster.txt')
dateInputPath = os.path.join("data", 'first_cluster.txt')
dateInput = open(dateInputPath, 'r')

dateDict = {}

for line in dateInput:
	genreInput, genreDate, newline = line.split(",")
	genreName = str(genreInput).replace(" ", "")
	dateDict[genreName] = genreDate

sortDates = OrderedDict(sorted(dateDict.items()))
print sortDates
anFile.write('Sorted genre dates: ' + str(sortDates) + '\n' + '\n')

# Discard nodes without first-cluster dates
noDateNode = 0
print ('\n' + 'Checking for nodes with dates...' + '\n')
for i in nodeList:
	if not i in sortDates.keys():
		enGraph.remove_node(i)
		print ('Removed node ' + str(i))
		noDateNode += 1

if noDateNode == 1:
	print ('\n' + 'Removed ' + str(noDateNode) + ' node.')

if noDateNode > 1:
	print ('\n' + 'Removed ' + str(noDateNode) + ' nodes.')

# Apply dates of nodes as attributes
print ('\n' + 'Applying date attribute to nodes...')
nx.set_node_attributes (enGraph, 'Date', sortDates)

# Remove zero degree nodes
if isolatedIP == 0:
	print ('\n' + 'Removing isolated nodes...' +'\n')
	runLog.write ('Isolated nodes removed:' +'\n' + '\n')
	for i in nodeList:
		if nx.is_isolate(enGraph,i):
			enGraph.remove_node(i)
			print ('removed node ' + str(i))
			runLog.write('Removed node ' + str(i) +'\n')
else:
	print ('\n' + 'Isolated nodes intact.')
	runLog.write('\n' + 'Isolated nodes intact.' + '\n')

# Remove self-loops
if selfLoopIP == 0:
	print ('\n' + 'Removing self-loops...' + '\n')
	runLog.write('\n' + 'Removing self-loops...' + '\n')
	for u,v,data in enGraph.edges(data=True):
		if u == v:
			enGraph.remove_edge(u,v)
			print ('removed self-loop ' + str(u))
else:
	print ('\n' + 'Self-loops intact.')
	runLog.write('\n' + 'Self-loops intact.' + '\n')

# Clean edge-labels
print ('\n' + 'Cleaning edge labels...')
labels = {}
for u,v,data in enGraph.edges(data=True):
	labels[(u,v)] = int(data ['weight'])

# Recalculate basic graph statistics
print ('\n' + 'Recalculating various things...' + '\n')
newNodes = nx.number_of_nodes(enGraph)
newNodeList = nx.nodes(enGraph)
newNodeList.sort()
newEdges = nx.number_of_edges(enGraph)
newDensity = nx.density(enGraph)

print ('Nodes: ' + str(newNodes))
print ('Edges: ' + str(newEdges))
print ('Density: ' + str(newDensity))

runLog.write ('\n' + 'Intermediate data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(newNodes) + '\n')
runLog.write ('Edges: ' + str(newEdges) + '\n')
runLog.write ('Density: ' + str(newDensity) + '\n')

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list (with degree k)...')
for i in newNodeList:
	nodeDegree = enGraph.degree(i)
	nodeListOP.write(str(i) + ',' + str(nodeDegree) + '\n')

nodeListOP.close()

# Write gexf file for use in Gephi
print ('\n' + 'Writing gexf file...')
nx.write_gexf(enGraph, gexfFile)
gexfFile.close()

# NetworkX analysis algorithms
print ('\n' + 'Analysing graph...')
print ('Average clustering coefficient...')
avClustering = nx.average_clustering(enGraph)
print ('Laplacian spectrum...')
eigenArray = nx.laplacian_spectrum(enGraph)
print ('Connected components...')
connectComp = [len(c) for c in sorted(nx.connected_components(enGraph), key=len, reverse=True)]
print ('Find cliques...')
cl = nx.find_cliques(enGraph)
cl = sorted(list(cl), key = len, reverse = True)
print ('Number of cliques: ' + str(len(cl)))
cl_sizes = [len(c) for c in cl]
print ('Size of cliques: ' + str(cl_sizes) + '\n')

'''
print ('Clique removal...')
cliqueRemoval = clique.clique_removal(enGraph)
print ('Node connectivity...')
nodeConnect = nx.node_connectivity(enGraph)
print ('Average node connectivity...')
avNodeConnect = nx.average_node_connectivity(enGraph)
print ('Edge connectivity...')
edgeConnect = nx.edge_connectivity(enGraph)

# Various shortest paths, just to see...
rockToRapShortPath = nx.shortest_path(enGraph,source='rock',target='rap')
rockToJazzShortPath = nx.shortest_path(enGraph,source='rock',target='jazz')
rapToJazzShortPath = nx.shortest_path(enGraph,source='rap',target='jazz')
rockToClassicalShortPath = nx.shortest_path(enGraph,source='rock',target='classical')
rapToClassicalShortPath = nx.shortest_path(enGraph,source='rap',target='classical')
jazzToClassicalShortPath = nx.shortest_path(enGraph,source='jazz',target='classical')
'''

# Write directed graph gexf
diEnGraph = nx.DiGraph()
diEnGraph.add_nodes_from(enGraph)
diEnGraph.add_edges_from(enGraph.edges())
nx.write_gexf(diEnGraph, gexfDFile)
gexfDFile.close()

# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('\n' + 'Reading layout config file...')

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

print ('\n' + 'Laying out graph...' + '\n')
#nx.draw(enGraph)
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)
nx.draw_networkx_edge_labels(enGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_color = edge_label_colour, font_size = edge_text_size, font_family = text_font)

# write image file and display graph
'''
print ('\n' + 'Writing image file...')
plt.savefig(nwImg, format = 'png')
nwImg.close()

print ('\n' + 'Displaying graph...')
plt.show()
''' 

# Memory use
memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576

# End timing of run
endTime = datetime.now()

runLog.write ('\n' + 'Final Run Information' + '\n' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Memory Used: ' + str(memUseMb) + 'Mb' + '\n' + '\n')
runLog.close()

anFile.write ('Date of run: {}'.format(runDate) + '\n')
anFile.write ('Nodes: ' + str(newNodes) + '\n')
anFile.write ('Edges: ' + str(newEdges) + '\n')
anFile.write ('Density: ' + str(newDensity) + '\n')
anFile.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
anFile.write ('Connected Components: ' + str(connectComp) + '\n')
anFile.write ('Number of cliques: ' + str(len(cl)) + '\n')

'''
anFile.write ('Size of cliques: ' + str(cl_sizes) + '\n')
anFile.write ('Clique List: ' + str(cl) + '\n')
anFile.write ('Clique Removal: ' + str(cliqueRemoval) + '\n' + '\n')
anFile.write ('Node Connectivity (if 0, graph is disconnected): ' + str(nodeConnect) + '\n')
anFile.write ('Average Node Connectivity: ' + str(avNodeConnect) + '\n')
anFile.write ('Edge Connectivity: ' + str(edgeConnect) + '\n')
anFile.write ('\n' + 'Shortest Path - Rock to Rap: ' + str(rockToRapShortPath) + '\n')
anFile.write ('Shortest Path - Rock to Jazz: ' + str(rockToJazzShortPath) + '\n')
anFile.write ('Shortest Path - Rap to Jazz: ' + str(rapToJazzShortPath) + '\n')
anFile.write ('Shortest Path - Rock to Classical: ' + str(rockToClassicalShortPath) + '\n')
anFile.write ('Shortest Path - Rap to Classical: ' + str(rapToClassicalShortPath) + '\n')
anFile.write ('Shortest Path - Jazz to Classical: ' + str(jazzToClassicalShortPath) + '\n')
'''
anFile.close()

np.savetxt (lsFile, eigenArray)
lsFile.close()

print ('\n' + 'Final Run Information' + '\n')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Memory Used: ' + str(memUseMb) + 'Mb')
print ('Nodes: ' + str(newNodes))
print ('Edges: ' + str(newEdges))
print ('Density: ' + str(newDensity))
print ('Average Clustering Coefficient: ' + str(avClustering))

'''
print ('Laplacian Spectrum: ')
print (eigenArray)
print
print ('Connected Components: ' + str(connectComp))
print ('Number of cliques: ' + str(len(cl)))
print ('Size of cliques: ' + str(cl_sizes))
print ('Clique List: ' + str(cl) + '\n')
print ('Clique Removal: ' + str(cliqueRemoval) + '\n')
print ('Node Connectivity (if 0, graph is disconnected): ' + str(nodeConnect))
print ('Average Node Connectivity: ' + str(avNodeConnect))
print ('Edge Connectivity: ' + str(edgeConnect))
print
print ('Shortest Path - Rock to Rap: ' + str(rockToRapShortPath))
print ('Shortest Path - Rock to Jazz: ' + str(rockToJazzShortPath))
print ('Shortest Path - Rap to Jazz: ' + str(rapToJazzShortPath))
print ('Shortest Path - Rock to Classical: ' + str(rockToClassicalShortPath))
print ('Shortest Path - Rap to Classical: ' + str(rapToClassicalShortPath))
print ('Shortest Path - Jazz to Classical: ' + str(jazzToClassicalShortPath) + '\n')
'''
