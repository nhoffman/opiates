from os.path import join, dirname

_data = join(dirname(__file__), 'data')
    
try:
    with open(join(_data, 'sha')) as s, open(join(_data, 'ver')) as v:
        sha = s.read().strip()
        ver = int(v.read())
except Exception, e:
    __version__ = ''
else:    
    __version__ = '%04i.%s' % (ver, sha)

qafile = join(_data, 'qa.csv')
matrix_file = join(_data, 'matrix.csv')

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

# will be assigned to cmpnd.sample_prep_label
SAMPLE_PREP_LABELS = ['a','b','c','d']

# define the order in which samples are shown in each group of four -
# will be assigned to cmpnd.sample_prep_order
SAMPLE_PREP_ORDER = [2, 3, 1, 4]

# (COMPOUND_id, lab_mnemonic)
COMPOUND_CODES = (
    (1, 'UMORPH'),
    (2, 'UOXYM'),
    (3, 'UHMOR'),
    (4, 'UCOD'),
    (5, 'UOXCD'),
    (6, 'UHCOD'),
    (7, 'UMOR6'),
    (8, 'UFENTM'),
    (9, 'UMPERM'),
    (10, 'UMPER'),
    (11, 'UFENT'),
    (12, 'UBUPR'),
    (13, 'UPPOX'),
    (14, 'UMETH'),
    (15, 'UMOR3G'),
    (16, 'UMOR6G'),
    (17, 'UHMORG'),
    (18, 'UOXYMG'),
    (19, 'UCOD6G'),
    (20, 'UNBUPG')
    )

