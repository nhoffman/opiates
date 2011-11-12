"""Extract contents of an XML file into another format."""

from os import path
import csv
import json
import logging
import xml.etree.ElementTree

from opiate.parsers import sample_attrs, get_rows

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

    rows = get_rows(args.infile)

    headers, _ = zip(*sample_attrs)
    with open(outfile,'w') as f:
        if format == 'csv':
            writer = csv.DictWriter(f, fieldnames = headers, quoting = csv.QUOTE_NONNUMERIC)
            writer.writerow({k:k for k in headers})
            writer.writerows(rows)
        elif format == 'json':
            json.dump(list(rows), f, sort_keys=True, indent=4)
            
if __name__ == '__main__':
    main()
    
