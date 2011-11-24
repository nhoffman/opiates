"""Perform QA calculations."""

from collections import OrderedDict
from itertools import chain, ifilter
from os import path

import argparse
import csv
import json
import logging
import sys
import xml.etree.ElementTree

from opiate import matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, group_samples
from opiate.display import display_specimens
from opiate.containers import Compound, flatten

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    parser.add_argument('-o','--outfile', metavar = 'FILE', default = sys.stdout,
                        type = argparse.FileType('w'))
    parser.add_argument('-a','--show-all', help='Show all results for each compound (ie, not just QA failures)',
                        action = 'store_true', default = False)    
    parser.add_argument('-O','--outcomes-only', help='Show outcome for each QA calculation instead of a more detailed message containing values.',
                        action = 'store_true', default = False)    
    parser.add_argument('-c','--compound-id', help='Show results for this compound id only.',
                        metavar = 'NUMBER', type = int, default = None)
    
def action(args):
    qadata = qa_from_csv(qafile)
    matrix = read_matrix(matrix_file)

    if args.infile.lower().endswith('.xml'):
        controls, sample_groups = group_samples(args.infile)
    else:
        with open(args.infile) as f:
            controls, sample_groups = json.load(f)        

    style = 'screen' if args.outfile == sys.stdout else 'file'
            
    # controls
    # retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in controls.values())
    # display_qa_results(retvals, args.outfile, args.show_all)

    # other specimens
    if args.compound_id:
        cond = lambda c: c['COMPOUND_id'] == args.compound_id
    else:
        cond = lambda c: True
        
    compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']])
                 for c in flatten(sample_groups.values()) if cond(c)]     
    display_specimens(compounds,
                      outfile = args.outfile,
                      message = not args.outcomes_only,
                      style = style)
    
            
if __name__ == '__main__':
    main()
    
