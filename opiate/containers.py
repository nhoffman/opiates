from itertools import chain

# a=x10, b=spike_x10, c=straight, d=spiked
SAMPLE_NAMES = ['straight10','spiked10','straight','spiked']

class Compound(object):
    """
    Container class for a compound plus QA values.
    """

    defaults = (
        ('COMPOUND_id', 0),
        ('COMPOUND_name', 'undefined')
        )
    
    def __init__(self, experiment = None, qa = None):        

        experiment = experiment or {}
        qa = qa or {}

        for k,v in Compound.defaults:
            setattr(self, k, v)
        
        for k,v in chain.from_iterable([qa.items(), experiment.items()]):
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)
        
    def __repr__(self, ):
        return '<Compound "%(COMPOUND_name)s" id=%(COMPOUND_id)s>' % self
        
class Sample(object):
    """
    Container class for a collection of Compound objects. Calculations
    are implemented as methods of subclasses of this base Class.

    `sample_types` is a list of strings naming each element of
    `samples`; each element in `samples` will be defined as an
    attribute of `self`, as will any additional samples provided in
    `**kargs`. Each element of `samples` (and each value in
    `**kwargs`) is a dict that will be used to initialize an onject of
    class `Compound`.
    """

    def __init__(self, sample_names, samples, **kwargs):
        
        pass
