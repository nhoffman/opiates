"""
Test utils module.
"""

import os
from os import path
import unittest
import logging
import pprint
import sys
import json

from opiate.utils import get_outfile, flatten, mkdir

from __init__ import TestBase
import __init__ as config
log = logging.getLogger(__name__)

with open('testfiles/oct24.json') as f:
    controls, sample_groups = json.load(f)

class Args(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestFlatten(unittest.TestCase):
    def test01(self):
        flat = flatten(sample_groups.values())
        self.assertTrue(all(isinstance(x, dict) for x in flat))

    def test02(self):
        flat = flatten(controls.values())
        self.assertTrue(all(isinstance(x, dict) for x in flat))

class TestGetOutfile(TestBase):

    def setUp(self):
        self.outdir = self.mkoutdir()
        self.infile = path.join(self.outdir, 'infile.txt')
        with open(self.infile, 'w') as f:
            f.write('buh\n')

    def tearDown(self):
        pass

    def test01(self):
        args = Args(infile = self.infile,
                    outfile = None,
                    outdir = None)

        outfile = get_outfile(args, label = 'qa')
        log.debug(outfile)
        
    def test02(self):
        args = Args(infile = self.infile,
                    outfile = path.join(self.outdir, 'outfile.csv'),
                    outdir = None)
        
        self.assertRaises(OSError, get_outfile, args, label = 'qa')
        
    def test03(self):
        args = Args(infile = self.infile,
                    outfile = open(path.join(self.outdir, 'outfile.csv'), 'w'),
                    outdir = None)

        outfile = get_outfile(args, label = 'qa')
        log.debug(outfile)

    def test04(self):
        outdir = mkdir(path.join(self.outdir, 'subdir'), clobber = True)
        args = Args(infile = self.infile,
                    outfile = None,
                    outdir = outdir)

        outfile = get_outfile(args, label = 'qa')
        log.debug(outfile)
        
    def test05(self):
        args = Args(infile = self.infile,
                    outfile = None,
                    outdir = None)

        outfile = get_outfile(args)
        log.debug(outfile)

    def test06(self):
        args = Args(infile = self.infile,
                    outfile = None,
                    outdir = None)

        outfile = get_outfile(args, include_version = False)
        log.debug(outfile)
        
    def test07(self):
        args = Args(infile = self.infile,
                    outfile = None,
                    outdir = None)
        
        self.assertRaises(OSError, get_outfile, args, ext = 'txt', include_version = False)

        
