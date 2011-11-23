"""
Test functions in opiate.display.
"""

import os
import unittest
import logging
import pprint
import sys
import json
from itertools import chain

log = logging.getLogger(__name__)

from opiate import qafile, matrix_file
from opiate.calculations import perform_qa, all_checks
from opiate.parsers import qa_from_csv, read_matrix
from opiate.display import display_sample_group
from opiate.containers import flatten

import __init__ as config
from __init__ import TestCaseSuppressOutput

qadata = qa_from_csv(qafile)
with open('testfiles/oct24.json') as f:
    standards, sample_groups = json.load(f)

matrix = read_matrix(matrix_file)

class TestDisplayQA(TestCaseSuppressOutput):
    
    def test01(self):
        retvals = chain.from_iterable(perform_qa(sample, qadata, matrix) for sample in standards.values())
        display_qa_results(retvals, sys.stdout)

    def test02(self):
        retvals = perform_qa(chain.from_iterable(sample_groups['A00001']), qadata, matrix)
        display_sample_group(retvals, sys.stdout, show_all = True, result = 'comment')

    def test03(self):
        retvals = perform_qa(chain.from_iterable(sample_groups['A00001']), qadata, matrix)
        display_sample_group(retvals, sys.stdout, show_all = False)

    def test04(self):
        retvals = perform_qa(chain.from_iterable(sample_groups['A00001']), qadata, matrix)
        display_sample_group(retvals, sys.stdout, show_all = False, result = 'comment')

    def test05(self):
        retvals = perform_qa(flatten(sample_groups.values()), qadata, matrix)
        display_sample_group(retvals, sys.stdout, show_all = False, result = 'outcome')
        

        
