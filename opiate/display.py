from itertools import chain, groupby

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

def display_qa_results(results, show_all = False):

    outcomes = {True: 'pass', False: '*FAIL*', None: 'not performed'}

    show = (lambda x: True) if show_all else (lambda x: x is False)
    
    for sample_id, sample_group in groupby(results, lambda r: r[0].SAMPLE_id):
        print 'Sample', sample_id
        for cmpnd_id_and_name, compound_group in groupby(sample_group, lambda r: (r[0].COMPOUND_id, r[0].COMPOUND_name)):
            compound_group = list(compound_group)            
            if len([r for r in compound_group if r[-1] is False]) > 0:
                print ' '*4 + '%2s %s' % cmpnd_id_and_name
                for cmpnd, test, result in compound_group:
                    if show(result):
                        print ' '*7 + '%-30s %s' % (calc_names[test], outcomes[result])
        