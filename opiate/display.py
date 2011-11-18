from itertools import chain, groupby

import pprint
import sys
import csv

from opiate import CONTROL_NAMES
from opiate.calculations import all_checks
calc_names = dict((name, d['description']) for name, d in all_checks.items())

def list_grouped_samples(controls, sample_groups):
    print '# Standards and Controls:'
    for k, v in controls.items():
        print '%s\t%s' % (v[0]['SAMPLE_id'], k)
    print '# Other specimens:'
    for label, grp in sample_groups.items():
        print '# %s (%s specimens)' % (label, len(grp))
        for sample in grp:
            print '%s\t%s' % (sample[0]['SAMPLE_id'], sample[0]['SAMPLE_desc'])
    
def display_qa_results(results, outfile, show_all = False):
    """

     * results ...
     * outfile - file-like object open for writing 
    """
    controls = dict(CONTROL_NAMES)
    outcomes = {True: 'pass', False: '* FAIL *', None: 'not performed'}

    show = (lambda x: True) if show_all else (lambda x: x is False)

    # sort results by compound then by sample
    results = sorted(list(results), key = lambda r: (r[0].COMPOUND_id, r[0].SAMPLE_id))

    headers = ['compound','sample','concentration','test','result','commment']
    defaults = dict((k, '.') for k in headers)

    writer = csv.DictWriter(outfile, fieldnames = headers)
    
    def row(**args):
        d = defaults.copy()
        d.update(args)
        writer.writerow(d)

    row(**dict((k,k) for k in headers))
    for cmpnd_id_and_name, compound_group in groupby(results, lambda r: (r[0].COMPOUND_id, r[0].COMPOUND_name)):    
        row(compound = '%02i %s' % cmpnd_id_and_name)
        for sample_id, sample_group in groupby(compound_group, lambda r: r[0].SAMPLE_id):
            sample_group = list(sample_group)
            if any(show(r[-1]) for r in sample_group):
                row(sample = '%s %s' % (sample_id, controls.get(sample_id, '')),
                    concentration = '%.2f' % sample_group[0][0].PEAK_analconc)          
                for cmpnd, test, result in sample_group:
                    if show(result):
                        row(test = calc_names[test])
