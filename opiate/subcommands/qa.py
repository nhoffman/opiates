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
from opiate.parsers import qa_from_csv, read_matrix, group_samples, add_ion_ratios
from opiate.display import display_specimens, display_controls
from opiate.containers import Compound
from opiate.utils import flatten

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='Input xml or json file containing experimental data.')
    parser.add_argument('-o','--outfile', metavar = 'FILE', default = sys.stdout,
                        type = argparse.FileType('w'))
    parser.add_argument('-a','--show-all', help='Show all results for each compound (ie, not just QA failures)',
                        action = 'store_true', default = False)    
    parser.add_argument('-O','--outcomes-only',
                        help="""Show outcome for each QA calculation
    instead of a more detailed message containing values.""",
                        action = 'store_true', default = False)    
    parser.add_argument('-c','--compound-id', help='Show results for this compound id only.',
                        metavar = 'NUMBER', type = int, default = None)
    parser.add_argument('-n','-no-calculate-ion-ratio-avg', help="""By
    default, ion ratio averages are calculated from the standards;
    providing this option causes QA to be performed using
    'ion_ratio_avg' from the qa configuration file.""",
                        action = 'store_false', dest = 'calculate_ion_ratios', default = True)    
    
    
def action(args):

    style = 'screen' if args.outfile == sys.stdout else 'file'
    
    if args.infile.lower().endswith('.xml'):
        controls, sample_groups = group_samples(args.infile)
    else:
        with open(args.infile) as f:
            controls, sample_groups = json.load(f)        

    qadata = qa_from_csv(qafile)
    matrix = read_matrix(matrix_file)

    if args.calculate_ion_ratios:
        qadata = add_ion_ratios(qadata, controls)
        log.info('calculating ion ratio averages from experimental data.')

    # if a single compound is specified, define lambda cond to use as
    # a filter
    if args.compound_id:
        cond = lambda c: c['COMPOUND_id'] == args.compound_id
    else:
        cond = lambda c: True
    
    # controls
    compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']])
                 for c in flatten(controls.values()) if cond(c)]     

    display_controls(compounds,
                     outfile = args.outfile,
                     message = not args.outcomes_only,
                     style = style)

    compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']])
                 for c in flatten(sample_groups.values()) if cond(c)]     
    display_specimens(compounds,
                      outfile = args.outfile,
                      message = not args.outcomes_only,
                      style = style)
    
            
if __name__ == '__main__':
    main()
    
