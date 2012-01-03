"""Describe an XML file."""

import logging
from os import path
import xml.etree.ElementTree
import csv
from collections import OrderedDict

from opiate.parsers import get_input
from opiate.display import list_grouped_samples

log = logging.getLogger(__name__)

def build_parser(parser):
    parser.add_argument('infile', help='XML file')
    
def action(args):
    controls, sample_groups = get_input(args.infile)
    list_grouped_samples(controls, sample_groups)

    
