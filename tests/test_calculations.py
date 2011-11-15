"""
Test container classes
"""

import os
from os import path
import unittest
import logging
import pprint
import json
log = logging.getLogger(__name__)

from opiate.calculations import perform_qa, all_checks
from opiate.containers import Compound
from opiate.parsers import qa_from_csv, read_matrix
from opiate import qafile, matrix_file

import __init__ as config

## test data
# default qa values for this package
qadata = qa_from_csv(qafile)

with open('testfiles/oct24.json') as f:
    standards, sample_groups = json.load(f)

matrix = read_matrix(matrix_file)

expt_stda = standards['stdA']

class TestPerformQA(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
    
    def test01(self):
        retvals = perform_qa(sample = standards['stdA'],
                             qadata = qadata,
                             matrix = matrix
                             )

        for r in retvals:
            print r
        
