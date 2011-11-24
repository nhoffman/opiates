"""Perform QA calculations."""

from collections import OrderedDict
from itertools import chain
from os import path

import argparse
import csv
import json
import logging
import sys
import xml.etree.ElementTree

from opiate import matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, group_samples
# from opiate.display import display_sample_group, display_controls

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    parser.add_argument('-o','--outfile', metavar = 'FILE', default = sys.stdout,
                        type = argparse.FileType('w'))
    parser.add_argument('-a','--show-all', help='Show all results for each compound (ie, not just failures)',
                        action = 'store_true', default = False)
    parser.add_argument('-m','--no-matrix', help='Perform all calculations on each compound, regardless of definitions in the metrix file',
                        action = 'store_true', default = False)
    
    
def action(args):
    qadata = qa_from_csv(qafile)
    matrix = None if args.no_matrix else read_matrix(matrix_file)

    if args.infile.lower().endswith('.xml'):
        controls, sample_groups = group_samples(args.infile)
    else:
        with open(args.infile) as f:
            controls, sample_groups = json.load(f)        
        
    # controls
    retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in controls.values())
    display_qa_results(retvals, args.outfile, args.show_all)

    # specimens
    # for group_label, samples in sample_groups.items():
    #     print group_label
    #     retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in samples)
    #     display_qa_results(retvals, args.show_all)
        
if __name__ == '__main__':
    main()
    
