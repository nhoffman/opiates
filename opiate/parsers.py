#!/usr/bin/env python

import pprint
import xml.etree.ElementTree
import sys
import csv
from collections import defaultdict, OrderedDict
from itertools import chain

from __init__ import qafile

dump = xml.etree.ElementTree.dump

sample_attrs = (
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

def cast_numeric(val):
    """
    Attempt to coerce val first into an in, then into a float or
    return None if both fail.
    """

    for fun in (int, float, lambda x: None):
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

    sample_data = cast_vals(get_attrs(sample), sample_attrs)
    for compound in sample.findall('COMPOUND'):
        compound_data = cast_vals(flatten(compound), sample_attrs)
        if keep(compound_data):
            compound_data.update(sample_data)
            yield compound_data

def get_rows(infile):

    qadata = qa_from_csv(qafile)    
    tree = xml.etree.ElementTree.ElementTree(file=infile)
    samples = tree.getiterator('SAMPLELISTDATA')[0].findall('SAMPLE')

    compound_ids = [d['id'] for d in qadata.values()]
    rows = chain.from_iterable(parse_sample(sample, compound_ids) for sample in samples)

    return rows
            
def qa_from_csv(fname):

    qadata = OrderedDict()
    with open(fname, 'rU') as f:
        reader = csv.DictReader(f)
        for d in reader:
            compound = d.pop('compound').strip()
            if compound:
                qadata[compound] = OrderedDict((k, cast_numeric(d[k])) for k in reader.fieldnames[1:])

    return qadata
