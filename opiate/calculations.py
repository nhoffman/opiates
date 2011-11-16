import pprint
from itertools import chain
import logging

log = logging.getLogger(__name__)

from __init__ import SAMPLE_NAMES
from containers import Compound

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

    Should never return None.
    """
    
    retval = cmpnd.PEAK_signoise > cmpnd.signoise_stda
    return retval
    
def check_amr(cmpnd):
    """
    Check AMR

    Compare Drug Concentration with Drug QA Concentration Range

    Return None if cmpnd.PEAK_analconc is None or 0
    """    

    if cmpnd.PEAK_analconc == 0 or cmpnd.PEAK_analconc is None:
        return None
    else:
        return  cmpnd.amr_low <= cmpnd.PEAK_analconc <= cmpnd.amr_high

def check_amr_low(cmpnd):
    """
    AMR Lower Limit

    Compare Drug Concentration with lower limit of Drug QA Concentration Range

    Return None if cmpnd.PEAK_analconc is None or 0
    """    

    if cmpnd.PEAK_analconc == 0 or cmpnd.PEAK_analconc is None:
        return None
    else:
        return  cmpnd.amr_low <= cmpnd.PEAK_analconc

def check_rrt(cmpnd):
    """
    RRT test

    Compare Drug Relative Retention Time with Relative Retention Time QA

    Return None if cmpnd.PEAK_foundrrt is None
    """

    if cmpnd.PEAK_foundrrt is None:
        return None
    else:
        return cmpnd.rel_reten_low <= cmpnd.PEAK_foundrrt <= cmpnd.rel_reten_high

def check_signoise(cmpnd):
    """
    S/N test

    Compare Drug signal to noise (S/N) ratio with QA Range    

    Return None if cmpnd.PEAK_signoise is None.
    """

    retval = cmpnd.PEAK_signoise > cmpnd.signoise
    return retval
    
def check_ion_rato(cmpnd):
    """
    Ion Ratio Test

    Compare Drug Ion Ratio (Quatifying Peak Area/ Qualifying Peak
    Area) to a QA range. If the denominator is zero, return None.

    Return None if cmpnd.CONFIRMATIONIONPEAK1_area is 0 or missing.
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

    Compare and report metabolites that have no deuterated internal standard.

    Somone will need to clarify this one.
    """

    return None
    
def perform_qa(sample, qadata, matrix = None):
    """
    * qadata - dict containing QA values for each compound
    * sample - a list of dicts, each containing experimental
      results for a compound
    * matrix - dict with keys (sample_id, compound_id) returning a
      set of calculation names. If None, apply all calculations defined in `calculations.all_checks`.
    """
    
    results = []
    for compound in sample:        
        # 'sample_prep' is added by `parsers.group_specimens()` - is
        # this value is defined, use it in place of SAMPLE_id
        sample_id = compound.get('sample_prep') or compound['SAMPLE_id']
        compound_id = compound['COMPOUND_id']
        cmpnd = Compound(compound, **qadata[compound_id])

        if matrix:
            testnames = matrix.get((sample_id, compound_id), [])
        else:
            testnames = all_checks.keys()
            
        for testname in testnames:
            retval = globals()[testname](cmpnd)
            results.append((cmpnd, testname, retval))

    return results

def description(fun):
    return fun.__doc__.strip().split('\n', 1)[0]

all_checks = dict((name, {'description': description(fun), 'function': fun}) for name, fun in globals().items() if name.startswith('check_'))

