# eng_network_wu_b02.py
# Version b02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# November 17th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'wuGraphData.txt'
# Displays using parameters from 'config_nw.txt'
# Writes 'weighted_nodeList.txt' with nodes and degrees (k) for each
# Writes analysis file to 'results\'
# Writes eps image to 'networks\..'
# Removes self-loop edges zero-degree nodes if required

# Run AFTER 'eng_nodesets.py'

# import packages
import os
import resource
import networkx as nx
from networkx.algorithms.approximation import clique
import matplotlib.pyplot as plt
from datetime import datetime

versionNumber = ("b02")

# Initiate timing of run
runDate = datetime.now()
startTime = datetime.now()

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# create 'gexf' subdirectory if necessary
if not os.path.exists("gexf"):
	os.makedirs("gexf")

# create 'results' subdirectory if necessary
if not os.path.exists("results"):
	os.makedirs("results")

# create 'networks' subdirectory if necessary
if not os.path.exists("networks"):
    os.makedirs("networks")

# open file to write list of nodes
nodeListPath = os.path.join("data", versionNumber + '_wu_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_network_wu_log.txt')
runLog = open(logPath, 'a')

# open file for writing gexf
gexfPath = os.path.join("gexf", versionNumber + '_eng_network_wu.gexf')
gexfFile = open(gexfPath, 'w')

# open file for analysis results
anPath = os.path.join("results", versionNumber + '_eng_network_wu_analysis.txt')
anFile = open(anPath, 'w')

# Open file to write image
#nwImgPath = os.path.join("networks", versionNumber + '_' + str(startTime) + '_wu_Nw.eps')
#nwImg = open (nwImgPath, 'w')

# Begin
print ('\n' + 'Weighted Network Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Weighted Network Thing | Version ' + versionNumber + '\n' + '\n')
anFile.write ('Weighted Network Thing | Version ' + versionNumber + '\n' + '\n')

print
selfLoopIP = int(input ("Enter 0 here to remove self-loop edges: "))
isolatedIP = int(input ("Enter 0 here to remove isolated nodes: "))

# Read the edgelist
print ('\n' + 'Importing Weighted Edge List...')
inputPath = os.path.join("data", 'wuGraph_data.txt')
edgeList = open (inputPath, 'r')
enGraph = nx.read_weighted_edgelist(edgeList, delimiter=',')
edgeList.close()

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
print ('Density: ' + str(density))

runLog.write ('\n' + 'Initial data: ' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')

if selfLoopIP == 0:
	# Remove self-loops
	print ('\n' + 'Removing self-loops...' + '\n')
	runLog.write('\n' + 'Removing self-loops...' + '\n')
	for u,v,data in enGraph.edges(data=True):
		if u == v:
			enGraph.remove_edge(u,v)
			print ('removed self-loop ' + str(u))
else:
	print ('\n' + 'Self-loops intact.')
	runLog.write('\n' + 'Self-loops intact.' + '\n')

if isolatedIP == 0:
	# remove zero degree nodes
	print ('\n' + 'Removing isolated nodes...' +'\n')
	runLog.write ('\n' + 'Isolated nodes removed:' +'\n' + '\n')
	for i in nodeList:
		if nx.is_isolate(enGraph,i):
			enGraph.remove_node(i)
			print ('removed node ' + str(i))
			runLog.write('Removed node ' + str(i) +'\n')
else:
	print ('\n' + 'Isolated nodes intact.')
	runLog.write('\n' + 'Isolated nodes intact.' + '\n')

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list...')
for i in nodeList:
	nodeDegree = enGraph.degree(i)
	nodeListOP.write(str(i) + ',' + str(nodeDegree) + '\n')

nodeListOP.close()

# Cleaning edge-labels
print ('\n' + 'Cleaning edge labels...')
labels = {}
for u,v,data in enGraph.edges(data=True):
	labels[(u,v)] = int(data ['weight'])

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

# write gexf file
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
print ('Clique removal...')
cliqueRemoval = clique.clique_removal(enGraph)
print ('Node connectivity...')
nodeConnect = nx.node_connectivity(enGraph)
print ('Average node connectivity...')
avNodeConnect = nx.average_node_connectivity(enGraph)
print ('Edge connectivity...')
edgeConnect = nx.edge_connectivity(enGraph)

# various shortest paths, just to see...
rockToRapShortPath = nx.shortest_path(enGraph,source='rock',target='rap')
rockToJazzShortPath = nx.shortest_path(enGraph,source='rock',target='jazz')
rapToJazzShortPath = nx.shortest_path(enGraph,source='rap',target='jazz')
rockToClassicalShortPath = nx.shortest_path(enGraph,source='rock',target='classical')
rapToClassicalShortPath = nx.shortest_path(enGraph,source='rap',target='classical')
jazzToClassicalShortPath = nx.shortest_path(enGraph,source='jazz',target='classical')

# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('\n' + 'Reading layout config file...')

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
edge_text_size = int(e_text_size)

print ('\n' + 'Laying out graph...' + '\n')
#nx.draw(enGraph)
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)
nx.draw_networkx_edge_labels(enGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_color = edge_label_colour, font_size = edge_text_size, font_family = text_font)

#print ('\n' + 'Writing image file...')
#plt.savefig(nwImg, format = 'eps')
#nwImg.close()

#print ('\n' + 'Displaying graph...')
#plt.show()

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
anFile.write ('Connected Components: ' + str(connectComp) + '\n' + '\n')
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
anFile.close()

print ('\n' + 'Final Run Information' + '\n')
print ('Date of run: {}'.format(runDate))
print ('Duration of run : {}'.format(endTime - startTime))
print ('Memory Used: ' + str(memUseMb) + 'Mb')
print ('Nodes: ' + str(newNodes))
print ('Edges: ' + str(newEdges))
print ('Density: ' + str(newDensity))
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Laplacian Spectrum: ')
print (eigenArray)
print
print ('Connected Components: ' + str(connectComp) + '\n')
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
