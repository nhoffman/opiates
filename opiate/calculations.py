import pprint
from itertools import chain, ifilter, groupby
import logging
from collections import OrderedDict, defaultdict
from __init__ import CONTROL_NAMES

from utils import flatten

log = logging.getLogger(__name__)

def _check_true(cmpnd):
    return True

def _check_false(cmpnd):
    return False

def _check_none(cmpnd):
    return None

def fmt(*args):
    return tuple('%.2f' % val if isinstance(val, float) else val for val in args)
    
def check_stda_signoise(cmpnd):
    """
    StdA S/N

    Compare Drug S/N with Drug QA S/N

    Missing values are treated as 0.
    """

    retval = (cmpnd.PEAK_signoise or 0) > cmpnd.signoise_stda
    msg = '%s > %s' % fmt(cmpnd.PEAK_signoise, cmpnd.signoise_stda)

    return retval, msg
    
def check_amr(cmpnd):
    """
    AMR

    Compare Drug Concentration with Drug QA Concentration Range

    Return None if cmpnd.PEAK_analconc is None or 0
    """    

    if cmpnd.PEAK_analconc == 0 or cmpnd.PEAK_analconc is None:
        retval = None
    else:
        retval = cmpnd.amr_low <= cmpnd.PEAK_analconc <= cmpnd.amr_high

    msg = '%s [%s-%s]' % fmt(cmpnd.PEAK_analconc, cmpnd.amr_low, cmpnd.amr_high)

    return retval, msg

def check_amr_low(cmpnd):
    """
    AMR Low

    Compare Drug Concentration with lower limit of Drug QA Concentration Range

    Return None if cmpnd.PEAK_analconc is None or 0
    """    

    if cmpnd.PEAK_analconc == 0 or cmpnd.PEAK_analconc is None:
        retval = None
    else:
        retval = cmpnd.amr_low <= cmpnd.PEAK_analconc

    msg = '%s <= %s' % fmt(cmpnd.amr_low, cmpnd.PEAK_analconc)

    return retval, msg
    
def check_rrt(cmpnd):
    """
    RRT

    Compare Drug Relative Retention Time with Relative Retention Time QA

    Return None if cmpnd.PEAK_foundrrt is None
    """
    
    if cmpnd.PEAK_foundrrt is None or cmpnd.PEAK_foundrrt == 0:
        retval = None
    else:
        retval = cmpnd.rel_reten_low <= cmpnd.PEAK_foundrrt <= cmpnd.rel_reten_high

    msg = '%s [%s-%s]' % fmt(cmpnd.PEAK_foundrrt, cmpnd.rel_reten_low, cmpnd.rel_reten_high)

    return retval, msg
    
def check_signoise(cmpnd):
    """
    S/N

    Compare Drug signal to noise (S/N) ratio with QA Range    

    Return None if cmpnd.PEAK_signoise is None.

    TODO: Should this test fail if cmpnd.PEAK_signoise == 0?
    """
    
    if cmpnd.PEAK_signoise is None or not cmpnd.PEAK_analconc:
        retval = None
    else:
        retval = cmpnd.PEAK_signoise > cmpnd.signoise

    msg = '%s > %s' % fmt(cmpnd.PEAK_signoise, cmpnd.signoise)

    return retval, msg
        
def check_ion_ratio(cmpnd):
    """
    Ion Ratio

    Compare Drug Ion Ratio (Quatifying Peak Area/ Qualifying Peak
    Area) to a QA range. If the denominator is zero, return None.

    Return None if cmpnd.CONFIRMATIONIONPEAK1_area is 0 or missing.
    """

    # calculate reference range
    delta = cmpnd.ion_ratio_average * cmpnd.ion_ratio_cv
    ion_ratio_low = cmpnd.ion_ratio_average - delta
    ion_ratio_high = cmpnd.ion_ratio_average + delta

    if not cmpnd.CONFIRMATIONIONPEAK1_area:
        ion_ratio = None
        retval = None
    else:
        ion_ratio = cmpnd.PEAK_area/cmpnd.CONFIRMATIONIONPEAK1_area
        retval = ion_ratio_low <= ion_ratio <= ion_ratio_high

    msg = '%s [%s-%s]' % \
        fmt(ion_ratio, ion_ratio_low, ion_ratio_high)
        
    return retval, msg
        
def check_is_peak_area(cmpnd):
    """
    I.S. Pk Area

    Compare Drug Internal Standard Peak Area with QA Peak Area
    """
    
    retval = (cmpnd.ISPEAK_area or 0) > cmpnd.int_std_peak_area
    msg = '%s > %s' % fmt(cmpnd.ISPEAK_area, cmpnd.int_std_peak_area)
    return retval, msg
    
def check_spike(cmpnd):
    """
    Spike

    Compare and report metabolites that have no deuterated internal standard.
    """

    retval = (cmpnd.PEAK_analconc or 0) >= cmpnd.spike_low
    msg = '%s >= %s' % fmt(cmpnd.PEAK_analconc, cmpnd.spike_low)
    return retval, msg
    
def description(fun):
    return fun.__doc__.strip().split('\n', 1)[0]

all_checks = OrderedDict(sorted((name, description(fun)) for
                                name, fun in globals().items()
                                if name.startswith('check_')))

def mean_ion_ratios(controls, sample_ids):
    """
    Calculate the mean ion ratio for all compounds for each of the
    specimens included in `sample_ids`.

    `controls` is the first element of the tuple returned by
    `parsers.group_samples` and is an OrderedDict where
    controls.values() is a list of lists of dicts.

    Return a dict keyed by
    compound id containing the the calculated values.
    """
    
    stds = ifilter(lambda c: c['SAMPLE_id'] in sample_ids,
                   flatten(controls.values()))
    stds = sorted(list(stds),
                  key = lambda c: (c['COMPOUND_id'],c['SAMPLE_id']))

    cnames = dict(CONTROL_NAMES)
    
    out = OrderedDict()
    for cmpnd, cmpnd_grp in groupby(stds, lambda c: c['COMPOUND_id']):
        out[cmpnd] = OrderedDict(
            (cnames[c['SAMPLE_id']], ion_ratio(c)) for c in cmpnd_grp)
        out[cmpnd]['ion_ratio_average_calc'] = average(out[cmpnd].values())

    return out
                
def ion_ratio(cmpnd):
    if not cmpnd['CONFIRMATIONIONPEAK1_area']:
        return None
    else:
        return cmpnd['PEAK_area']/float(cmpnd['CONFIRMATIONIONPEAK1_area'])

def average(seq):
    noneless = filter(lambda x: x is not None, seq)
    return sum(noneless)/len(noneless) if noneless else None
    
