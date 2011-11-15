"""
Test subcommands.
"""

import os
import unittest
import logging
import pprint

from opiate.subcommands.qa import action as qa_action
from opiate.subcommands.info import action as info_action

import __init__ as config

log = logging.getLogger(__name__)

class Args(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def __getattr__(self, key):        
        return self.data.get(key)
            
class TestQA(unittest.TestCase):

    def setUp(self):        
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test_01(self):
        qa_action(Args())

    def test_02(self):
        qa_action(Args(names = True))

    def test_03(self):
        qa_action(Args(qa_file = True))

    def test_04(self):
        qa_action(Args(variables = True))

    def test_05(self):
        qa_action(Args(compound_id = 1))
        qa_action(Args(compound_id = 21))
        
class TestInfo(unittest.TestCase):

    def setUp(self):        
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test_01(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml'))

    def test_02(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', samples = True))

    def test_03(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', compounds = True))
        
