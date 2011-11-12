from itertools import chain

class Compound(object):
    """
    Container class for a compound plus QA values.
    """

    def __init__(self, qadata = None, experiment = None):
        qadata = qadata or {}
        experiment = experiment or {}
        
        for k,v in chain.from_iterable([qadata.items(), experiment.items()]):
            setattr(self, k, v)
    
class Sample(object):
    """
    Class implementing calculations.
    """

    def __init__(self, a, b, c, d):
        
        pass
