"""Collect results from multiple runs into a single file."""

from collections import OrderedDict
from itertools import chain, ifilter, count
from os import path

import pprint
import argparse
import csv
import json
import logging
import sys
import xml.etree.ElementTree

from opiate import CONTROL_NAMES, COMPOUND_CODES
from opiate import __version__, matrix_file, qafile
from opiate.parsers import qa_from_csv, read_matrix, get_input, get_samples
from opiate.display import display_results
from opiate.utils import flatten, get_outfile
from opiate.calculations import add_ion_ratios
from opiate import subcommands

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infiles', nargs='+', help = 'one or more input data files (xml or json format).')
    parser.add_argument('-o', '--outfile', help = 'output file (csv format)', default = sys.stdout)
    subcommands.add_no_calculate_ion_ratio_avg(parser)    
    subcommands.add_split_desc(parser)
    parser.add_argument('-k', '--keep-phi', action = 'store_true', default = False)

def sanitize(d):
    """
    POS   --> 1
    FAIL  --> NA
    ''    --> 0
    >1000 --> 1000
    """
    for k,v in d.items():
        val = v.strip('>') if isinstance(v, str) else v
        d[k] = {'POS': 1, 'FAIL': 'NA'}.get(val, val) or 0

    return d
            
def action(args):
    matrix = read_matrix(matrix_file)
    qadata = qa_from_csv(qafile)
    compound_ids, compound_codes = map(list, zip(*COMPOUND_CODES))

    writer = csv.DictWriter(
        args.outfile if hasattr(args.outfile, 'write') else open(args.outfile, 'w'),
        fieldnames = ['infile','label'] + compound_ids,
        extrasaction = 'ignore')

    # create headers for the first row
    d = dict(label = 'label', infile = 'infile')
    d.update(dict(COMPOUND_CODES))
    writer.writerow(d)

    counter = count(1)
    for infile in args.infiles:    
        d = dict(infile = infile)
        controls, sample_groups = get_input(infile, split_description = args.split_desc)
        if args.calculate_ion_ratios:
            qadata = add_ion_ratios(qadata.copy(), controls)

        patient_samples = get_samples(controls, sample_groups, qadata, matrix, quantitative = True)
        for samples in patient_samples:
            d['label'] = samples[0].row_label() if args.keep_phi else counter.next()
            d.update(dict((s.COMPOUND_id, s.result) for s in samples))
            writer.writerow(sanitize(d))

            

        

