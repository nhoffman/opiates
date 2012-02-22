#!/usr/bin/env python

import pygraphviz as pgv

infile = 'algorithm.gv'
outfile = infile.replace('.gv', '.png')

# with open(infile) as f:
#     g = f.read()
# G = pgv.AGraph(g)

fail = dict(shape = "octagon", fontcolor = "red")
ok = dict(shape = "ellipse", fontcolor = "green")

G = pgv.AGraph(directed = True)

# set node defaults here
G.node_attr['shape'] = 'rectangle'

G.add_node('start', label = "conc(c) < low")
G.add_node('A', label = r'QA passes for IS Peak Area (a) \nand Spike Test (b or d) ')

G.add_edge('start', 'A', label = "yes")

G.layout(prog = 'dot') # default to neato
G.draw(outfile)

