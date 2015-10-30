# eng_network_a04.py
# Version a04
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 30th 2015

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/

# Plots network graph from edgelist and displays

# Run AFTER 'eng_graph.py'

# import packages
import os
import networkx as nx
import pylab as plt

versionNumber = ("a04")

# Graph plotting parameters
node_size = 500
node_alpha = 0.4
node_colour = 'silver'
node_text_size = 10
text_font = 'sans-serif'
edge_thickness = 1
edge_alpha = 0.2
edge_colour = 'gray'

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

# Get the edgelist
inputPath = os.path.join("data", 'uuGraph_data.txt')
edgeList = open (inputPath, 'r')

# Begin
print ('\n' + 'Graph Drawing Thing | Version ' + versionNumber + ' | Starting...')
runLog.write ('Graph Drawing Thing | Version ' + versionNumber + '\n' + '\n')

print ('\n' + 'Importing Edge List...')
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
print ('Connections: ' + str(connections))
print ('Density: ' + str(density) + '\n')

print ('Writing node list...' + '\n')
for i in nodeList:
	nodeListOP.write(str(i) + '\n')

print ('\n' + 'Drawing Graph...' + '\n')
# nx.draw(enGraph)
graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)

nodeListOP.close()

print ('Displaying graph...' + '\n')

plt.show()

runLog.write ('\n' + 'Run Information' + '\n' + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Connections: ' + str(connections) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
