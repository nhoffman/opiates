"""Show predefined QA values."""

from collections import OrderedDict
from itertools import chain
from os import path
import csv
import logging
import pprint
import sys
import xml.etree.ElementTree

from opiate import qafile
from opiate.parsers import qa_from_csv

log = logging.getLogger(__name__)

def build_parser(parser):    
    parser.add_argument('-i','--compound-id', help='show QA values for the compound with id=ID',
                        default = None, metavar = 'ID', type = int)
    parser.add_argument('-n','--names', help='list id and name of each compound',
                        action = 'store_true', default = False)
    parser.add_argument('-f','--qa-file', help='print the path of the QA file',
                        action = 'store_true', default = False)
    parser.add_argument('-r','--variables', help='print variable names (headers in QA file)',
                        action = 'store_true', default = False)

def action(args):
    qadata = qa_from_csv(qafile)
    
    if args.qa_file:
        print(path.abspath(qafile))
    elif args.variables:
        _, d = qadata.popitem()
        print('\n'.join(d.keys()))
    elif args.names:
        print('id\tname')
        for compound_id, d in qadata.items():
            print('\t'.join(['%i' % compound_id, d['qa_compound']]))
    elif args.compound_id:
        try:
            for k,v in qadata[args.compound_id].items():
                print('%s = %s' % (k,v))
        except KeyError:
            print('"%s" is not a valid compound id; try listing compounds using the "-n/--names" option' % args.compound_id)
            sys.exit(1)
            
if __name__ == '__main__':
    main()
    
