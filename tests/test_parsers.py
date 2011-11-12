"""
Test parsing of XML files and QA data.
"""

import os
import unittest
import logging
import pprint

import __init__ as config

log = logging.getLogger(__name__)

class TestCast(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test01(self):
        print 'hi'
        
