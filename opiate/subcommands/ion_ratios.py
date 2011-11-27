"""Calculate average Ion Ratios for each compound."""

from collections import OrderedDict
from itertools import chain, ifilter
from os import path

import argparse
import csv
import json
import logging
import sys
import pprint

from opiate import matrix_file, qafile, CONTROL_NAMES
from opiate.parsers import qa_from_csv, read_matrix, group_samples
from opiate.display import display_specimens, display_controls
from opiate.calculations import mean_ion_ratios

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='Input xml or json file containing experimental data.')
    parser.add_argument('-o','--outfile', metavar = 'FILE', default = sys.stdout,
                        type = argparse.FileType('w'))
    
def action(args):
    nullchar = '.' if args.outfile == sys.stdout else ''
    fmt = lambda s: '%.2f' % s if isinstance(s, float) else (s or nullchar)

    qadata = qa_from_csv(qafile)

    if args.infile.lower().endswith('.xml'):
        controls, sample_groups = group_samples(args.infile)
    else:
        with open(args.infile) as f:
            controls, sample_groups = json.load(f)        

    std_ids, std_names = zip(
        *[(i,n) for i,n in CONTROL_NAMES if n.startswith('std')])

    headers = ['qa_id', 'qa_compound'] + \
        list(std_names) + ['ion_ratio_avg_calc','ion_ratio_avg']
    writer = csv.DictWriter(args.outfile,
                            fieldnames = headers, extrasaction = 'ignore')

    ion_ratios = mean_ion_ratios(controls, set(std_ids))    
    for compound_id, d in ion_ratios.items():
        if compound_id == min(ion_ratios.keys()):
            writer.writerow(dict(zip(headers, headers)))
            
        d.update(qadata[compound_id])
        writer.writerow(dict((k, fmt(d.get(k))) for k in headers))

        
if __name__ == '__main__':
    main()
    
