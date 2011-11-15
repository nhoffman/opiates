import pprint
from itertools import chain
import logging

log = logging.getLogger(__name__)

from __init__ import SAMPLE_NAMES
from containers import Compound

#matrix = 

def _check_true(cmpnd):
    return True

def _check_false(cmpnd):
    return False

def _check_none(cmpnd):
    return None

def check_stda_signoise(cmpnd):
    """
    Std A S/N test

    Compare Drug S/N with Drug QA S/N    
    """

    cmpnd.PEAK_signoise > cmpnd.signoise_stda
    
def check_amr(cmpnd):
    """
    AMR Test

    Compare Drug Concentration with Drug QA Concentration Range
    """    
    
    retval = cmpnd.amr_low <= cmpnd.PEAK_analconc <= cmpnd.amr_high
    return retval

def check_rrt(cmpnd):
    """
    RRT test

    Compare Drug Relative Retention Time with Relative Retention Time QA
    """

    retval = cmpnd.rel_reten_low <= cmpnd.PEAK_foundrrt <= cmpnd.rel_reten_high
    return retval

def check_signoise(cmpnd):
    """
    S/N test

    Compare Drug signal to noise (S/N) ratio with QA Range    
    """

    retval = cmpnd.PEAK_signoise > cmpnd.signoise
    return retval
    
def check_ion_rato(cmpnd):
    """
    Ion Ratio Test

    Compare Drug Ion Ratio (Quatifying Peak Area/ Qualifying Peak
    Area) to a QA range. If the denominator is zero, return None.
    """

    try:
        ratio = cmpnd.PEAK_area/cmpnd.CONFIRMATIONIONPEAK1_area
    except ZeroDivisionError:
        ratio = None
        
    retval = cmpnd.ion_ratio_low <= ratio <= cmpnd.ion_ratio_high    
    return retval

def check_is_peak_area(cmpnd):
    """
    I.S. Peak Area Test

    Compare Drug Internal Standard Peak Area with QA Peak Area
    """

    retval = cmpnd.ISPEAK_area > cmpnd.int_std_peak_area    
    return retval

def check_spike(cmpnd):
    """
    Spike Test

    Compare and report metabolites that have no deuterated internal standard

    Somone will need to clarify this one.
    """

    return None
    
def calculate(tests, sample, qadata):
    """
    * tests - list of function names to apply
    * samples - a list of dicts containing experimental results
    * qadata - dict containing QA values for each compound
    """

    results = []
    for compound in sample:
        compound_id = compound['COMPOUND_id']
        qa = qadata[compound_id]
        for testname in tests:
            fun = globals()[testname]
            retval = fun(Compound(compound, **qa))
            results.append((compound_id, testname, retval))

    return results

all_checks = dict((name,fun) for name, fun in globals().items() if name.startswith('check_'))

