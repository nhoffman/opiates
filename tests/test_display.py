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
from opiate.parsers import qa_from_csv, read_matrix, get_samples
from opiate.display import display_specimens, display_results
from opiate.containers import Compound
from opiate.utils import flatten

import __init__ as config
from __init__ import TestCaseSuppressOutput

qadata = qa_from_csv(qafile)
matrix = read_matrix(matrix_file)
with open('testfiles/oct24.json') as f:
    controls, sample_groups = json.load(f)

class TestDisplayQA(TestCaseSuppressOutput):
    
    def test01(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(sample_groups.values())]     
        display_specimens(compounds, sys.stdout)

    def test02(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(sample_groups.values())]     
        display_specimens(compounds, sys.stdout, message = False)
        
class TestDisplayResults(TestCaseSuppressOutput):
    samples = list(get_samples(controls, sample_groups, qadata, matrix))

    def test01(self):
        display_results(self.samples, sys.stdout)

    def test02(self):
        display_results(self.samples, sys.stdout, style = 'file')

    def test03(self):
        display_results(self.samples, sys.stdout, grouped = False)
        
