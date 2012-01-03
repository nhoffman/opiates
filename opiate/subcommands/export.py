"""Extract contents of an XML file into another format."""

import json
import logging

from opiate.parsers import get_input, remove_patient_info
from opiate import subcommands
from opiate.utils import get_outfile

log = logging.getLogger(__name__)

def build_parser(parser):
    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)
    subcommands.add_outdir(parser)    
    parser.add_argument(
        '-s','--sanitize', action = 'store_true',
        default = False,
        help = 'Remove PHI from patient samples.')
    
def action(args):

    fmt = 'json'

    samples = get_input(args.infile)
    if args.sanitize:
        samples = remove_patient_info(samples)            

    outfile = get_outfile(args, ext = fmt)    
    json.dump(samples, outfile, indent=4)
            
    
