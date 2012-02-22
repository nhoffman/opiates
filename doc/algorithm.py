#!/usr/bin/env python

import pygraphviz as pgv

infile = 'algorithm.gv'
outfile = infile.replace('.gv', '.png')

with open(infile) as f:
    g = f.read()

G = pgv.AGraph(g)
G.layout(prog = 'dot') # default to neato
G.draw(outfile)

