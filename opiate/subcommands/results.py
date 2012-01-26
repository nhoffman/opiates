"""Show concentration of each compound."""

from collections import OrderedDict
from itertools import chain, ifilter
from os import path

import pprint
import argparse
import csv
import json
import logging
import sys
import xml.etree.ElementTree

from opiate import __version__, matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, get_input, get_samples
from opiate.display import display_results
from opiate.utils import flatten, get_outfile
from opiate.calculations import add_ion_ratios
from opiate import subcommands

log = logging.getLogger(__name__)

def build_parser(parser):
    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)
    subcommands.add_outdir(parser)
    subcommands.add_no_calculate_ion_ratio_avg(parser)    
    subcommands.add_split_desc(parser)
    parser.add_argument('--c-first', action = 'store_true', default = False,
                        help = 'use "c first" algorithm for results (default is "a first")')
    parser.add_argument('--no-groups', action = 'store_false', default = True,
                        dest = 'grouped',
                        help = 'Do not group columns by worksheet.')
    
def action(args):

    controls, sample_groups = get_input(args.infile, split_description = args.split_desc)
    qadata = qa_from_csv(qafile)
    matrix = read_matrix(matrix_file)

    style = 'screen' if args.outfile == sys.stdout else 'file'
    outfile = get_outfile(args, label = 'results', ext = 'csv')
    
    if args.calculate_ion_ratios:
        qadata = add_ion_ratios(qadata, controls)

    samples = get_samples(controls, sample_groups, qadata, matrix)
    display_results(samples, outfile, style = style, grouped = args.grouped)

    if args.outfile is None:
        outfile.close()

