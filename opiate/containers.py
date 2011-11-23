from itertools import chain
from collections import Iterable, OrderedDict

from __init__ import CONTROL_NAMES
control_ids = set(i for i,n in CONTROL_NAMES)

import calculations
from calculations import all_checks

class Compound(object):
    """
    Container class for a compound plus QA values.
    """
    
    def __init__(self, experiment, **kwargs):                
        """
        Initialize the object with values in dict `experiment` and
        additional values in **kwargs. `experiment` should provide
        values in opiate.SAMPLE_ATTRS and **kwargs should provide
        other values used in various calculations.

        The attribute `self.type` is set as one of
        'control','patient', or 'misc'.
        """

        self.__dict__ = dict(chain(*[experiment.items(), kwargs.items()]))

        if self.SAMPLE_id in control_ids:
            self.type = 'control'
        elif self.get('sample_prep'):
            self.type = 'patient'
        else:
            self.type = 'misc'
        
    def __repr__(self):
        return '<Cpnd %s %s Smpl %s (%s)>' % (
            self.COMPOUND_id,
            self.COMPOUND_name,
            self.SAMPLE_id,
            self.type
            )
    
    def items(self):
        return self.__dict__.items()

    def get(self, key, default = None):
        return self.__dict__.get(key, default)

    def perform_qa(self, matrix = None):
        """
        Given `matrix`, perform QA calculations using experimental
        values associated with this instance and store results in
        `self.qa_results`, an OrderedDict keyed by testname and
        returning `(retval, msg)`. `matrix` provides a list of
        testnames given (sample_id, compound_id); if `matrix` is not
        provided, all tests defined in the calculations module are
        performed.
        """

        # 'sample_prep' is added by `parsers.group_samples()` - if
        # this value is defined, use it in place of SAMPLE_id        
        sample_id = self.get('sample_prep') or self.SAMPLE_id
        compound_id = self.COMPOUND_id

        testnames = matrix.get((sample_id, compound_id), []) if matrix else all_checks.keys()        

        # testname: (retval, msg)
        self.qa_results = OrderedDict(
            (test, getattr(calculations, test)(self)) for test in testnames)
        self.qa_ok = all(retval is not False for retval, msg in self.qa_results.values())

    def print_qa(self):
        for k,v in self.qa_results.items():
            print k, v
        
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

def flatten(seq):
    """
    Poached from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    
    Don't flatten strings or dict-like objects.
    """
    for el in seq:
        if isinstance(el, Iterable) and not (isinstance(el, basestring) or hasattr(el, 'get')):
            for sub in flatten(el):
                yield sub
        else:
            yield el    
