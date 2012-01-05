from itertools import chain, groupby, ifilter

import pprint
import sys
import csv

from opiate import CONTROL_NAMES, COMPOUND_CODES
from opiate.calculations import all_checks, fmt
from opiate.containers import Compound, Sample

choose_nullchar = {'screen':'.', 'file':''}
display_fields = [h for h,_ in Compound.display_headers] + all_checks.keys()
display_header = dict((k, all_checks.get(k,k)) for k in display_fields)
display_empty = dict((k,'') for k in display_fields)

def list_grouped_samples(controls, sample_groups):
    print '# Standards and Controls:'
    for k, v in controls.items():
        print '%s\t%s' % (v[0]['SAMPLE_id'], k)

    print '# Other specimens:'
    for label, grp in sample_groups.items():
        print '# %s (%s specimens)' % (label, len(grp))
        for sample in grp:
            print '%s\t%s' % (sample[0]['SAMPLE_id'], sample[0]['SAMPLE_desc'])

def display_specimens(compounds, outfile, show_all = False, message = True, style = 'screen'):

    nullchar = choose_nullchar[style]
    fmt = lambda s: '%.2f' % s if isinstance(s, float) else (s or nullchar)
    writer = csv.DictWriter(outfile, fieldnames = display_fields)

    if style == 'file':
        writer.writerow(display_header)

    # sort, then group by compound
    compounds.sort(key = lambda c: c.sort_by_compound())

    for compound_id, compound_group in groupby(compounds, lambda c: c.COMPOUND_id):
        if style == 'screen':
            writer.writerow(display_header)
        # within each compound, group by label
        for label, label_group in groupby(compound_group, lambda c: c.sample_label):
            # the 'show_for_qa' method should provide the logic for
            # whether to display each compound
            for cmpnd in label_group:
                if show_all or cmpnd.show_for_qa():
                    d = cmpnd.display(message)
                    writer.writerow(dict((k, fmt(d.get(k))) for k in display_fields))

            if style == 'screen':
                writer.writerow(display_empty)


def display_controls(compounds, outfile, show_all = False, message = True, style = 'screen'):

    nullchar = choose_nullchar[style]
    fmt = lambda s: '%.2f' % s if isinstance(s, float) else (s or nullchar)
    writer = csv.DictWriter(outfile, fieldnames = display_fields)

    if style == 'file':
        writer.writerow(display_header)

    # sort, then group by compound
    compounds.sort(key = lambda c: c.sort_by_compound())
    for compound_id, compound_group in groupby(compounds, lambda c: c.COMPOUND_id):
        grp = list(compound_group)
        show_group = any(c.qa_ok is False for c in grp) or show_all

        if show_group and style == 'screen':
            writer.writerow(display_header)

        for cmpnd in grp:
            if cmpnd.qa_ok is False or show_all:
                d = cmpnd.display(message)
                writer.writerow(dict((k, fmt(d.get(k))) for k in display_fields))

        if show_group and style == 'screen':
            writer.writerow(display_empty)
                
def display_results(compounds, outfile, style = 'screen'):

    """
For the resulting, we would like the compounds to be divided in three worksheets: worksheet 1: compound_ids 1-7, worksheet 2: compound_ids 8-14, worksheet 3: compound ids 15-20.

If c > amr_high, calculate the result from a by multiplying by 10
When a > amr_high, report >10,000
When c < amr_low, report <10

-Use whole numbers, except for fentanyl (compound_id 11) use 2 decimal places.
    """

    fieldnames, labels = zip(*COMPOUND_CODES)
          
    nullchar = choose_nullchar[style]
    fmt = lambda s: '%.2f' % s if isinstance(s, float) else (s or nullchar)

    keys = ['label'] + list(fieldnames)

    rows = []
    d = dict(label = 'label')
    d.update(dict(COMPOUND_CODES))
    rows.append(d)
    
    # sort, then group by accession
    compounds.sort(key = lambda c: c.sort_by_patient())
    patient_compounds = ifilter(lambda c: c.type == 'patient', compounds)
    for sample_label, sample_group in groupby(patient_compounds, lambda c: c.sample_label):
        # ... then group by compound and initialize a Sample for each group
        samples = [Sample(grp) for _, grp in groupby(sample_group, lambda c: c.COMPOUND_id)]
        # d contains concentrations keyed by compound_id
        d = dict(zip(keys, [sample_label] + [fmt(s.conc()) for s in samples]))
        rows.append(d)
            

    writer = csv.DictWriter(outfile,
                            fieldnames = keys,
                            extrasaction = 'ignore')

    for d in rows:
        writer.writerow(d)
