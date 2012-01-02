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
from opiate.parsers import qa_from_csv, read_matrix, get_input, add_ion_ratios
from opiate.display import display_specimens, display_controls
from opiate.containers import Compound
from opiate.utils import flatten
from opiate import subcommands

log = logging.getLogger(__name__)

def build_parser(parser):

    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)
    subcommands.add_outdir(parser)
    subcommands.add_no_calculate_ion_ratio_avg(parser)    
    subcommands.add_split_desc(parser)
    parser.add_argument(
        '-a','--show-all',
        action = 'store_true', default = False,
        help = 'Show all results for each compound (ie, not just QA failures)')
    parser.add_argument(
        '-O','--outcomes-only',
        action = 'store_true', default = False,        
        help= """Show outcome for each QA calculation instead of a more
        detailed message containing values.""")
    parser.add_argument(
        '-c','--compound-id',
        metavar = 'NUMBER', type = int, default = None,
        help = 'Show results for this compound id only.')

def action(args):

    style = 'screen' if args.outfile == sys.stdout else 'file'

    if args.outfile is None:
        dirname, basename = path.split(args.infile)
        outfile = open(
            path.join(
                args.outdir or dirname,
                '.'.join([path.splitext(basename)[0], __version__, 'qa', 'csv'])
                ), 'w')
    else:
        outfile = args.outfile

    controls, sample_groups = get_input(args.infile, split_description = args.split_desc)

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

