"""
Test parsing of XML files and QA data.
"""

import os
import unittest
import logging
import pprint

from opiate.parsers import cast, cast_numeric, cast_vals, read_matrix
from opiate import matrix_file
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

        
