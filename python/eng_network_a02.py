# eng_network_a02.py
# October 30th 2015

# Plots network graph from edgelist and displays

import os
import networkx as nx
import pylab as plt

versionNumber = ("a02")

node_size = 400
node_alpha = 0.5
node_colour = 'blue'
node_text_size = 10
text_font = 'sans-serif'
edge_thickness = 1
edge_alpha = 0.2
edge_colour = 'red'

inputPath = os.path.join("data", 'uuGraph_data.txt')
edgeList = open (inputPath, 'r')

print ('\n' + 'Graph Drawing Thing v a01')
print ('\n' + 'Importing Edge List...')
enGraph = nx.read_edgelist(edgeList, delimiter=',')

print ('\n' + 'Drawing Graph...' + '\n')
# nx.draw(enGraph)

graph_pos = nx.spring_layout(enGraph)
nx.draw_networkx_nodes(enGraph, graph_pos, node_size = node_size, alpha = node_alpha, node_color=node_colour)
nx.draw_networkx_edges(enGraph, graph_pos, width = edge_thickness, alpha = edge_alpha, color = edge_colour)
nx.draw_networkx_labels(enGraph, graph_pos, font_size = node_text_size, font_family = text_font)

print ('\n' + 'Calculating nodes, edges and density...' + '\n')
nodes = nx.number_of_nodes(enGraph)
edges = nx.number_of_edges(enGraph)
density = nx.density(enGraph)

print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Density: ' + str(density))

print ('Displaying graph...' + '\n')

plt.show()
