"""
Test container classes
"""

import os
from os import path
import unittest
import logging
import pprint
import json
log = logging.getLogger(__name__)

from opiate.containers import Compound, Sample
from opiate.parsers import qa_from_csv
from opiate import qafile
qadata = qa_from_csv(qafile)

import __init__ as config

with open('testfiles/oct24.json') as f:
    standards1, sample_groups1 = json.load(f)

class TestCompound(unittest.TestCase):

    def setUp(self):
        self.funcname = '_'.join(self.id().split('.')[-2:])

    def tearDown(self):
        pass
    
    def test01(self):
        cpnd = Compound(qa = {'meh':'buh'})
        self.assertTrue(cpnd.meh == 'buh')

    def test02(self):
        cpnd = Compound(experiment = {}, qa = {})
        defaults = dict(Compound.defaults)
        self.assertTrue(cpnd.COMPOUND_id == defaults['COMPOUND_id'])
        self.assertTrue(cpnd.COMPOUND_name == defaults['COMPOUND_name'])        
        
    def test03(self):
        cpnd = Compound(experiment = standards1['stdA'][0], qa = {})
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')        

    def test04(self):
        experiment = standards1['stdA'][0]
        #pprint.pprint(qadata)
        
        cpnd = Compound(experiment = standards1['stdA'][0], qa = {})
        self.assertTrue(cpnd.COMPOUND_id == 1)
        self.assertTrue(cpnd.COMPOUND_name == 'Morphine')        
        
