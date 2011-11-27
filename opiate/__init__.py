from os import path

def _safeint(s):
    try:
        return int(s)
    except ValueError:
        return s

from _sha import _sha
    
__version__ = "0.1" + _sha
__version_info__ = tuple([_safeint(num) for num in __version__.split('.')])

qafile = path.join(path.dirname(__file__), 'data', 'qa.csv')
matrix_file = path.join(path.dirname(__file__), 'data', 'matrix.csv')

SAMPLE_ATTRS = (
    ('SAMPLE_id', int),
    ('SAMPLE_desc', str),
    # ('SAMPLE_vial', str),
    ('COMPOUND_id', int),
    ('COMPOUND_name', str),
    ('PEAK_foundrrt', float),
    ('PEAK_signoise', float),
    ('PEAK_analconc', float),
    ('PEAK_area', float),
    ('CONFIRMATIONIONPEAK1_area', float),
    ('ISPEAK_area', float)
    )

# first element corresponds to SAMPLE_id
CONTROL_NAMES = (
    (1, 'stdA'),
    (2, 'stdB'),
    (3, 'stdC'),
    (4, 'stdD'),
    (5, 'stdE'),
    (6, 'low'),
    (7, 'high'),
    (8, 'add50'),
    (9, 'neg'),
    (10, 'neg_spiked')
    )

# a=x10, b=spike_x10, c=straight, d=spiked
SAMPLE_PREP_NAMES = ['straight10','spiked10','straight','spiked']

# will be assigned to cmpnd.sample_prep
SAMPLE_PREP_LABELS = ['a','b','c','d']

# define the order in which samples are shown in each group of four -
# will be assigned to cmpnd.sample_order
SAMPLE_PREP_ORDER = [2, 3, 1, 4]
