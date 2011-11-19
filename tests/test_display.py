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
from opiate.display import display_qa_results

import __init__ as config
from __init__ import TestCaseSuppressOutput

qadata = qa_from_csv(qafile)
with open('testfiles/oct24.json') as f:
    standards, sample_groups = json.load(f)

matrix = read_matrix(matrix_file)
    
class TestDisplayQA(TestCaseSuppressOutput):
        
    def test01(self):
        retvals = chain.from_iterable([perform_qa(standards['stdA'], qadata, matrix),
                                       perform_qa(standards['high'], qadata, matrix)])

        display_qa_results(retvals, sys.stdout)

