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

from opiate.calculations import calculate
from opiate.containers import Compound
from opiate.parsers import qa_from_csv
from opiate import qafile

import __init__ as config

## test data
# default qa values for this package
qadata = qa_from_csv(qafile)

with open('testfiles/oct24.json') as f:
    standards, sample_groups = json.load(f)
expt_stda = standards['stdA']

class TestCalculate(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
    
    def test01(self):
        calculate(tests = ['check_nothing'],
                  samples = sample_groups['A00001'],
                  standards = standards,
                  qadata = qadata                  
                  )
        
