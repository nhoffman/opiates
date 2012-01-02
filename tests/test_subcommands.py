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

class TestConfig(TestCaseSuppressOutput):
    
    def test_exits(self):
        options = [['-h'],
                   ['-i'],
                   ['-s']]

        for opt in options:               
            self.assertRaises(SystemExit, smack, ['config'] + opt)

    def test_options(self):
        options = [
            ['-C'],
            ['-c'],
            ['-f'],
            ['-i', '1'],
            ['-r'],
            ['-s', 'check_amr'],
            ]
        for opt in options:
            smack(['config'] + opt)
                
class TestInfo(TestCaseSuppressOutput):

    def test_options(self):

        infile = 'testfiles/oct24.json'
        options = [
            [infile]
            ]
        for opt in options:
            smack(['info'] + opt)
        

class TestQA(TestCaseSuppressOutput):
    
    def testExit01(self):
        self.assertRaises(SystemExit, smack, ['qa'])
            
    def test01(self):
        smack(['qa', 'testfiles/oct24.json', '-o', '-'])

    def test02(self):
        smack(['qa', 'testfiles/oct24.json', '-o', '-', '--compound-id', '1'])

    def test03(self):
        smack(['qa', 'testfiles/oct24.json', '-o', '-', '--compound-id', '1', '--outcomes-only'])
        

class TestResults(TestCaseSuppressOutput):
    
    def testExit01(self):
        self.assertRaises(SystemExit, smack, ['results'])
            
    def test01(self):
        smack(['results', 'testfiles/oct24.json', '-o', '-'])

    # def test02(self):
    #     smack(['qa', 'testfiles/oct24.json', '-o', '-', '--compound-id', '1'])

    # def test03(self):
    #     smack(['qa', 'testfiles/oct24.json', '-o', '-', '--compound-id', '1', '--outcomes-only'])
        
        
