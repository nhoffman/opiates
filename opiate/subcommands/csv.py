"""Extract contents of an XML file into CSV format."""

import subprocess
import tempfile
import logging
import shutil
import os
from os import path

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', 
        help='XML file')
    parser.add_argument('-o','--outfile', 
        help='Output file in CSV format; output is named according to infile if not provided.')

def action(args):

    infile = args.infile
    outfile = args.outfile or path.basename(infile).replace('.xml','.csv')

    qafile = sys.argv[2]

    qadata = qa_from_csv(qafile)

    tree = xml.etree.ElementTree.ElementTree(file=infile)
    samples = tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')

    compound_names = qadata.keys()
    rows = chain.from_iterable(parse_sample(sample, compound_names) for sample in samples)

    headers, _ = zip(*sample_attrs)
    with open(outfile,'w') as f:
        writer = csv.DictWriter(f, fieldnames = headers, quoting = csv.QUOTE_NONNUMERIC)
        writer.writerow({k:k for k in headers})
        writer.writerows(rows)

if __name__ == '__main__':
    main()
    
