"""Extract contents of an XML file into another format."""

from os import path
import csv
import json
import logging
import xml.etree.ElementTree

from opiate import SAMPLE_ATTRS
from opiate.parsers import get_input, remove_patient_info
from opiate import subcommands

log = logging.getLogger(__name__)

def build_parser(parser):
    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)    
    parser.add_argument(
        '-s','--sanitize', action = 'store_true',
        default = False,
        help = 'Remove PHI from patient samples.')
    
def action(args):

    infile = args.infile
    format = args.format
    outfile = args.outfile or path.basename(infile).replace('.xml','.'+format)

    with open(outfile,'w') as f:
        samples = get_input(args.infile)
        if args.sanitize:
            samples = remove_patient_info(samples)            
        json.dump(samples, f, indent=4)
            
if __name__ == '__main__':
    main()
    
