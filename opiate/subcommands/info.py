"""List contents of an XML file."""

import logging
from os import path
import xml.etree.ElementTree
from itertools import chain
import csv
from collections import OrderedDict

from opiate import qafile
from opiate.parsers import qa_from_csv, sample_attrs, parse_sample

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    parser.add_argument('--samples', help='list id and description of each sample',
                        action = 'store_true', default = False)
    parser.add_argument('--compounds', help='list id and name of each compound',
                        action = 'store_true', default = False)

    
def action(args):

    infile = args.infile
    qadata = qa_from_csv(qafile)

    tree = xml.etree.ElementTree.ElementTree(file=infile)
    samples = tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')

    compound_names = qadata.keys()
    rows = chain.from_iterable(parse_sample(sample, compound_names) for sample in samples)

    if args.samples:
        d = OrderedDict((row['SAMPLE_id'], row['SAMPLE_desc']) for row in rows)
        for i, desc in d.items():
            print i, desc
    elif args.compounds:
        d = OrderedDict((row['COMPOUND_id'], row['COMPOUND_name']) for row in rows)
        for i, desc in d.items():
            print i, desc
        

if __name__ == '__main__':
    main()
    
