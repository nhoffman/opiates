"""
Test subcommands.
"""

import os
import unittest
import logging
import pprint
import sys

from opiate.subcommands.config import action as config_action
from opiate.subcommands.info import action as info_action

import __init__ as config

log = logging.getLogger(__name__)

if log.getEffectiveLevel() >= logging.INFO:
    sys.stdout = open(os.devnull)

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

    def test01(self):
        config_action(Args())

    def test02(self):
        config_action(Args(names = True))

    def test03(self):
        config_action(Args(qa_file = True))

    def test04(self):
        config_action(Args(variables = True))

    def test05(self):
        config_action(Args(compound_id = 1))
        config_action(Args(compound_id = 21))
        
class TestInfo(unittest.TestCase):

    def setUp(self):        
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass

    def test01(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml'))

    def test02(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', samples = True))

    def test03(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', compounds = True))
        
