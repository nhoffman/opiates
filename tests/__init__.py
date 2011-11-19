import sys
import logging
import os
import unittest

verbosity_flag = [x for x in sys.argv if x.startswith('-v')]
verbosity = (verbosity_flag[0] if verbosity_flag else '').count('v')

# loglevel = {
#     0: logging.ERROR,
#     1: logging.WARNING,
#     2: logging.INFO,
#     3: logging.DEBUG,
# }.get(verbosity, logging.DEBUG)

loglevel = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}.get(verbosity, logging.DEBUG)

if verbosity > 1:
    logformat = '%(levelname)s %(module)s %(lineno)s %(message)s'
else:
    logformat = '%(message)s'

# set up logging
logging.basicConfig(file=sys.stdout, format=logformat, level=loglevel)

log = logging.getLogger(__name__)

class TestCaseSuppressOutput(unittest.TestCase):

    def setUp(self):        
        self.funcname = '_'.join(self.id().split('.')[-2:])
        self.suppress_output = log.getEffectiveLevel() >= logging.INFO
        if self.suppress_output:
            sys.stdout = open(os.devnull, 'w')
            
    def tearDown(self):
        if self.suppress_output:
            sys.stdout = sys.__stdout__


