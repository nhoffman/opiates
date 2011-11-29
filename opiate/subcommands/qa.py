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

from opiate import __version__, matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, group_samples, add_ion_ratios
from opiate.display import display_specimens, display_controls
from opiate.containers import Compound
from opiate.utils import flatten

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='Input xml or json file containing experimental data.')
    parser.add_argument('-o','--outfile', metavar = 'FILE', default = None,
                        type = argparse.FileType('w'), help = """Output file in csv format. If this argument is not provided, the output file name will be generated from the input file name plus the version number. Use '-o -' or '--outfile=-' to print to the screen.""")
    parser.add_argument('-d','--outdir', metavar = 'DIRECTORY', default = None,
                        help = """Optional output directory. Writes to same directory as infile by default.""")
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

    if args.outfile is None:
        outdir = args.outdir or path.dirname(args.infile)
        outfile = open(
            path.join(
                outdir,
                '.'.join([path.splitext(path.basename(args.infile))[0], __version__, 'csv'])
                ), 'w')

    else:
        outfile = args.outfile
        
    if args.infile.lower().endswith('.xml'):
        controls, sample_groups = group_samples(args.infile)
    elif args.infile.lower().endswith('.json'):
        with open(args.infile) as f:
            controls, sample_groups = json.load(f)        
    else:
        log.error('input file name must end with either ".xml" or ".json"')
        sys.exit(1)
            
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
                     outfile = outfile,
                     show_all = args.show_all,
                     message = not args.outcomes_only,
                     style = style)

    compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']])
                 for c in flatten(sample_groups.values()) if cond(c)]     
    display_specimens(compounds,
                      outfile = outfile,
                     show_all = args.show_all,                      
                      message = not args.outcomes_only,
                      style = style)
    
    if args.outfile is None:
        outfile.close()

    
if __name__ == '__main__':
    main()
    
