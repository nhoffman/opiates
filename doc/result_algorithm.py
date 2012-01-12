#!/usr/bin/env python

import pygraphviz as pgv

g = """digraph {

  node [    fill=cornflowerblue,
            fontcolor=white,
            shape=diamond,
            style=filled];

  Step1 [   color=darkgoldenrod2,
            fontcolor=navy,
            label=start,
            shape=box];

  Step2;

  Step3a [  style=filled,
            fillcolor=grey80,
            color=grey80,
            shape=circle,
            fontcolor=navy];

  Step1  -> Step2;
  Step1  -> Step2a;
  Step2a -> Step3a;
  Step3;
  Step3a -> Step3;
  Step3a -> Step2b;
  Step2  -> Step2b;
  Step2b -> Step3;
  End [ shape=rectangle,
        color=darkgoldenrod2,
        fontcolor=navy];
  Step3  -> End [label=193];
}"""


g = r"""digraph {
  graph [];
  node [shape = "box"];
  edge [ordering = "in"];

  Start;

  Start -> Level1a [label = "conc(c) < low", outputorder = 1];
  Level1a [label = "a.check_qa(['is_peak_area']) \nand \n(b.check_qa(['spike']) or d.check_qa(['spike']))"];

  Level1a -> Level2a [label="true"];
  Level2a [label = "negative", shape = "circle", fontcolor = "green"];
  Level1a -> Level2b [label="false"];
  Level2b [label = "QA FAIL", shape = "octagon", fontcolor = "red"];

  Start -> Level1b [label = "conc(c) <= high \nand \nc.check_qa(['rrt', 'ion_ratio', 'signoise'])"];
  Level1b [label = "conc(c)", shape = "circle", fontcolor = "green"];

  Start -> Level1c [label = "a.check_qa(['rrt', 'ion_ratio', 'signoise'])"];
  Level1c [label = "conc(a) <= high"];

  Level1c -> Level2c [label = "true"];
  Level2c [label = "conc(a)*10", shape = "circle", fontcolor = "green"];

  Level1c -> Level2d [label="false"];
  Level2d [label = "> amr_high", shape = "circle", fontcolor = "green"];

  Start -> Level1d [label = "otherwise..."];
  Level1d [label = "QA FAIL", shape = "octagon", fontcolor = "red"];
}"""


G = pgv.AGraph(g)
G.layout(prog = 'dot') # default to neato
G.draw('file.png')

