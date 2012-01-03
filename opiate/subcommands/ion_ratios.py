"""Calculate average Ion Ratios for each compound."""

import csv
import logging
import sys

from opiate import qafile, CONTROL_NAMES
from opiate.parsers import qa_from_csv, get_input
from opiate.utils import get_outfile
from opiate.calculations import mean_ion_ratios
from opiate import subcommands

log = logging.getLogger(__name__)

def build_parser(parser):
    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)
    subcommands.add_outdir(parser)

def action(args):
    nullchar = '.' if args.outfile == sys.stdout else ''
    fmt = lambda s: '%.2f' % s if isinstance(s, float) else (s or nullchar)

    controls, sample_groups = get_input(args.infile)    
    qadata = qa_from_csv(qafile)

    outfile = get_outfile(args, label = 'ion_ratios', ext = 'csv')
    
    std_ids, std_names = zip(
        *[(i,n) for i,n in CONTROL_NAMES if n.startswith('std')])

    headers = ['qa_id', 'qa_compound'] + \
        list(std_names) + ['ion_ratio_avg_calc', 'ion_ratio_avg']
    writer = csv.DictWriter(
        outfile, fieldnames = headers, extrasaction = 'ignore')

    ion_ratios = mean_ion_ratios(controls, set(std_ids))    
    for compound_id, d in ion_ratios.items():
        if compound_id == min(ion_ratios.keys()):
            writer.writerow(dict(zip(headers, headers)))
            
        d.update(qadata[compound_id])
        writer.writerow(dict((k, fmt(d.get(k))) for k in headers))

    
