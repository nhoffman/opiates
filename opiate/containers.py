from itertools import chain
from collections import OrderedDict

from __init__ import CONTROL_NAMES
control_ids = set(i for i,n in CONTROL_NAMES)
outcomes = {True: 'ok', False: 'FAIL', None: '-'}

import calculations
from calculations import all_checks

class Compound(object):
    """
    Container class for a compound plus QA values.
    """

    display_headers = (
        ('cmpnd','COMPOUND_name'),
        ('cmpnd_id','COMPOUND_id'),        
        ('sample','SAMPLE_desc'),
        ('sample_id','SAMPLE_id'),        
        ('conc','PEAK_analconc')
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
        elif self.get('sample_prep'):
            self.type = 'patient'
        else:
            self.type = 'misc'

        # define testnames; 'sample_prep' is added by
        # `parsers.group_samples()` - if this value is defined, use it
        # in place of SAMPLE_id
        sample_id = self.get('sample_prep') or self.SAMPLE_id
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
            
    def __repr__(self):
        return '<Cpnd %s %s Smpl %s %s (%s)>' % (
            self.COMPOUND_id,
            self.COMPOUND_name[:10] + '...',
            self.SAMPLE_id,
            self.get('sample_prep') or '',
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
        """

        # testname: (retval, msg)
        self.qa_results = OrderedDict(
            (test, getattr(calculations, test)(self)) for test in self.testnames)
        self.qa_ok = all(retval is not False for retval, msg in self.qa_results.values())

    def print_qa(self):
        for k,v in self.qa_results.items():
            print k, v

    def sort_by_compound(self):
        """
        Emit a tuple to sort a list of Compound objects depending on
        type.
        """

        if self.type == 'patient':
            return (self.COMPOUND_id, self.sample_label, self.sample_order)
        elif self.type == 'misc':
            return (self.COMPOUND_id, self.sample_label, self.SAMPLE_id)
        elif self.type == 'control':
            return (self.COMPOUND_id, self.SAMPLE_id)

        
    def display(self, message = True):
        """
        Return an OrderedDict containing values to display in the
        final report.
        """

        d = OrderedDict((k, self.__dict__[a]) for k,a in self.display_headers)

        for calc_name, results in self.qa_results.items():                   
            retval, msg = results
            if message:
                # show messages, but only if retval is False
                d[calc_name] = msg if retval is False else None
            else:
                d[calc_name] = outcomes[retval]
        
        return d
        
class Sample(object):
    """
    Container class for a collection of Compound objects. Calculations
    are implemented as methods of subclasses of this base Class.

    `sample_types` is a list of strings naming each element of
    `samples`; each element in `samples` will be defined as an
    attribute of `self`, as will any additional samples provided in
    `**kargs`. Each element of `samples` (and each value in
    `**kwargs`) is a dict that will be used to initialize an object of
    class `Compound`.
    """

    def __init__(self, sample_names, samples, **kwargs):
        
        pass

