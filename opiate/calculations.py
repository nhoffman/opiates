from itertools import chain
from __init__ import SAMPLE_NAMES

def check_nothing():
    pass

def calculate(tests, samples, standards, qadata):
    """
    * tests - list of function names to apply
    * samples - list of four dicts containing experimental results
    * standards - a dict of dicts containing results for each standard
    * qadata - dict containing QA values for each compound
    """

    args = {}
    for name in SAMPLE_NAMES:
        args[name] = 1
    

    
