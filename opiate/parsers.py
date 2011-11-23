#!/usr/bin/env python

import pprint
import xml.etree.ElementTree
import sys
import csv
from collections import defaultdict, OrderedDict
from itertools import chain, groupby, count
from calculations import all_checks

from __init__ import qafile, SAMPLE_ATTRS, CONTROL_NAMES, SAMPLE_PREP_LABELS, SAMPLE_PREP_ORDER

dump = xml.etree.ElementTree.dump

def get_attrs(elem):
    """
    Return a dict containing all attributes and attributes of child
    elements keyed by <element tag>_<attribute name>
    """

    return {elem.tag+'_'+key: val for key, val in elem.attrib.items()}

def flatten(elem, attr = None):
    """
    Recursively flatten an xml.etree.ElementTree element into a dict
    containing all of elem's attributes, as well as attributes of
    child elements keyed by <element tag>_<attribute name>.
    """

    attr = attr or {}
    attr.update(get_attrs(elem))

    children = list(elem)
    if children:
        for child in children:
            attr.update(flatten(child, attr))

    return attr

def cast(val, fun):
    """
    Return `fun(val)` or None if ValueError.
    """

    try:
        return fun(val)
    except ValueError:
        return None

def cast_numeric(val, failfun = lambda x: None):
    """
    Attempt to coerce val first into an in, then into a float. If both
    attempts fail, apply `failfun` to `val`.
    """

    for fun in (int, float, failfun):
        try:
            retval = fun(val)
        except ValueError:
            pass
        else:
            return retval

def cast_vals(d, attrs):
    """
    Apply transformations specified by each `fun` in `attrs`, a list of
    two-tuples containing (`key`, `fun`), limiting output to keys.
    """
    return {key:cast(d[key], fun) for key, fun in attrs if key in d}

def parse_sample(sample, compound_ids = None):
    """
    Return an iterator of dicts containing data for `sample`. Restrict
    to compounds with an id contained in set `compound_ids` if provided.
    """

    if compound_ids:
        keep = lambda d: d['COMPOUND_id'] in compound_ids
    else:
        keep = lambda d: True

    sample_data = cast_vals(get_attrs(sample), SAMPLE_ATTRS)
    for compound in sample.findall('COMPOUND'):
        compound_data = cast_vals(flatten(compound), SAMPLE_ATTRS)
        if keep(compound_data):
            compound_data.update(sample_data)
            yield compound_data

def get_rows(infile):

    qadata = qa_from_csv(qafile)
    compound_ids = [d['qa_id'] for d in qadata.values()]

    tree = xml.etree.ElementTree.ElementTree(file=infile)
    sample_elems = tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')
    rows = chain.from_iterable(parse_sample(elem, compound_ids) for elem in sample_elems)

    return rows

def group_samples(infile, ctl_names = CONTROL_NAMES, split_desc = lambda desc: desc.split()[0]):
    """
    Parse the contents of XML-file `infile`, and return two
    OrderedDict objects: (`controls`,`sample_groups`) where `controls`
    is keyed by names in ctl_names (default is `opiate.CONTROL_NAMES`)
    and `sample_groups` is a dict of groups generated by applying
    function `split_desc` to each SAMPLE_desc. Dicts containing
    compound data in sample_groups are given an additional key
    'sample_prep' returning an element of opiate.SAMPLE_PREP_LABELS
    corresponding to their position in the group *if* the group is of
    length 4. Also adds `sample_order` to these samples indicating
    order in which samples should be sorted within each group of 4,
    and `sample_label` containing the sample grouping term.

     * XML file
     * ctl_names - list of (sample_id, control_name) tuples
     * split_desc - function applied to SAMPLE_desc used to group clinical samples.
    """

    qadata = qa_from_csv(qafile)
    compound_ids = [d['qa_id'] for d in qadata.values()]

    tree = xml.etree.ElementTree.ElementTree(file=infile)

    samples = [list(parse_sample(elem, compound_ids)) \
                   for elem in tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')]

    # controls is a dict with keys defined in ctl_names returning a
    # list of dicts, each containing data for one compound. Here we
    # consume from the top of the list of samples until the specimens
    # identified as controls are exhausted.
    controls = OrderedDict()
    for sample_id, name in ctl_names:
        sample = samples.pop(0)
        assert sample[0]['SAMPLE_id'] == sample_id
        controls[name] = sample

    # the remainder of samples are now grouped by leading common
    # elements in SAMPLE_desc according to function `split_desc`.
    sample_groups = OrderedDict()
    for label, grp in groupby(samples, lambda s: split_desc(s[0]['SAMPLE_desc'])):
        this_group = list(grp)
        if len(this_group) == len(SAMPLE_PREP_LABELS):
            for sample_prep, sample_order, sample in zip(
                SAMPLE_PREP_LABELS, SAMPLE_PREP_ORDER, this_group):
                for cmpnd in sample:
                    cmpnd['sample_prep'] = sample_prep
                    cmpnd['sample_order'] = sample_order
                    cmpnd['sample_label'] = label
        else:
            for sample in this_group:
                for cmpnd in sample:
                    cmpnd['sample_label'] = label
        sample_groups[label] = this_group

    return (controls, sample_groups)

def qa_from_csv(fname):

    qadata = OrderedDict()
    with open(fname, 'rU') as f:
        reader = csv.DictReader(f)
        for d in reader:
            coerced = OrderedDict((k, cast_numeric(d[k]) or d[k].strip() or None) \
                                      for k in reader.fieldnames)
            compound_id = coerced['qa_id']
            if compound_id:
                qadata[compound_id] = coerced

    return qadata

def read_matrix(fname):
    """
    Read a configuration file describing compound-calculation
    combinations for each specimen. Returns a dict keyed by
    (sample_id, compound_id) returning a set of calculation
    names.

    The input is a csv-format file with a column `compound_id` and
    additional columns named "check_*". Sample ids are provided
    as a comma-delimited list in each cell.
    """

    split_and_cast = lambda x: [cast_numeric(e, lambda x: x) for e in x.split(',')] if x else []

    matrix = defaultdict(set)
    with open(fname, 'rU') as f:
        reader = csv.DictReader(f)
        headers = [n for n in reader.fieldnames if n]

        # ensure that all tests are defined in matrix file
        missing = set(all_checks.keys()) - set(headers)
        if missing:
            raise ValueError('matrix file does not define %s' % \
                                 ', '.join(missing))

        for d in [d for d in reader if d['compound_id']]:
            compound_id = int(d['compound_id'])
            for k, v in d.items():
                if k.startswith('check_'):
                    for sample_id in split_and_cast(v):
                        matrix[(sample_id, compound_id)].add(k)

    return dict(matrix)

def remove_patient_info(samples):
    controls, specimen_groups = samples

    sanitized = OrderedDict()

    group_number = count(1)
    for label, group in specimen_groups.items():
        new_label = 'Accession%02i' % group_number.next()
        for sample in group:
            for compound in sample:
                compound['sample_label'] = new_label
                compound['SAMPLE_desc'] = '%s %s' % \
                    (new_label, compound.get('sample_prep') or compound['SAMPLE_id'])
        sanitized[new_label] = group

    return (controls, sanitized)
