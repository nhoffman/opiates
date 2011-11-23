from itertools import chain
import collections

class Compound(object):
    """
    Container class for a compound plus QA values.
    """
    
    def __init__(self, experiment, **kwargs):                
        self.__dict__ = dict(chain(*[experiment.items(), kwargs.items()]))
        
    def __repr__(self):
        """
        Uses any attributes starting with COMPOUND to identify
        instance.
        """
        
        return '<Cpnd %s %s Sample %s>' % (
            self.COMPOUND_id,
            self.COMPOUND_name,
            self.SAMPLE_id
            )

    def items(self):
        return self.__dict__.items()

    def get(self, key, default = None):
        return self.__dict__.get(key, default)
    
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
        if isinstance(el, collections.Iterable) and not (isinstance(el, basestring) or hasattr(el, 'get')):
            for sub in flatten(el):
                yield sub
        else:
            yield el    
