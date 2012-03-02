"""Error-check input data."""

import logging
import pprint
import xml.etree.ElementTree

from opiate import __version__, matrix_file, qafile
from opiate.parsers import get_input, qa_from_csv, read_matrix, parse_sample
from opiate import subcommands
from opiate.utils import get_outfile

log = logging.getLogger(__name__)

def build_parser(parser):
    subcommands.add_infile(parser)
    subcommands.add_outfile(parser)
    subcommands.add_outdir(parser)    
    
def action(args):

    qadata = qa_from_csv(qafile)
    matrix = read_matrix(matrix_file)
    
    # first get an ungrouped list of samples
    tree = xml.etree.ElementTree.ElementTree(file=args.infile)
    compound_ids = [d['qa_id'] for d in qadata.values()]
    samples = [list(parse_sample(elem, compound_ids)) \
                   for elem in tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')]

    compound_keys = set(['COMPOUND_id', 'COMPOUND_name',
    'CONFIRMATIONIONPEAK1_area', 'ISPEAK_area', 'PEAK_analconc',
    'PEAK_area', 'PEAK_foundrrt', 'PEAK_signoise', 'SAMPLE_desc',
    'SAMPLE_id'])
    
    for sample in samples:
        descriptions = set(compound['SAMPLE_desc'] for compound in sample)
        assert len(descriptions) == 1
        desc = descriptions.pop() 

        # are all elements present?
        for compound in sample:
            if compound_keys - set(compound.keys()):
                print 'sample %(SAMPLE_desc)s compound %(COMPOUND_id)s is missing' % compound,
                print 'element(s)', ''.join(compound_keys - set(compound.keys()))
                
    # controls, sample_groups = get_input(args.infile)

    
    # control_elements = set([
    #         'COMPOUND_id',
    #         'ISPEAK_area',
    #         'PEAK_foundrrt',
    #         'SAMPLE_desc',
    #         'CONFIRMATIONIONPEAK1_area',
    #         'sample_index',
    #         'SAMPLE_id',
    #         'PEAK_signoise',
    #         'PEAK_analconc',
    #         'COMPOUND_name',
    #         'PEAK_area'
    #         ])
    
    # # for label, sample in controls.items():
    # #     print label
    # #     pprint.pprint(sample[0].keys())
    # #     break
            
    
    # for preparation, samples in sample_groups.items():
    #     print preparation

