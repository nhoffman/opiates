"""Perform QA calculations."""

import logging
from os import path
import xml.etree.ElementTree
import csv
from collections import OrderedDict
from itertools import chain

from opiate import matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, group_samples
from opiate.display import display_qa_results
from opiate.calculations import perform_qa

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    parser.add_argument('-a','--show-all', help='Show all results for each compound (ie, not just failures)',
                        action = 'store_true', default = False)
    parser.add_argument('-m','--no-matrix', help='Perform all calculations on each compound, regardless of definitions in the metrix file',
                        action = 'store_true', default = False)

    
def action(args):
    qadata = qa_from_csv(qafile)
    matrix = None if args.no_matrix else read_matrix(matrix_file)
    controls, sample_groups = group_samples(args.infile)

    # controls
    retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in controls.values())
    display_qa_results(retvals, args.show_all)

    # specimens
    for group_label, samples in sample_groups.items():
        print group_label
        retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in samples)
        display_qa_results(retvals, args.show_all)
        
if __name__ == '__main__':
    main()
    
