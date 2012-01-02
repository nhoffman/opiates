"""
Test parsing of XML files and QA data.
"""

import os
import unittest
import logging
import pprint
import json
from collections import OrderedDict

from opiate.parsers import cast, cast_numeric, cast_vals, read_matrix, group_samples, qa_from_csv, add_ion_ratios, get_input
from opiate import matrix_file, qafile
import __init__ as config

log = logging.getLogger(__name__)

class TestCast(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test_cast_numeric(self):
        # int
        self.assertTrue(isinstance(cast_numeric('10'), int))
        self.assertFalse(isinstance(cast_numeric('10'), float))        
        self.assertEqual(cast_numeric('10'), 10)

        # float
        self.assertTrue(isinstance(cast_numeric('10.1'), float))        
        self.assertAlmostEqual(cast_numeric('10.1'), 10.1)

        # other
        self.assertTrue(cast_numeric('meh') is None)

class TestReadMatrix(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test01(self):
        matrix = read_matrix(matrix_file)

class TestGroupSamples(unittest.TestCase):

    def test01(self):
        controls, sample_groups = group_samples('testfiles/opi_checkout.xml')
        self.assertEqual(len(controls), 10)
        self.assertEqual(sample_groups, OrderedDict())

class TestAddIonRatios(unittest.TestCase):

    def test01(self):
        with open('testfiles/oct24.json') as f:
            controls, sample_groups = json.load(f)
        qadata = qa_from_csv(qafile)
        
        qd = add_ion_ratios(qadata, controls)
        for d in qd.values():
            self.assertTrue('ion_ratio_avg_calc' in d)
        
class TestGetInput(unittest.TestCase):

    def test01(self):
        controls, sample_groups = get_input(
            'testfiles/oct24.json')

    def test02(self):
        controls, sample_groups = get_input(
            'testfiles/opi_checkout.xml')
        
    def test03(self):
        self.assertRaises(SystemExit, get_input,
            'testfiles/oct24.json',
            format = 'xml')

    def test04(self):
        self.assertRaises(SystemExit, get_input,
            'testfiles/opi_checkout.xml',
            format = 'json')
