"""
Test functions in opiate.display.
"""

import os
import unittest
import logging
import pprint
import sys
import json
from itertools import chain

log = logging.getLogger(__name__)

from opiate import qafile, matrix_file
from opiate.calculations import all_checks
from opiate.parsers import qa_from_csv, read_matrix
from opiate.display import display_specimen_qa
from opiate.containers import Compound, flatten

import __init__ as config
from __init__ import TestCaseSuppressOutput

qadata = qa_from_csv(qafile)
with open('testfiles/oct24.json') as f:
    controls, sample_groups = json.load(f)

matrix = read_matrix(matrix_file)

class TestDisplayQA(TestCaseSuppressOutput):
    
    def test01(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(sample_groups.values())]     
        display_specimen_qa(compounds, sys.stdout)
