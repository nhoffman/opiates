from os import path

def _safeint(s):
    try:
        return int(s)
    except ValueError:
        return s

__version__ = "0.1"
__version_info__ = tuple([_safeint(num) for num in __version__.split('.')])

qafile = path.join(path.dirname(__file__), 'data/qa.csv')

# a=x10, b=spike_x10, c=straight, d=spiked
SAMPLE_NAMES = ['straight10','spiked10','straight','spiked']

