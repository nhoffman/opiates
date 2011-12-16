from itertools import chain, groupby

import pprint
import sys
import csv

from opiate import CONTROL_NAMES
from opiate.calculations import all_checks, fmt
from opiate.containers import Compound

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
            first = label_group.next()

            # display the first in the group of specimens from this
            # accession
            d = first.display(message)
            writer.writerow(dict((k, fmt(d.get(k))) for k in display_fields))

            # ...and maybe the rest
            if not first.type == 'patient' or not first.qa_ok or show_all:
                for cmpnd in label_group: 
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
            
