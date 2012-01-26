#!/usr/bin/env python

import pygraphviz as pgv

g = r"""digraph {

  node [shape = "box", order = "in"];

  Start [label = "conc(c) < low"];

  Start -> Level1b [label = "yes"];
  Level1b [label = "a.check_qa(['is_peak_area']) \nand\n (b.check_qa(['spike']) or d.check_qa(['spike']))"];

  Start -> Level1a [label = "no"];
  Level1a [label = "conc(c) <= high \nand\n c.check_qa(['rrt', 'ion_ratio', 'signoise'])"];

  Level1b -> Level2b [label = "yes"];
  Level2b [label = "< amr_low", shape = "circle", fontcolor = "green"];

  Level1b -> Level2c [label = "no"];
  Level2c [label = "QA FAIL", shape = "octagon", fontcolor = "red"];

  Level1a -> Level2d [label = "yes"];
  Level2d [label = "conc(c)", shape = "circle", fontcolor = "green"];

  Level1a -> Level2a [label= "no" ];
  Level2a [label = "a.check_qa(['rrt', 'ion_ratio', 'signoise'])"];

  Level2a -> Level3b [label = "yes"];
  Level3b [label = "conc(a) <= high"];

  Level2a -> Level3a [label = "no"];
  Level3a [label = "QA FAIL", shape = "octagon", fontcolor = "red"];

  Level3b -> Level4a [label = "yes"];
  Level4a [label = "conc(a)*10", shape = "circle", fontcolor = "green"];

  Level3b -> Level4b [label = "no"];
  Level4b [label = "> amr_high", shape = "circle", fontcolor = "green"];
}"""


G = pgv.AGraph(g)
G.layout(prog = 'dot') # default to neato
G.draw('result_algorithm.png')

