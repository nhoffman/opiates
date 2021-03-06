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
from itertools import groupby

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

# type 'misc'
misc_sample = sample_groups['Accession01']

# type 'patient'
patient_sample = sample_groups['Accession02']
compound1 = patient_sample[0]
        
class TestCompound(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
            
    def test01(self):
        cmpnd = Compound(expt_stda[0])
        self.assertTrue(cmpnd.COMPOUND_id == 1)
        self.assertTrue(cmpnd.COMPOUND_name == 'Morphine')

    def test02(self):
        data = expt_stda[0]
        cmpnd = Compound(data, **qadata[data['COMPOUND_id']])
        self.assertTrue(cmpnd.COMPOUND_id == 1)
        self.assertTrue(cmpnd.COMPOUND_name == 'Morphine')

        # qa_id and qa_compound defined in qadata
        self.assertTrue(cmpnd.qa_id == 1)
        self.assertTrue(cmpnd.qa_compound == 'Morphine')
        self.assertTrue(cmpnd.testnames == set())
        self.assertTrue(cmpnd.qa_results == OrderedDict())
        
    def test03(self):
        cmpnd = Compound(dict(SAMPLE_id = 1,
                             COMPOUND_id = 1,
                             COMPOUND_name = 'whatever',
                             PEAK_analconc = 10))
        self.assertEqual(cmpnd.type, 'control')
        self.assertEqual(cmpnd.peak_analconc_x10, None)
                
        cmpnd = Compound(dict(SAMPLE_id = 11,
                             COMPOUND_id = 1,
                             COMPOUND_name = 'whatever',
                             PEAK_analconc = 10))
        self.assertEqual(cmpnd.type, 'misc')
        self.assertEqual(cmpnd.peak_analconc_x10, None)
        
        cmpnd = Compound(dict(SAMPLE_id = 11,
                             COMPOUND_id = 1,
                             COMPOUND_name = 'whatever',
                             sample_prep_label = 'a',
                             PEAK_analconc = 10))
        self.assertEqual(cmpnd.type, 'patient')
        self.assertEqual(cmpnd.peak_analconc_x10, 100)        
        
        
class TestQACalculation(unittest.TestCase):

    def test01(self):
        compound = compound1[0]
        cmpnd = Compound(compound, **qadata[compound['COMPOUND_id']])
        self.assertTrue(cmpnd.qa_ok is None)

    def test02(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(controls.values())]
        self.assertTrue(all(x.type == 'control' for x in compounds))

    def test03(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(compound1)]
        self.assertTrue(all(x.type == 'patient' for x in compounds))

class TestSample(unittest.TestCase):
    
    def test01(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(patient_sample)]
        compounds.sort(key = lambda c: c.sort_by_patient())
        for cmpnd_id, cmpnds in groupby(compounds, lambda c: c.COMPOUND_id):
            sample = Sample(cmpnds)
            self.assertEqual(cmpnd_id, sample.COMPOUND_id)
            self.assertEqual(sample.type, 'patient')

    def test02(self):
        compounds = [Compound(c, matrix, **qadata[c['COMPOUND_id']]) for c in flatten(misc_sample)]
        compounds.sort(key = lambda c: c.sort_by_patient())
        for cmpnd_id, cmpnds in groupby(compounds, lambda c: c.COMPOUND_id):
            self.assertRaises(TypeError, Sample, cmpnds)


