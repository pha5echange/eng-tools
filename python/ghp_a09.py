# Genre Hive Plotter
# v. a0.9
# October 7th 2016
# by jmg*AT*phasechange*DOT*info

# Licence: http://creativecommons.org/licenses/by-nc-sa/3.0/
# Source code at: https://github.com/pha5echange/eng-tools

# Reads GEXF genre-network files from `gexf/directed'
# Generates hive plots (as .svg file) and saves in `networks/hives/all'

# Import packages
from pyveplot import *
from math import sin, cos, pi
from svgwrite.utils import rgb
from collections import OrderedDict
import os
import networkx as nx
import numpy as np
import operator

versionNumber = ("a09")

# Begin
print ('\n' + "Genre Data Hive Plotter | Version " + versionNumber + " | Starting...")

# Make stuff if required
if not os.path.exists("networks/hives/all"):
	os.makedirs("networks/hives/all")

# line parameters
axisWidth = 1.0
axisOpacity = 1.0
nodeStrokeWidth = 0.07
edgeWidth = 0.1
edgeOpacity = 0.2

#colour parameters
nodeStrokeCol = "black"
prpCol = "gold"
prbrCol = "green"
prmCol = "red"
prdCol = "purple"
prICol = "blue"
prsmCol = "darkgray"
pstsmCol = "darkolivegreen"

# Create dictionary for incepDates
dateDict = {}

# Get user input
print
print ("The maximal degree of the graph dictates where the nodes are placed on the axes.")
maxDeg = int(input ("Enter the maximal degree for all graphs (or 0 to let the GEXF file dictate this): "))
print

# get list of files from gexf folder
gexfPath = 'gexf/directed'
fileNames = [f for f in os.listdir(gexfPath) if f.endswith('.gexf')]

for index in range(len(fileNames)):

	# define axes as required
	axis0 = Axis( (150,150), (150,0), stroke = prpCol, stroke_width = axisWidth, stroke_opacity = axisOpacity) 
	axis1 = Axis( (150,150), (300,0), stroke = prbrCol, stroke_width = axisWidth, stroke_opacity = axisOpacity)
	axis2 = Axis( (150,150), (300,150), stroke = prmCol, stroke_width = axisWidth, stroke_opacity = axisOpacity)
	axis3 = Axis( (150,150), (300,300), stroke = prdCol, stroke_width = axisWidth, stroke_opacity = axisOpacity)
	axis4 = Axis( (150,150), (0,300), stroke = prICol, stroke_width = axisWidth, stroke_opacity = axisOpacity)
	axis5 = Axis( (150,150), (0,150), stroke = prsmCol, stroke_width = axisWidth, stroke_opacity = axisOpacity)
	axis6 = Axis( (150,150), (0,0), stroke = pstsmCol, stroke_width = axisWidth, stroke_opacity = axisOpacity)

	gexfPath = os.path.join("gexf/directed", fileNames[index])
	gexfFile = str(fileNames[index])
	gexfYear, fileExtension = gexfFile.split(".")
	omegaYear = int(gexfYear)
	g = nx.read_gexf(gexfPath)

	hSvgPath = os.path.join("networks/hives/all", 'hive_' + versionNumber + '_' + gexfYear + '.svg')
	h = Hiveplot(hSvgPath)
	h.axes = [axis0, axis1, axis2, axis3, axis4, axis5, axis6]

	nodeList = nx.nodes(g)

	for i in nodeList:
	  incepDate = nx.get_node_attributes(g, 'incepDate')
	  intIncep = str(incepDate[i])
	  dateDict[i] = intIncep

	sortDates = OrderedDict(sorted(dateDict.items()))

	print ('SortDates (OrderedDict): ')
	print sortDates
	print

	# Do nodes
	dateCounts, bins = np.histogram(sortDates.values(), bins = [0,1900,1921,1955,1988,1998,2008,2016])
	counts = np.histogram(g.degree(g.nodes()).values())
	degrees   = g.degree(g.nodes())
	sorted_dg = sorted(degrees.items(), key = operator.itemgetter(1))
	maxDegTup = max(sorted_dg, key=operator.itemgetter(1))

	mdtKey, mdtValue = maxDegTup

	if maxDeg == 0:
	  maxDeg = float(mdtValue)

	print ('Items in bins: ')
	print (dateCounts)
	print
	print ('Contents of sorted_dg: ')
	print sorted_dg
	print
	print ('Maximum Degree:')
	print (maxDeg)
	print

	# place nodes on axes
	for k,v in sorted_dg:
	    nd = Node(k)
	    d = int(sortDates[k])
	    deg = float(v)
	    offset = float(deg/maxDeg)

	    print ('Node: ')
	    print nd
	    print ('Key: ')
	    print k
	    print ('Degree: ')
	    print v
	    print ('Inception date: ')
	    print d
	    print ('Offset: ')
	    print offset
	    print

	    if d >= bins[0] and d < bins[1]:
	        #offset0 += delta0
	        axis0.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prpCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[1] and d < bins[2]:
	        #offset1 += delta1
	        axis1.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prbrCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[2] and d < bins[3]:
	        #offset2 += delta2
	        axis2.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prmCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[3] and d < bins[4]:
	        #offset3 += delta3
	        axis3.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prdCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[4] and d < bins[5]:
	        #offset4 += delta4
	        axis4.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prICol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[5] and d < bins[6]:
	        #offset5 += delta5
	        axis5.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = prsmCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	    if d >= bins[6]:
	        #offset6 += delta6
	        axis6.add_node(nd, offset)
	        nd.dwg = nd.dwg.circle(center = (nd.x, nd.y), fill = pstsmCol, stroke = nodeStrokeCol, stroke_width = nodeStrokeWidth)

	# Do edges
	for e in g.edges():

		# edges from axis0 to axis0
	    if (e[0] in axis0.nodes) and (e[1] in axis0.nodes):
	        h.connect(axis0, e[0], 45,  # angle of invisible axis for source control points
	                  axis0, e[1], -45, # angle of invisible axis for target control points
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis1
	    if (e[0] in axis0.nodes) and (e[1] in axis1.nodes):
	        h.connect(axis0, e[0], 45,  
	                  axis1, e[1], -45, 
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis1.nodes):
	        h.connect(axis0, e[1], 45,  
	                  axis1, e[0], -45, 
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis2
	    if (e[0] in axis0.nodes) and (e[1] in axis2.nodes):
	        h.connect(axis0, e[0], -45,
	                  axis2, e[1], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis2.nodes):
	        h.connect(axis0, e[1], -45,
	                  axis2, e[0], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis3
	    if (e[0] in axis0.nodes) and (e[1] in axis3.nodes):
	        h.connect(axis0, e[0], -45,
	                  axis3, e[1], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis3.nodes):
	        h.connect(axis0, e[1], -45,
	                  axis3, e[0], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis4
	    if (e[0] in axis0.nodes) and (e[1] in axis4.nodes):
	        h.connect(axis0, e[0], -45,
	                  axis4, e[1], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis4.nodes):
	        h.connect(axis0, e[1], -45,
	                  axis4, e[0], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis5
	    if (e[0] in axis0.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis0, e[0], -45,
	                  axis5, e[1], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis5.nodes):
	        h.connect(axis0, e[1], -45,
	                  axis5, e[0], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis0 to axis6
	    if (e[0] in axis0.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis0, e[0], -45,
	                  axis6, e[1], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    if (e[1] in axis0.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis0, e[1], -45,
	                  axis6, e[0], 45,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prpCol,
	                  )

	    # edges from axis1 to axis1
	    if (e[0] in axis1.nodes) and (e[1] in axis1.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis1, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    # edges from axis1 to axis2
	    if (e[0] in axis1.nodes) and (e[1] in axis2.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis2, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    if (e[1] in axis1.nodes) and (e[0] in axis2.nodes):
	        h.connect(axis1, e[1], 15,
	                  axis2, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    # edges from axis1 to axis3
	    if (e[0] in axis1.nodes) and (e[1] in axis3.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis3, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    if (e[1] in axis1.nodes) and (e[0] in axis3.nodes):
	        h.connect(axis1, e[1], 15,
	                  axis3, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    # edges from axis1 to axis4
	    if (e[0] in axis1.nodes) and (e[1] in axis4.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis4, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    if (e[1] in axis1.nodes) and (e[0] in axis4.nodes):
	        h.connect(axis1, e[1], 15,
	                  axis4, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    # edges from axis1 to axis5
	    if (e[0] in axis1.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis5, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    if (e[1] in axis1.nodes) and (e[0] in axis5.nodes):
	        h.connect(axis1, e[1], 15,
	                  axis5, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    # edges from axis1 to axis6
	    if (e[0] in axis1.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis1, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )

	    if (e[1] in axis1.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis1, e[1], 15,
	                  axis6, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prbrCol,
	                  )
	 
	    # edges from axis2 to axis2
	    if (e[0] in axis2.nodes) and (e[1] in axis2.nodes):
	        h.connect(axis2, e[0], 15,
	                  axis2, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    # edges from axis2 to axis3
	    if (e[0] in axis2.nodes) and (e[1] in axis3.nodes):
	        h.connect(axis2, e[0], 15,
	                  axis3, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    if (e[1] in axis2.nodes) and (e[0] in axis3.nodes):
	        h.connect(axis2, e[1], 15,
	                  axis3, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    # edges from axis2 to axis4
	    if (e[0] in axis2.nodes) and (e[1] in axis4.nodes):
	        h.connect(axis2, e[0], 15,
	                  axis4, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    if (e[1] in axis2.nodes) and (e[0] in axis4.nodes):
	        h.connect(axis2, e[1], 15,
	                  axis4, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    # edges from axis2 to axis5
	    if (e[0] in axis2.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis2, e[0], 15,
	                  axis5, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol, 
	                  )

	    if (e[1] in axis2.nodes) and (e[0] in axis5.nodes):
	        h.connect(axis2, e[1], 15,
	                  axis5, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol,
	                  )

	    # edges from axis2 to axis6
	    if (e[0] in axis2.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis2, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol, 
	                  )

	    if (e[1] in axis2.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis2, e[1], 15,
	                  axis6, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prmCol, 
	                  )

	    # edges from axis3 to axis3
	    if (e[0] in axis3.nodes) and (e[1] in axis3.nodes):
	        h.connect(axis3, e[0], 15,
	                  axis3, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    # edges from axis3 to axis4
	    if (e[0] in axis3.nodes) and (e[1] in axis4.nodes):
	        h.connect(axis3, e[0], 15,
	                  axis4, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    if (e[1] in axis3.nodes) and (e[0] in axis4.nodes):
	        h.connect(axis3, e[1], 15,
	                  axis4, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    # edges from axis3 to axis5
	    if (e[0] in axis3.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis3, e[0], 15,
	                  axis5, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    if (e[1] in axis3.nodes) and (e[0] in axis5.nodes):
	        h.connect(axis3, e[1], 15,
	                  axis5, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    # edges from axis3 to axis6
	    if (e[0] in axis3.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis3, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    if (e[1] in axis3.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis3, e[1], 15,
	                  axis6, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prdCol, 
	                  )

	    # edges from axis4 to axis4
	    if (e[0] in axis4.nodes) and (e[1] in axis4.nodes):
	        h.connect(axis4, e[0], 15,
	                  axis4, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prICol,
	                  )

	    # edges from axis4 to axis5
	    if (e[0] in axis4.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis4, e[0], 15,
	                  axis5, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prICol,
	                  )

	    if (e[1] in axis4.nodes) and (e[0] in axis5.nodes):
	        h.connect(axis4, e[1], 15,
	                  axis5, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prICol,
	                  )

	    # edges from axis4 to axis6
	    if (e[0] in axis4.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis4, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prICol,
	                  )

	    if (e[1] in axis4.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis4, e[1], 15,
	                  axis6, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prICol,
	                  )

	    # edges from axis5 to axis5
	    if (e[0] in axis5.nodes) and (e[1] in axis5.nodes):
	        h.connect(axis5, e[0], 15,
	                  axis5, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prsmCol,
	                  )

	    # edges from axis5 to axis6
	    if (e[0] in axis5.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis5, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prsmCol,
	                  )

	    if (e[1] in axis5.nodes) and (e[0] in axis6.nodes):
	        h.connect(axis5, e[1], 15,
	                  axis6, e[0], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = prsmCol,
	                  )

	    # edges from axis6 to axis6
	    if (e[0] in axis6.nodes) and (e[1] in axis6.nodes):
	        h.connect(axis6, e[0], 15,
	                  axis6, e[1], -15,
	                  stroke_width   = edgeWidth,  
	                  stroke_opacity = edgeOpacity,
	                  stroke         = pstsmCol,
	                  )

	h.save()

	# clear axes the hard way (can't find another way)
	axis0 = Axis( (150,150), (150,0), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0) 
	axis1 = Axis( (150,150), (300,0), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
	axis2 = Axis( (150,150), (300,150), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
	axis3 = Axis( (150,150), (300,300), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
	axis4 = Axis( (150,150), (0,300), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
	axis5 = Axis( (150,150), (0,150), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
	axis6 = Axis( (150,150), (0,0), stroke = "white", stroke_width = axisWidth, stroke_opacity = 0)
