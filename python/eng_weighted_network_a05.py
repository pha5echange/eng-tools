# eng_weighted_network_a05.py
# Version a05
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# November 3rd 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'wuGraphData.txt'
# Displays using parameters from 'config_nw.txt'
# writes 'weighted_nodeList.txt' with nodes and degrees (k) for each
# Removes self-loop edges

# Run AFTER 'eng_graph.py'

# import packages
import os
import networkx as nx
import pylab as plt

versionNumber = ("a05")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_weighted_network_log.txt')
runLog = open(logPath, 'a')

# Open file to write list of nodes
nodeListPath = os.path.join("data", versionNumber + '_weighted_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Open file to write image
# nwPngPath = os.path.join("networks", versionNumber + '_wuNw.eps')
# nwPng = open (nwPngPath, 'w')

# Begin
print ('\n' + 'Weighted Graph Drawing Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Weighted Graph Drawing Thing | Version ' + versionNumber + '\n' + '\n')

print ('\n' + 'Importing Weighted Edge List...')
inputPath = os.path.join("data", 'wuGraph_data.txt')
edgeList = open (inputPath, 'r')
enGraph = nx.read_weighted_edgelist(edgeList, delimiter=',')
edgeList.close()

print ('\n' + 'Calculating nodes, edges and density...' + '\n')
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

# Remove self-loops and clean edge labels
print ('\n' + 'Removing self-loops and cleaning edge-labels...')
labels = {}
for u,v,data in enGraph.edges(data=True):
	if u == v:
		enGraph.remove_edge(u,v)

	newEdges = nx.number_of_edges(enGraph)

	labels[(u,v)] = data ['weight']

# Write file with nodes and degree,for reference
print ('Writing node list...' + '\n')
for i in nodeList:
	nodeDegree = enGraph.degree(i)
	nodeListOP.write(str(i) + ',' + str(nodeDegree) + '\n')

nodeListOP.close()

# Graph plotting parameters - moved to config file 'config_nw.txt'
print ('\n' + 'Reading layout config. file...')

# open and read 'config_nw.txt'
nwConfig = open('config_nw.txt').readlines()

# remove the first line
firstLine = nwConfig.pop(0)

for line in nwConfig:
	n_size, n_alpha, node_colour, n_text_size, text_font, e_thickness, e_alpha, edge_colour, l_pos = line.split(",")
	
node_size = int(n_size)
node_alpha = float(n_alpha)
node_text_size = int(n_text_size)
edge_thickness = int(e_thickness)
edge_alpha = float(e_alpha)
label_pos = float(l_pos)

print ('\n' + 'Drawing Graph...' + '\n')
# nx.draw(enGraph)
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)
nx.draw_networkx_edge_labels(enGraph, graph_pos, edge_labels = labels, label_pos = label_pos, font_size = node_text_size, font_family = text_font)

print ('\n' + 'Displaying graph...' + '\n')

plt.show()
# plt.savefig(nwPng, format = 'eps')

print ('\n' + 'Final Run Information' + '\n')
print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Edges after self-loop removal: ' + str(newEdges))
print ('Connections (edges minus self-loops): ' + str(connections))
print ('Density: ' + str(density))

runLog.write ('\n' + 'Final Run Information' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Edges after self-loop removal: ' + str(newEdges) + '\n')
runLog.write ('Connections: ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
