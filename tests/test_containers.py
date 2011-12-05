"""
Test container classes
"""

import os
from os import path
import unittest
import logging
import pprint
import json
from collections import OrderedDict

log = logging.getLogger(__name__)

from opiate.containers import Compound, Sample
from opiate.utils import flatten
from opiate.parsers import qa_from_csv, read_matrix
from opiate import qafile, matrix_file

import __init__ as config

## test data
# default qa values for this package
qadata = qa_from_csv(qafile)
matrix = read_matrix(matrix_file)

with open('testfiles/oct24.json') as f:
    controls, sample_groups = json.load(f)
expt_stda = controls['stdA']
sample1 = sample_groups['Accession02'][0]

class TestFlatten(unittest.TestCase):
    def test01(self):
        flat = flatten(sample_groups.values())
        self.assertTrue(all(isinstance(x, dict) for x in flat))

    def test02(self):
        flat = flatten(controls.values())
        self.assertTrue(all(isinstance(x, dict) for x in flat))

        
class TestCompound(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
            
    def test01(self):
        cpnd = Compound(expt_stda[0])
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')

    def test02(self):
        data = expt_stda[0]
        cpnd = Compound(data, **qadata[data['COMPOUND_id']])
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')

        # qa_id and qa_compound defined in qadata
        self.assertTrue(cpnd.qa_id == 1)
        self.assertTrue(cpnd.qa_compound == 'Morphine')
        self.assertTrue(cpnd.testnames == set())
        self.assertTrue(cpnd.qa_results == OrderedDict())
        
class TestQACalculation(unittest.TestCase):

    def test01(self):
        compound = sample1[0]
        cmpnd = Compound(compound, **qadata[compound['COMPOUND_id']])
        self.assertTrue(cmpnd.qa_ok is None)

    def test02(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(controls.values())]
        self.assertTrue(all(x.type == 'control' for x in compounds))

    def test03(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(sample1)]
        self.assertTrue(all(x.type == 'patient' for x in compounds))
        
