"""
Test container classes
"""

import os
import unittest
import logging
import pprint

import __init__ as config
from opiates.containers import Compound

log = logging.getLogger(__name__)

class TestCompound(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test01(self):
        print 'hi'
        
