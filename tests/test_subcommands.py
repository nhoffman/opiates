"""
Test subcommands.
"""

import os
import unittest
import logging
import pprint
import sys

import opiate.subcommands.config as config_subcommand
from opiate.subcommands.config import action as config_action
from opiate.subcommands.info import action as info_action

from opiate.scripts.smack import main as smack

from __init__ import TestCaseSuppressOutput
import __init__ as config
log = logging.getLogger(__name__)

class Args(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def __getattr__(self, key):        
        return self.data.get(key)

class TestConfig(TestCaseSuppressOutput):
    subcommand = config_subcommand

    def test_exits(self):
        self.assertRaises(SystemExit, smack, ['config','-h'])
        self.assertRaises(SystemExit, smack, ['config','-i'])
        self.assertRaises(SystemExit, smack, ['config','-s'])        

    def test_options(self):
        options = [
            ['config','-C'],
            ['config','-c'],
            ['config','-f'],
            ['config','-i', '1'],
            ['config','-r'],
            ['config','-s', 'check_amr'],
            ]
        for opt in options:
            smack(opt)
                
class TestConfigOld(TestCaseSuppressOutput):

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
        self.assertRaises(SystemExit, config_action, Args(compound_id = 21))
        
class TestInfo(TestCaseSuppressOutput):

    def test01(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml'))

    def test02(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', samples = True))

    def test03(self):
        info_action(Args(infile = 'testfiles/opi_checkout.xml', compounds = True))
        
