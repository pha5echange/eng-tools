# eng_network_a09.py
# Version a09
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# November 6th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'uuGraphData.txt'
# Displays using parameters from 'config_nw.txt'
# writes 'nodeList.txt' with nodes and degrees (k) for each
# Writes 'weighted_nodeList.txt' with nodes and degrees (k) for each
# Writes eps image to '\networks\'
# Removes self-loop edges

# Run AFTER 'eng_nodesets.py'

# import packages
import os
import resource
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

versionNumber = ("a09")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_network_log.txt')
runLog = open(logPath, 'a')

# Open file to write list of nodes
nodeListPath = os.path.join("data", versionNumber + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file to write image
nwImgPath = os.path.join("networks", versionNumber + '_' + str(startTime) + '_uuNw.eps')
nwImg = open (nwImgPath, 'w')

# Begin
print ('\n' + 'Graph Drawing Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Graph Drawing Thing | Version ' + versionNumber + '\n' + '\n')

# Read the edgelist
print ('\n' + 'Importing Edge List...')
inputPath = os.path.join("data", 'uuGraph_data.txt')
edgeList = open (inputPath, 'r')
enGraph = nx.read_edgelist(edgeList, delimiter=',')
edgeList.close()

print ('\n' + 'Calculating various things...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)
nodeList = nx.nodes(enGraph)
selfLoopEdges = enGraph.number_of_selfloops()
connections = edges - selfLoopEdges

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))

runLog.write ('\n' + 'Initial data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

# Remove self-loops
print ('\n' + 'Removing self-loops...')
for u,v in enGraph.edges():
	if u == v:
		enGraph.remove_edge(u,v)

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list...')
for i in nodeList:
	nodeDegree = enGraph.degree(i)
	nodeListOP.write(str(i) + ',' + str(nodeDegree) + '\n')

nodeListOP.close()

# remove zero degree nodes
#print ('\n' + 'Removing isolated nodes...' +'\n')
#runLog.write ('\n' + 'Isolated nodes removed:' +'\n' + '\n')
#for i in nodeList:
#	if nx.is_isolate(enGraph,i):
#		enGraph.remove_node(i)
#		print ('removed node ' + str(i))
#		runLog.write('Removed node ' + str(i) +'\n')

print ('\n' + 'Recalculating various things...' + '\n')
newNodes = nx.number_of_nodes(enGraph)
newEdges = nx.number_of_edges(enGraph)
newDensity = nx.density(enGraph)

print ('Nodes: ' + str(newNodes))
print ('Edges: ' + str(newEdges))
print ('Density: ' + str(newDensity))

runLog.write ('\n' + 'Intermediate data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(newNodes) + '\n')
runLog.write ('Edges: ' + str(newEdges) + '\n')
runLog.write ('Density: ' + str(newDensity) + '\n')

# NetworkX analysis algorithms
print ('\n' + 'Analysing graph...')
nodeConnect = nx.node_connectivity(enGraph)
avClustering = nx.average_clustering(enGraph)
eigenArray = nx.laplacian_spectrum(enGraph)

# various shortest paths, just to see...
rockToRapShortPath = nx.shortest_path(enGraph,source='rock',target='rap')
rockToJazzShortPath = nx.shortest_path(enGraph,source='rock',target='jazz')
rapToJazzShortPath = nx.shortest_path(enGraph,source='rap',target='jazz')
rockToClassicalShortPath = nx.shortest_path(enGraph,source='rock',target='classical')
rapToClassicalShortPath = nx.shortest_path(enGraph,source='rap',target='classical')
jazzToClassicalShortPath = nx.shortest_path(enGraph,source='jazz',target='classical')

# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('\n' + 'Reading layout config. file...')

# open and read 'config_nw.txt'
nwConfig = open('config_nw.txt').readlines()

# remove the first line
firstLine = nwConfig.pop(0)

for line in nwConfig:
	n_size, n_alpha, node_colour, n_text_size, text_font, e_thickness, e_alpha, edge_colour, l_pos, e_text_size, edge_label_colour = line.split(",")
	
node_size = int(n_size)
node_alpha = float(n_alpha)
node_text_size = int(n_text_size)
edge_thickness = int(e_thickness)
edge_alpha = float(e_alpha)
label_pos = float(l_pos)

print ('\n' + 'Laying out graph...' + '\n')
# nx.draw(enGraph)
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)

print ('\n' + 'Writing image file...')
plt.savefig(nwImg, format = 'eps')

print ('\n' + 'Displaying graph...')
plt.show()

# End timing of run
endTime = datetime.now()

memUseMb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1048576

runLog.write ('\n' + 'Final Run Information' + '\n' + '\n')
runLog.write ('Date of run: {}'.format(runDate) + '\n')
runLog.write ('Duration of run : {}'.format(endTime - startTime) + '\n')
runLog.write ('Memory Used: ' + str(memUseMb) + 'Mb' + '\n' + '\n')
runLog.write ('Nodes: ' + str(newNodes) + '\n')
runLog.write ('Edges: ' + str(newEdges) + '\n')
runLog.write ('Density: ' + str(newDensity) + '\n')
runLog.write ('Node Connectivity (if 0, graph is disconnected): ' + str(nodeConnect) + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('\n' + 'Shortest Path - Rock to Rap: ' + str(rockToRapShortPath) + '\n')
runLog.write ('Shortest Path - Rock to Jazz: ' + str(rockToJazzShortPath) + '\n')
runLog.write ('Shortest Path - Rap to Jazz: ' + str(rapToJazzShortPath) + '\n')
runLog.write ('Shortest Path - Rock to Classical: ' + str(rockToClassicalShortPath) + '\n')
runLog.write ('Shortest Path - Rap to Classical: ' + str(rapToClassicalShortPath) + '\n')
runLog.write ('Shortest Path - Jazz to Classical: ' + str(jazzToClassicalShortPath) + '\n')

print ('\n' + 'Final Run Information' + '\n')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Memory Used: ' + str(memUseMb) + 'Mb')
print ('Nodes: ' + str(newNodes))
print ('Edges: ' + str(newEdges))
print ('Density: ' + str(newDensity))
print ('Node Connectivity (if 0, graph is disconnected): ' + str(nodeConnect))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('\n' + 'Shortest Path - Rock to Rap: ' + str(rockToRapShortPath))
print ('Shortest Path - Rock to Jazz: ' + str(rockToJazzShortPath))
print ('Shortest Path - Rap to Jazz: ' + str(rapToJazzShortPath))
print ('Shortest Path - Rock to Classical: ' + str(rockToClassicalShortPath))
print ('Shortest Path - Rap to Classical: ' + str(rapToClassicalShortPath))
print ('Shortest Path - Jazz to Classical: ' + str(jazzToClassicalShortPath) + '\n')
