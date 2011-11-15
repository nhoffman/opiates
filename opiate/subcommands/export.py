"""Extract contents of an XML file into another format."""

from os import path
import csv
import json
import logging
import xml.etree.ElementTree

from opiate import SAMPLE_ATTRS
from opiate.parsers import get_rows, group_samples

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', 
        help='XML file')
    parser.add_argument('-o','--outfile', 
                        help="""Output file name; by default, output
                        is named according to infile (with appropriate
                        extension) and is written to the current
                        working directory.""")
    parser.add_argument('-f','--format', choices = ['csv','json'], default = 'csv',
                        help = 'Output format. Choices are %(choices)s'                        
                        )

def action(args):

    infile = args.infile
    format = args.format
    outfile = args.outfile or path.basename(infile).replace('.xml','.'+format)

    with open(outfile,'w') as f:
        if format == 'csv':
            headers, _ = zip(*SAMPLE_ATTRS)
            rows = get_rows(args.infile)
            writer = csv.DictWriter(f, fieldnames = headers, quoting = csv.QUOTE_NONNUMERIC)
            writer.writerow({k:k for k in headers})
            writer.writerows(rows)
        elif format == 'json':
            samples = group_samples(args.infile)
            json.dump(samples, f, indent=4)
            
if __name__ == '__main__':
    main()
    
