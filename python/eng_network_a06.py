# eng_network_a06.py
# Version a06
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# November 3rd 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist 'uuGraphData.txt'
# Displays using parameters from 'config_nw.txt'
# writes 'nodeList.txt' with nodes and degrees (k) for each
# Removes self-loop edges

# Run AFTER 'eng_graph.py'

# import packages
import os
import networkx as nx
import pylab as plt

versionNumber = ("a06")

# create 'data' subdirectory if necessary
if not os.path.exists("data"):
    os.makedirs("data")

# create 'logs' subdirectory if necessary
if not os.path.exists("logs"):
    os.makedirs("logs")

# open file for writing log
logPath = os.path.join("logs", versionNumber + '_eng_network_log.txt')
runLog = open(logPath, 'a')

# Open file to write list of nodes
nodeListPath = os.path.join("data", versionNumber + '_nodeList.txt')
nodeListOP = open (nodeListPath, 'w') 

# Begin
print ('\n' + 'Graph Drawing Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Graph Drawing Thing | Version ' + versionNumber + '\n' + '\n')

# Read the edgelist
print ('\n' + 'Importing Edge List...')
inputPath = os.path.join("data", 'uuGraph_data.txt')
edgeList = open (inputPath, 'r')
enGraph = nx.read_edgelist(edgeList, delimiter=',')
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

# Remove self-loops
print ('\n' + 'Removing self-loops...')
for u,v in enGraph.edges():
	if u == v:
		enGraph.remove_edge(u,v)

	newEdges = nx.number_of_edges(enGraph)

# Write file with nodes and degree,for reference
print ('\n' + 'Writing node list...')
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
	n_size, n_alpha, node_colour, n_text_size, text_font, e_thickness, e_alpha, edge_colour, l_pos, edge_label_colour = line.split(",")
	
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

print ('\n' + 'Displaying graph...' + '\n')

plt.show()

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
runLog.write ('Connections (edges minus self-loops): ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
