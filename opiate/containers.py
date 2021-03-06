import sys
import pprint
from itertools import chain
from collections import OrderedDict
import logging

log = logging.getLogger(__name__)

from __init__ import CONTROL_NAMES, SAMPLE_PREP_NAMES
control_ids = set(i for i,n in CONTROL_NAMES)
outcomes = {True: 'ok', False: 'FAIL', None: '-'}

import calculations
from calculations import all_checks, results

class QaFailure(Exception):
    pass

class Compound(object):
    """
    Container class for a compound plus QA values.
    """

    # display_headers provide the (column name, attribute) for the qa
    # reports
    display_headers = (
        ('cmpnd_id','COMPOUND_id'),
        ('cmpnd','COMPOUND_name'),
        ('sample_id','SAMPLE_id'),
        ('sample','SAMPLE_desc'),
        ('sample_prep','sample_prep_name'),
        ('conc','PEAK_analconc'),
        ('conc_x10','peak_analconc_x10')
        )

    def __init__(self, experiment, matrix = None, testnames = None, **kwargs):
        """
        Initialize the object with values in dict `experiment` and
        additional values in **kwargs. QA calculations are performed
        if a list of calculations is provided via either `matrix` or
        `testnames`.

         * experiment - a dict providing experimental results with keys in opiate.SAMPLE_ATTRS
         * matrix - a dict with keys (sample_id, compound_id) returning a list of
           testnames
         * testnames - provides a list of calculation names in the
           absence of matrix.
         * **kwargs - should provide other values used in various calculations.

        The attribute `self.type` is set as one of
        'control','patient', or 'misc'.

        Example:

        >>> from opiate.parsers import qa_from_csv, read_matrix
        >>> qadata = qa_from_csv(qafile)
        >>> matrix = read_matrix(matrix_file)
        >>> compound = {u'COMPOUND_id': 1,
         u'COMPOUND_name': u'Morphine',
         u'CONFIRMATIONIONPEAK1_area': 3783.097,
         u'ISPEAK_area': 16837.574,
         u'PEAK_analconc': 10.0928668309,
         u'PEAK_area': 5260.104,
         u'PEAK_foundrrt': 1.0140000582,
         u'PEAK_signoise': 300.1793138859,
         u'SAMPLE_desc': u'StdA',
         u'SAMPLE_id': 1}
        >>> cmpnd = Compound(compound, matrix, **qadata[compound['COMPOUND_id']]
        """

        self.__dict__ = dict(chain(*[experiment.items(), kwargs.items()]))

        if self.SAMPLE_id in control_ids:
            self.type = 'control'
        elif self.get('sample_prep_label'):
            self.type = 'patient'
        else:
            self.type = 'misc'

        # define testnames; 'sample_prep_label' is added by
        # `parsers.group_samples()` - if this value is defined, use it
        # in place of SAMPLE_id
        sample_id = self.get('sample_prep_label') or self.SAMPLE_id
        compound_id = self.COMPOUND_id

        if testnames:
            self.testnames = set(testnames)
        elif matrix:
            self.testnames = matrix.get((sample_id, compound_id), []) if matrix else all_checks.keys()
        else:
            self.testnames = set()

        if self.testnames:
            self.perform_qa()
        else:
            self.qa_results = OrderedDict()
            self.qa_ok = None

        # set attributes using "_get_" methods
        for attr in ['peak_analconc_x10']:
            val = getattr(self, '_get_'+attr)()
            setattr(self, attr, val)
            
    # We need to calculate some additional values from existing
    # ones. The methods below starting with '_get_' determine whether
    # the named attribute should be defined and perform the necessary
    # calculation. TODO: consider hooking attributes to getters so
    # that they can be calculated lazily.
    def _get_peak_analconc_x10(self):
        cond = self.type == 'patient' \
            and self.sample_prep_label in ('a','b') \
            and self.PEAK_analconc

        return (self.PEAK_analconc * 10) if cond else None

    def __repr__(self):
        return '<Cpnd %02i %s Smpl %s %s (%s)>' % (
            self.COMPOUND_id,
            (self.COMPOUND_name[:10] + '...') if len(self.COMPOUND_name) > 10 else self.COMPOUND_name,
            self.SAMPLE_id,
            self.get('sample_prep_label') or '',
            self.type
            )

    def items(self):
        return self.__dict__.items()

    def get(self, key, default = None):
        return self.__dict__.get(key, default)

    def perform_qa(self):
        """
        Perform QA calculations for list of calculations defined in
        `self.testnames` using experimental values associated with
        this instance and store results in `self.qa_results`, an
        OrderedDict keyed by testname and returning `(retval,
        msg)`. Also defines `self.qa_ok` with a value of True (all
        checks pass) or False (at least one test fails).

        `self.malformed` will be given a value of True in if there are
        any missing data elements in the input.
        """
        
        # testname: (retval, msg)
        try:
            self.qa_results = OrderedDict(
                (test, getattr(calculations, test)(self)) for test in self.testnames)
            self.qa_ok = all(retval is not False for retval, msg in self.qa_results.values())            
            self.malformed = False
        except AttributeError, msg:
            log.warning(msg)
            log.warning(self)
            all_tests = [test for test in dir(calculations) if test.startswith('check_')]
            self.qa_results = OrderedDict((test, (False, 'CHECK INTEGRATION')) for test in all_tests)
            self.qa_ok = False
            self.malformed = True
            
    def print_qa(self):
        for k,v in self.qa_results.items():
            print k, v

    def check_qa_error(self, name):
        """
        Raise QaFailure if the outcome of the qa calculation
        identified by 'name' (one of the columns of matrix.csv with
        the leading 'check_' removed) is False.
        """

        if self.qa_results.get('check_'+name, (None, None))[0] is False:
            raise QaFailure(name)

    def check_qa(self, test_names):
        """
        Return True if the outcome of the qa calculation identified by
        each `test_name` (one of the columns of matrix.csv with the
        leading 'check_' removed) is not False.
        """

        d = self.qa_results
        results = [d.get('check_'+name, (None, None))[0] for name in test_names]
        return all([r is not False for r in results])
        
    def sort_by_compound(self):
        """
        Emit a tuple to sort a list of Compound objects by compound id
        depending on type.
        """

        if self.type == 'patient':
            return (self.COMPOUND_id, self.sample_label, self.sample_prep_order)
        elif self.type == 'misc':
            return (self.COMPOUND_id, self.sample_label, self.SAMPLE_id)
        elif self.type == 'control':
            return (self.COMPOUND_id, self.SAMPLE_id)

    def sort_by_patient(self):
        """
        Emit a tuple to sort a list of Compound objects by specimen
        label depending on type.
        """

        return (self.sample_index, self.COMPOUND_id, self.sample_prep_order)

    def display(self, message = True):
        """
        Return an OrderedDict containing values to display in the
        final report.
        """

        # d = OrderedDict((k, self.__dict__[a]) for k,a in self.display_headers)
        d = OrderedDict((k, self.__dict__.get(a, None)) for k,a in self.display_headers)

        for calc_name, results in self.qa_results.items():
            retval, msg = results
            if message:
                # show messages, but only if retval is False
                # (explicitly check for False here, since values may
                # also be None)
                d[calc_name] = msg if retval is False else None
            else:
                d[calc_name] = outcomes[retval]

        return d

    def show_for_qa(self):
        """
        Return True if this compound should be displayed in QA report.
        """

        labels_to_show = set(['a','c'])
        if self.type == 'patient' and self.sample_prep_label in labels_to_show:
            # we always show the "a", "c" rows in each group of
            # patient specimens
            show = True
        elif not self.qa_ok:
            show = True
        else:
            show = False

        return show

    def show_for_results(self):
        """
        Return True if this compound should be displayed in results report.
        """

        labels_to_show = set(['a','c'])
        if self.type == 'patient':
            show = self.sample_prep_label in labels_to_show
        elif self.type == 'misc':
            show = True
        else:
            show = False

        return show

class Sample(object):
    """
    Container class for a group of Compound objects. Logic for
    display of results is implemented here.
    """

    def __init__(self, compounds, calculate_results = True, quantitative = False):


        """
         * quantitative - if False, return POS for positive glucuronides and < amr_low when below amr
        """
        
        compounds = list(compounds)

        # ensure that this set of compounds are homogenous for certain
        # attributes
        for attr in ['COMPOUND_id', 'COMPOUND_name', 'sample_label', 'type']:
            self.__dict__[attr] = getattr(compounds[0], attr)
            assert len(set(getattr(c, attr) for c in compounds)) == 1

        if compounds[0].type != 'patient':
            raise TypeError('Sample object requires compounds of type "patient"')
        self.compounds = OrderedDict((c.sample_prep_name, c) for c in compounds)

        self.abbrev_name = (self.COMPOUND_name[:10] + '...') if len(self.COMPOUND_name) > 10 else self.COMPOUND_name

        # these abbreviations are used in several calculations
        self.a = self.compounds['straight10']
        self.c = self.compounds['straight']

        # calculate results
        self.result = results(self, quantitative) if calculate_results else []
                        
    def __repr__(self):
        return '<Sample %(sample_label)s %(abbrev_name)s (%(type)s)>' % \
            self

    def __getitem__(self, key):
        return self.__dict__[key]

    def row_label(self):
        """
        Return a label to identify sample in the results.
        """

        return self.compounds['straight'].SAMPLE_desc
        
    def get(self, key, default = None):
        return self.__dict__.get(key, default)

