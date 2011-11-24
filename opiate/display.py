from itertools import chain, groupby

import pprint
import sys
import csv

from opiate import CONTROL_NAMES
from opiate.calculations import all_checks, fmt

calc_names = dict((name, d['description']) for name, d in all_checks.items())
outcomes = {True: 'ok', False: 'FAIL', None: '-'}

def list_grouped_samples(controls, sample_groups):
    print '# Standards and Controls:'
    for k, v in controls.items():
        print '%s\t%s' % (v[0]['SAMPLE_id'], k)
    print '# Other specimens:'
    for label, grp in sample_groups.items():
        print '# %s (%s specimens)' % (label, len(grp))
        for sample in grp:
            print '%s\t%s' % (sample[0]['SAMPLE_id'], sample[0]['SAMPLE_desc'])

class Row(object):
    def __init__(self, outfile, headers, nullchar = '', **args):

        self.headers = headers
        self.defaults = dict((k, nullchar) for k in headers)
        self.writer = csv.DictWriter(outfile, fieldnames = headers, **args)

    def write(self, **args):
        d = self.defaults.copy()
        d.update(args)
        self.writer.writerow(d)

    def write_headers(self):
        self.write(**dict((k, calc_names.get(k) or k) for k in self.headers))
        
def display_controls(results, outfile, show_all = False, nullchar = '.'):
    """

     * results ...
     * outfile - file-like object open for writing
    """

    controls = dict(CONTROL_NAMES)
    outcomes = {True: 'ok', False: 'FAIL', None: '-'}

    show = (lambda result: True) if show_all else (lambda result: result is False)

    row = Row(outfile,
              headers = ['cmpnd_id','cmpnd','sample_id','sample','conc'] + all_checks.keys(),
              nullchar = nullchar)
    
    # sort results by compound then by sample
    results = sorted(list(results), key = lambda r: (r['cmpnd'].COMPOUND_id, r['cmpnd'].SAMPLE_id))

    # headers
    row.write_headers()
    for cmpnd_id, cmpnd_group in groupby(results, lambda r: r['cmpnd'].COMPOUND_id):
        for sample_id, sample_group in groupby(cmpnd_group, lambda r: r['cmpnd'].SAMPLE_id):
            sample_group = list(sample_group)

            if not any(show(r['result']) for r in sample_group):
                continue

            cmpnd = sample_group[0]['cmpnd']
            row.write(cmpnd = cmpnd.COMPOUND_name,
                cmpnd_id = cmpnd.COMPOUND_id,
                sample = cmpnd.SAMPLE_desc,
                sample_id = cmpnd.SAMPLE_id,
                conc = fmt(cmpnd.PEAK_analconc)[0] or nullchar,
                **{r['test']: outcomes[r['result']] for r in sample_group if show(r['result'])}
                )


def display_sample_group(results, outfile, show_all = False, nullchar = '.', result = 'outcome'):
    """

     * results ...
     * outfile - file-like object open for writing
     * result in ('outcome','comment')
    """

    assert result in ('outcome','comment')    
    show = (lambda result: True) if show_all else (lambda result: result is False)

    row = Row(outfile,
              headers = ['cmpnd_id','cmpnd','sample_id','sample','conc'] + all_checks.keys(),
              nullchar = nullchar)
    
    # sort results by compound then by sample - use 'sample_order' to
    # sort sample (added by `parsers.group_samples()`) if available,
    # otherwise use sample id
    results = sorted(list(results), key = lambda r: (
            r['cmpnd'].COMPOUND_id,  r['cmpnd'].get('sample_order') or r['cmpnd'].SAMPLE_id))

    # headers
    row.write_headers()
    for cmpnd_id, cmpnd_group in groupby(results, lambda r: r['cmpnd'].COMPOUND_id):
        for sample_id, sample_group in groupby(cmpnd_group, lambda r: r['cmpnd'].SAMPLE_id):
            sample_group = list(sample_group)

            if not any(show(r['result']) for r in sample_group):
                continue

            cmpnd = sample_group[0]['cmpnd']
                        
            if result == 'outcome':
                d = {r['test']: outcomes[r['result']] for r in sample_group if show(r['result'])}
            elif result == 'comment':
                d = {r['test']: r['comment'] if r['result'] is False else nullchar for r in sample_group if show(r['result'])}
            
            row.write(cmpnd = cmpnd.COMPOUND_name,
                      cmpnd_id = cmpnd.COMPOUND_id,
                      sample = cmpnd.SAMPLE_desc,
                      sample_id = cmpnd.SAMPLE_id,
                      conc = fmt(cmpnd.PEAK_analconc)[0] or 0.0,
                      **d
                      )

def display_specimen_qa(compounds, outfile, show_all = False, style = 'screen'):
    assert style in ('screen','file')

    # sort by compound
    compounds.sort(key = lambda c: c.sort_by_compound())

    # group by compound
    for compound_id, compound_group in groupby(compounds, lambda c: c.COMPOUND_id):
        # within each compound, group by label
        for label, label_group in groupby(compound_group, lambda c: c.sample_label):
            first = label_group.next()
            rest = list(label_group)
            if first.type == 'patient' and first.qa_ok:
                print first.summary_dict()
                
        
