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

from opiate.calculations import *
from opiate.containers import Compound
from opiate.parsers import qa_from_csv, read_matrix
from opiate import qafile, matrix_file, CONTROL_NAMES

import __init__ as config

qadata = qa_from_csv(qafile)
with open('testfiles/oct24.json') as f:
    controls, sample_groups = json.load(f)

matrix = read_matrix(matrix_file)

class Cmpnd(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __repr__(self):
        return str(self.__dict__)

    def get(self, key, default = None):
        return self.__dict__.get(key, default)
    
class TestCalculations(unittest.TestCase):
    
    def _testall(self, checkfun, trials):
        for kwargs, predicted in trials:
            log.debug('in: %s --> %s...' % (str(kwargs), predicted))
            retval, msg = checkfun(Cmpnd(**kwargs))
            log.debug('out: %s --> %s' % (msg, retval))
            self.assertTrue(retval is predicted)
            self.assertTrue(bool(msg))
            
    def test_stda_signoise(self):
        trials = [
            (dict(PEAK_signoise = 0.5, signoise_stda = 0.1), True),
            (dict(PEAK_signoise = 1, signoise_stda = 5), False),
            (dict(PEAK_signoise = None, signoise_stda = 5), False),
            (dict(PEAK_signoise = 0, signoise_stda = 5), False)
            ]
        self._testall(check_stda_signoise, trials)

    # def test_amr(self):
    #     trials = [
    #         (dict(PEAK_analconc = 0.3, amr_low = 0.1, amr_high = 0.5), True),
    #         (dict(PEAK_analconc = 1, amr_low = 0.1, amr_high = 0.5), False),
    #         (dict(PEAK_analconc = None, amr_low = 0.1, amr_high = 0.5), None),
    #         (dict(PEAK_analconc = 0, amr_low = 0.1, amr_high = 0.5), None)
    #         ]
    #     self._testall(check_amr, trials)
        
    # def test_amr_low(self):
    #     trials = [
    #         (dict(PEAK_analconc = 0.3, amr_low = 0.1), True),
    #         (dict(PEAK_analconc = 0.1, amr_low = 1), False),
    #         (dict(PEAK_analconc = None, amr_low = 0.1), None),
    #         (dict(PEAK_analconc = 0, amr_low = 0.1), None)
    #         ]
    #     self._testall(check_amr_low, trials)

    def test_rrt(self):
        trials = [
            (dict(PEAK_foundrrt = 0.3, rel_reten_low = 0.1, rel_reten_high = 0.5), True),
            (dict(PEAK_foundrrt = 1, rel_reten_low = 0.1, rel_reten_high = 0.5), False),
            (dict(PEAK_foundrrt = None, rel_reten_low = 0.1, rel_reten_high = 0.5), None),
            (dict(PEAK_foundrrt = 0, rel_reten_low = 0.1, rel_reten_high = 0.5), None)
            ]
        self._testall(check_rrt, trials)
        
    def test_signoise(self):
        trials = [
            (dict(PEAK_signoise = 0.3, PEAK_analconc = 1, signoise = 0.1), True),
            (dict(PEAK_signoise = 0.1, PEAK_analconc = 1, signoise = 1), False),
            (dict(PEAK_signoise = None, PEAK_analconc = 1, signoise = 0.1), None),
            (dict(PEAK_signoise = 0, PEAK_analconc = 1, signoise = 0.1), False),
            (dict(PEAK_signoise = 0, PEAK_analconc = None, signoise = 0.1), None),
            (dict(PEAK_signoise = 0, PEAK_analconc = 0, signoise = 0.1), None)
            ]
        self._testall(check_signoise, trials)

    def test_ion_ratio(self):
        trials = [
            (dict(PEAK_area = 1., CONFIRMATIONIONPEAK1_area = 1.,
                  ion_ratio_avg = 1, ion_ratio_cv = 0.1), True),
            (dict(PEAK_area = 1., CONFIRMATIONIONPEAK1_area = 2.,
                  ion_ratio_avg = 1, ion_ratio_cv = 0.1), False),
            (dict(PEAK_area = 0, CONFIRMATIONIONPEAK1_area = 2.,
                  ion_ratio_avg = 1, ion_ratio_cv = 0.1), False),
            (dict(PEAK_area = 1., CONFIRMATIONIONPEAK1_area = 0,
                  ion_ratio_avg = 1, ion_ratio_cv = 0.1), False),
            (dict(PEAK_area = 1., CONFIRMATIONIONPEAK1_area = 2,
                  ion_ratio_avg_calc = 1.1, ion_ratio_cv = 0.1), False),
            
            ]
        self._testall(check_ion_ratio, trials)

    def test_is_peak_area(self):
        trials = [
            (dict(ISPEAK_area = 0.3, int_std_peak_area = 0.1, PEAK_analconc = 1, amr_low = 2), True),
            (dict(ISPEAK_area = 0, int_std_peak_area = 0.1, PEAK_analconc = 1, amr_low = 2), False),
            (dict(ISPEAK_area = 0.3, int_std_peak_area = 0.1, PEAK_analconc = None, amr_low = 2), True),
            (dict(ISPEAK_area = 0, int_std_peak_area = 0.1, PEAK_analconc = None, amr_low = 2), False),
            (dict(ISPEAK_area = None, int_std_peak_area = 0.1, PEAK_analconc = 1, amr_low = 2), False),
            (dict(ISPEAK_area = 0.3, int_std_peak_area = 0.1, PEAK_analconc = 3, amr_low = 2), None),
            (dict(ISPEAK_area = 0, int_std_peak_area = 0.1, PEAK_analconc = 3, amr_low = 2), None)
            ]
        self._testall(check_is_peak_area, trials)

    def test_spike(self):
        trials = [
            (dict(PEAK_analconc = 0.3, spike_low = 0.1), True),
            (dict(PEAK_analconc = 0, spike_low = 0.1), False),
            (dict(PEAK_analconc = None, spike_low = 0.1), False),
            ]
        self._testall(check_spike, trials)
        
class TestMeanIonRatios(unittest.TestCase):

    def test01(self):
        ratios = mean_ion_ratios(controls, set([1,2,3,4,5]))
        self.assertEqual(len(ratios), len(qadata))

