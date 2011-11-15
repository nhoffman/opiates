from os import path

def _safeint(s):
    try:
        return int(s)
    except ValueError:
        return s

__version__ = "0.1"
__version_info__ = tuple([_safeint(num) for num in __version__.split('.')])

qafile = path.join(path.dirname(__file__), 'data', 'qa.csv')
matrix_file = path.join(path.dirname(__file__), 'data', 'control_matrix.csv')

# a=x10, b=spike_x10, c=straight, d=spiked
SAMPLE_NAMES = ['straight10','spiked10','straight','spiked']

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

