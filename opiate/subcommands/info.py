"""List contents of an XML file."""

import logging
from os import path
import xml.etree.ElementTree
import csv
from collections import OrderedDict

from opiate.parsers import get_rows

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    parser.add_argument('-s','--samples', help='list id and description of each sample',
                        action = 'store_true', default = False)
    parser.add_argument('-c','--compounds', help='list id and name of each compound',
                        action = 'store_true', default = False)

    
def action(args):

    rows = get_rows(args.infile)
    
    if args.samples:
        d = OrderedDict((row['SAMPLE_id'], row['SAMPLE_desc']) for row in rows)
        for i, desc in d.items():
            print i, desc
    elif args.compounds:
        d = OrderedDict((row['COMPOUND_id'], row['COMPOUND_name']) for row in rows)
        for i, desc in d.items():
            print i, desc
    else:
        print 'Found %s samples' % len(set(row['SAMPLE_id'] for row in rows))

if __name__ == '__main__':
    main()
    
