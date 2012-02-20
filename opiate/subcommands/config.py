"""Show predefined QA values and other configuration details."""

from collections import OrderedDict
from itertools import chain
from os import path
import csv
import logging
import pprint
import sys
import xml.etree.ElementTree
import inspect

from opiate import qafile, CONTROL_NAMES, COMPOUND_CODES
from opiate.parsers import qa_from_csv
from opiate import calculations
from opiate import calculations
from opiate.calculations import all_checks

log = logging.getLogger(__name__)

def build_parser(parser):    
    parser.add_argument('-C','--controls', help='list sample id and name of control samples', action = 'store_true', default = False)
    parser.add_argument('-c','--list-calculations', help='list names of calculations', action = 'store_true', default = False)
    parser.add_argument('-f','--qa-file', help='print the path of the QA file', action = 'store_true', default = False)
    parser.add_argument('-i','--compound-id', help='show QA values for the compound with id=ID', default = None, metavar = 'ID', type = int)
    parser.add_argument('-n','--names', help='list id and name of each compound', action = 'store_true', default = False)
    parser.add_argument('-r','--variables', help='print variable names (headers in QA file)', action = 'store_true', default = False)
    parser.add_argument('-s','--show-calculation', help='show a functions implementing a calculation specified by NAME', metavar = 'NAME', default = False)
    parser.add_argument('-a','--algorithm', help='Show the function for calculating results from a patient sample.', action = 'store_true', default = False)

    
def action(args):
    qadata = qa_from_csv(qafile)
    
    if args.qa_file:
        print(path.abspath(qafile))
    elif args.variables:
        _, d = qadata.popitem()
        print('\n'.join(d.keys()))
    elif args.names:
        cmpnd_codes = dict(COMPOUND_CODES)
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['id', 'code', 'name'])
        for compound_id, d in qadata.items():
            writer.writerow([compound_id,
                             cmpnd_codes[compound_id],
                             d['qa_compound']])
    elif args.compound_id:
        try:
            for k,v in qadata[args.compound_id].items():
                print('%s = %s' % (k,v))
        except KeyError:
            print('"%s" is not a valid compound id; try listing compounds using the "-n/--names" option' % args.compound_id)
            sys.exit(1)
    elif args.list_calculations:
        for name, description in all_checks.items():
            print '%-20s %s' % (name, description)
    elif args.show_calculation:
        fun = getattr(calculations, args.show_calculation)
        print ''.join(inspect.getsourcelines(fun)[0])
    elif args.controls:
        for row in CONTROL_NAMES:
            print '%s\t%s' % row
    elif args.algorithm:
        print ''.join(inspect.getsourcelines(calculations.results)[0])
