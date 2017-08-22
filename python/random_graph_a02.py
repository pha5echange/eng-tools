# random_graph_a02.py
# Version a02
# by jmg - j.gagen*AT*gold*DOT*ac*DOT*uk
# October 20th 2016

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Random graph maker for comparison with `eng_networks'

import os
import networkx as nx

versionNumber = ("a02")

# Open file for writing log
logPath = os.path.join("logs", 'random_network_' + versionNumber + '_log.txt')
runLog = open(logPath, 'a')

# Begin
print ('\n' + "Random Directed Network Maker Thing | Version " + versionNumber + " | Starting..." + '\n')

# Get user input
print
dateIP = int(input ("Enter an omega year for this graph: "))
omegaYear = str(dateIP)
nodeIP = int(input("How many nodes should this graph have? "))
edgeIP = int(input("How many edges should this graph have? "))

# Generate a random, directed graph with nodeIP nodes and edgeIP edges
dG = nx.gnm_random_graph(nodeIP, edgeIP, directed=True)

# Calculate basic graph statistics
nodes = nx.number_of_nodes(dG)
edges = nx.number_of_edges(dG)
density = nx.density(dG)
isDag = nx.is_directed_acyclic_graph(dG)
dgIsolateList = nx.isolates(dG)
dgSelfLoops = dG.number_of_selfloops()

# Write GEXF file
gexfDPath = os.path.join("gexf/directed", omegaYear + '.gexf')
gexfDFile = open(gexfDPath, 'w')
nx.write_gexf(dG, gexfDFile)
gexfDFile.close()

# Generate undirected graph for analysis
# Previous attempts to reconfigure the directed graph have screwed up the edge-count
# Therefore, am creating from scratch

# Attempt 1 - lost edges
#uG = dG.to_undirected()
# Attempt 2 - still lost edges
#uG = nx.Graph()
#uG.add_nodes_from(dG.nodes())
#uG.add_edges_from(dG.edges())
# Attempt 3 - let's see
uG = nx.gnm_random_graph(nodeIP, edgeIP)


# Calculate graph statistics
avClustering = nx.average_clustering(uG)
connectComp = [len(c) for c in sorted(nx.connected_components(uG), key=len, reverse=True)]
cl = nx.find_cliques(uG)
cl_sizes = [len(c) for c in cl]
ugIsolateList = nx.isolates(uG)
ugSelfLoops = uG.number_of_selfloops()

print
print ('Directed Graph Information' + '\n')
print ('Omega Year: ' + str(dateIP))
print ('Nodes: ' + str(nodes))
print ('Edges: ' + str(edges))
print ('Density: ' + str(density))
print ('Isolates:' + str(len(dgIsolateList)))
print ('Self Loops: ' + str(dgSelfLoops))
print
print (str(nx.info(dG)))
print

print ('Undirected Graph Information' + '\n')
print ('Average Clustering Coefficient: ' + str(avClustering))
print ('Connected Components: ' + str(connectComp))
print ('Isolates:' + str(len(ugIsolateList)))
print ('Self Loops: ' + str(ugSelfLoops))
print
print (str(nx.info(uG)))
print

runLog.write ('Directed Graph Information' + '\n')
runLog.write ('Omega Year: ' + str(dateIP) + '\n')
runLog.write ('Nodes: ' + str(nodes) + '\n')
runLog.write ('Edges: ' + str(edges) + '\n')
runLog.write ('Density: ' + str(density) + '\n')
runLog.write ('Isolates:' + str(len(dgIsolateList)) + '\n')
runLog.write ('Self Loops: ' + str(dgSelfLoops) + '\n')
runLog.write (str(nx.info(dG)) + '\n' + '\n')

runLog.write ('Undirected Graph Information' + '\n')
runLog.write ('Average Clustering Coefficient: ' + str(avClustering) + '\n')
runLog.write ('Connected Components: ' + str(connectComp) + '\n')
runLog.write ('Isolates:' + str(len(ugIsolateList)) + '\n')
runLog.write ('Self Loops: ' + str(ugSelfLoops) + '\n')
runLog.write (str(nx.info(uG)) + '\n' + '\n')
runLog.close()
