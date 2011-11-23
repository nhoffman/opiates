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

from opiate.containers import Compound, Sample, flatten
from opiate.parsers import qa_from_csv
from opiate import qafile

import __init__ as config

## test data
# default qa values for this package
qadata = qa_from_csv(qafile)

with open('testfiles/oct24.json') as f:
    standards, sample_groups = json.load(f)
expt_stda = standards['stdA']

class TestFlatten(unittest.TestCase):
    def test01(self):
        flat = flatten(sample_groups.values())
        self.assertTrue(all(isinstance(x, dict) for x in flat))

class TestCompound(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
    
    def test01(self):
        # can initialize with arbitrary values
        cpnd = Compound({'meh':'buh'})
        self.assertTrue(cpnd.meh == 'buh')

    def test02(self):
        # arbitrary values in both `experiment` and `kwargs`
        cpnd = Compound({'meh':'buh'}, blee = 1)
        self.assertTrue(cpnd.meh == 'buh')
        self.assertTrue(cpnd.blee == 1)        
        
    def test03(self):
        cpnd = Compound(expt_stda[0])
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')

    def test04(self):
        data = expt_stda[0]
        cpnd = Compound(data, **qadata[data['COMPOUND_id']])
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')
        self.assertTrue(cpnd.qa_id == 1)
        self.assertTrue(cpnd.qa_compound == 'Morphine')
        
