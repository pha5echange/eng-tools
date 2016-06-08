# Genre Hive Plotter
# v. a0.5
# June 8th 2016
# by jmg*AT*phasechange*DOT*info

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Reads GEXF genre-network file and generates hive plot (as .svg file)

# Import packages
from pyveplot import *
from math import sin, cos, pi
from svgwrite.utils import rgb
from collections import OrderedDict
import os
import random
import networkx as nx
import numpy as np
import operator

versionNumber = ("a05")

# Make stuff if required
if not os.path.exists("networks/hives"):
	os.makedirs("networks/hives")

hSvgPath = os.path.join("networks/hives", 'hive_' + versionNumber + '.svg')
h = Hiveplot(hSvgPath)

# define as many axes as you need
axis0 = Axis( (150,150), (150,0), stroke = "black", stroke_width = 1, stroke_opacity = 0.6) 
axis1 = Axis( (150,150), (300,0), stroke = "gray", stroke_width = 1.1, stroke_opacity = 0.6)
axis2 = Axis( (150,150), (300,150), stroke = "blue", stroke_width = 1.2, stroke_opacity = 0.6)
axis3 = Axis( (150,150), (300,300), stroke = "purple", stroke_width = 1.3, stroke_opacity = 0.6)
axis4 = Axis( (150,150), (0,300), stroke = "red", stroke_width = 1.4, stroke_opacity = 0.6)
axis5 = Axis( (150,150), (0,150), stroke = "green", stroke_width = 1.5, stroke_opacity = 0.6)
axis6 = Axis( (150,150), (0,0), stroke = "yellow", stroke_width = 1.6, stroke_opacity = 0.6)

h.axes = [axis0, axis1, axis2, axis3, axis4, axis5, axis6]

# read gexf file, get genre inception dates and store in dictionary
dateDict = {}
gexfPath = os.path.join("gexf/ghp", 'hive.gexf')
g = nx.read_gexf(gexfPath)
nodeList = nx.nodes(g)

for i in nodeList:
  incepDate = nx.get_node_attributes(g, 'incepDate')
  intIncep = str(incepDate[i])
  dateDict[i] = intIncep

sortDates = OrderedDict(sorted(dateDict.items()))

print ('SortDates (OrderedDict): ' +'\n')
print sortDates
print

# Do nodes
dateCounts, bins = np.histogram(sortDates.values(), bins = [0,1900,1921,1955,1988,1998,2008,2016])
counts = np.histogram(g.degree(g.nodes()).values())
degrees   = g.degree(g.nodes())
sorted_dg = sorted(degrees.items(), key = operator.itemgetter(1))
maxDegTup = max(sorted_dg, key=operator.itemgetter(1))

mdtKey, mdtValue = maxDegTup
maxDeg = float(mdtValue)

print ('sorted_dg: ' +'\n')
print sorted_dg
print maxDeg

'''
try:
  delta6 = 0.99/float(counts[0])
except:
  delta6 = 0.99

try:  
  delta5 = 0.93/float(counts[1])
except:
  delta5 = 0.93

try:
  delta4 = 0.94/float(counts[2])
except:
  delta4 = 0.94

try:
  delta3 = 0.95/float(counts[3])
except:
  delta3 = 0.95

try:
  delta2 = 0.96/float(counts[4])
except:
  delta2 = 0.96

try:
  delta1 = 0.97/float(counts[5])
except:
  delta1 = 0.97

try:
  delta0 = 1/float(counts[6])
except:
  delta0 = 1


offset0 = 0
offset1 = 1
offset2 = 2
offset3 = 3
offset4 = 4
offset5 = 5
offset6 = 6
'''

# place nodes on axes
for k,v in sorted_dg:
    nd = Node(k)
    d = int(sortDates[k])
    deg = float(v)
    offset = float(deg/maxDeg)

    print nd
    print k
    print v
    print d
    print offset

    if d >= bins[0] and d < bins[1]:
        #offset0 += delta0
        axis0.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'yellow', stroke = 'black', stroke_width = 0.01)

    if d >= bins[1] and d < bins[2]:
        #offset1 += delta1
        axis1.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'green', stroke = 'black', stroke_width = 0.01)

    if d >= bins[2] and d < bins[3]:
        #offset2 += delta2
        axis2.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'red', stroke = 'black', stroke_width = 0.01)

    if d >= bins[3] and d < bins[4]:
        #offset3 += delta3
        axis3.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'purple', stroke = 'black', stroke_width = 0.01)

    if d >= bins[4] and d < bins[5]:
        #offset4 += delta4
        axis4.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'blue', stroke = 'black', stroke_width = 0.01)

    if d >= bins[5] and d < bins[6]:
        #offset5 += delta5
        axis5.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'gray', stroke = 'black', stroke_width = 0.01)

    if d >= bins[6]:
        #offset6 += delta6
        axis6.add_node(nd, offset)
        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = 'black', stroke = 'black', stroke_width = 0.01)

# Do edges
for e in g.edges():

    # edges from axis0 to axis1
    if (e[0] in axis0.nodes) and (e[1] in axis1.nodes):
        h.connect(axis0, e[0],
                  45,  # angle of invisible axis for source control points
                  axis1, e[1], 
                  -45, # angle of invisible axis for target control points
                  stroke_width   = 0.34,  # pass any SVG attributes to an edge
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis1.nodes):
        h.connect(axis0, e[1], 45,  
                  axis1, e[0], -45, 
                  stroke_width   = 0.34,  # pass any SVG attributes to an edge
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    # edges from axis0 to axis2
    if (e[0] in axis0.nodes) and (e[1] in axis2.nodes):
        h.connect(axis0, e[0], -45,
                  axis2, e[1], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis2.nodes):
        h.connect(axis0, e[1], -45,
                  axis2, e[0], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.9,
                  stroke         = 'red',
                  )

    # edges from axis0 to axis3
    if (e[0] in axis0.nodes) and (e[1] in axis3.nodes):
        h.connect(axis0, e[0], -45,
                  axis3, e[1], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis3.nodes):
        h.connect(axis0, e[1], -45,
                  axis3, e[0], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.9,
                  stroke         = 'red',
                  )

    # edges from axis0 to axis4
    if (e[0] in axis0.nodes) and (e[1] in axis4.nodes):
        h.connect(axis0, e[0], -45,
                  axis4, e[1], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis4.nodes):
        h.connect(axis0, e[1], -45,
                  axis4, e[0], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.9,
                  stroke         = 'red',
                  )

    # edges from axis0 to axis5
    if (e[0] in axis0.nodes) and (e[1] in axis5.nodes):
        h.connect(axis0, e[0], -45,
                  axis5, e[1], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis5.nodes):
        h.connect(axis0, e[1], -45,
                  axis5, e[0], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.9,
                  stroke         = 'red',
                  )

    # edges from axis0 to axis6
    if (e[0] in axis0.nodes) and (e[1] in axis6.nodes):
        h.connect(axis0, e[0], -45,
                  axis6, e[1], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'red',
                  )

    if (e[1] in axis0.nodes) and (e[0] in axis6.nodes):
        h.connect(axis0, e[1], -45,
                  axis6, e[0], 45,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.9,
                  stroke         = 'red',
                  )

    # edges from axis1 to axis2
    if (e[0] in axis1.nodes) and (e[1] in axis2.nodes):
        h.connect(axis1, e[0], 15,
                  axis2, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    if (e[1] in axis1.nodes) and (e[0] in axis2.nodes):
        h.connect(axis1, e[1], 15,
                  axis2, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    # edges from axis1 to axis3
    if (e[0] in axis1.nodes) and (e[1] in axis3.nodes):
        h.connect(axis1, e[0], 15,
                  axis3, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    if (e[1] in axis1.nodes) and (e[0] in axis3.nodes):
        h.connect(axis1, e[1], 15,
                  axis3, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    # edges from axis1 to axis4
    if (e[0] in axis1.nodes) and (e[1] in axis4.nodes):
        h.connect(axis1, e[0], 15,
                  axis4, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    if (e[1] in axis1.nodes) and (e[0] in axis4.nodes):
        h.connect(axis1, e[1], 15,
                  axis4, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    # edges from axis1 to axis5
    if (e[0] in axis1.nodes) and (e[1] in axis5.nodes):
        h.connect(axis1, e[0], 15,
                  axis5, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    if (e[1] in axis1.nodes) and (e[0] in axis5.nodes):
        h.connect(axis1, e[1], 15,
                  axis5, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    # edges from axis1 to axis6
    if (e[0] in axis1.nodes) and (e[1] in axis6.nodes):
        h.connect(axis1, e[0], 15,
                  axis6, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )

    if (e[1] in axis1.nodes) and (e[0] in axis6.nodes):
        h.connect(axis1, e[1], 15,
                  axis6, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'blue',
                  )
    
    # edges from axis2 to axis3
    if (e[0] in axis2.nodes) and (e[1] in axis3.nodes):
        h.connect(axis2, e[0], 15,
                  axis3, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple',
                  )

    if (e[1] in axis2.nodes) and (e[0] in axis3.nodes):
        h.connect(axis2, e[1], 15,
                  axis3, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple',
                  )

    # edges from axis2 to axis4
    if (e[0] in axis2.nodes) and (e[1] in axis4.nodes):
        h.connect(axis2, e[0], 15,
                  axis4, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple',
                  )

    if (e[1] in axis2.nodes) and (e[0] in axis4.nodes):
        h.connect(axis2, e[1], 15,
                  axis4, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple',
                  )

    # edges from axis2 to axis5
    if (e[0] in axis2.nodes) and (e[1] in axis5.nodes):
        h.connect(axis2, e[0], 15,
                  axis5, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple', 
                  )

    if (e[1] in axis2.nodes) and (e[0] in axis5.nodes):
        h.connect(axis2, e[1], 15,
                  axis5, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple',
                  )

    # edges from axis2 to axis6
    if (e[0] in axis2.nodes) and (e[1] in axis6.nodes):
        h.connect(axis2, e[0], 15,
                  axis6, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple', 
                  )

    if (e[1] in axis2.nodes) and (e[0] in axis6.nodes):
        h.connect(axis2, e[1], 15,
                  axis6, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'purple', 
                  )

    # edges from axis3 to axis4
    if (e[0] in axis3.nodes) and (e[1] in axis4.nodes):
        h.connect(axis3, e[0], 15,
                  axis4, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    if (e[1] in axis3.nodes) and (e[0] in axis4.nodes):
        h.connect(axis3, e[1], 15,
                  axis4, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    # edges from axis3 to axis5
    if (e[0] in axis3.nodes) and (e[1] in axis5.nodes):
        h.connect(axis3, e[0], 15,
                  axis5, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    if (e[1] in axis3.nodes) and (e[0] in axis5.nodes):
        h.connect(axis3, e[1], 15,
                  axis5, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    # edges from axis3 to axis6
    if (e[0] in axis3.nodes) and (e[1] in axis6.nodes):
        h.connect(axis3, e[0], 15,
                  axis6, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    if (e[1] in axis3.nodes) and (e[0] in axis6.nodes):
        h.connect(axis3, e[1], 15,
                  axis6, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'green', 
                  )

    # edges from axis4 to axis5
    if (e[0] in axis4.nodes) and (e[1] in axis5.nodes):
        h.connect(axis4, e[0], 15,
                  axis5, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'magenta',
                  )

    if (e[1] in axis4.nodes) and (e[0] in axis5.nodes):
        h.connect(axis4, e[1], 15,
                  axis5, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'magenta',
                  )

    # edges from axis4 to axis6
    if (e[0] in axis4.nodes) and (e[1] in axis6.nodes):
        h.connect(axis4, e[0], 15,
                  axis6, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'magenta',
                  )

    if (e[1] in axis4.nodes) and (e[0] in axis6.nodes):
        h.connect(axis4, e[1], 15,
                  axis6, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'magenta',
                  )

    # edges from axis5 to axis6
    if (e[0] in axis5.nodes) and (e[1] in axis6.nodes):
        h.connect(axis5, e[0], 15,
                  axis6, e[1], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'black',
                  )

    if (e[1] in axis5.nodes) and (e[0] in axis6.nodes):
        h.connect(axis5, e[1], 15,
                  axis6, e[0], -15,
                  stroke_width   = 0.34,
                  stroke_opacity = 0.4,
                  stroke         = 'black',
                  )

h.save()