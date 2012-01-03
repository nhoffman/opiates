from collections import Iterable
import os
from os import path
import shutil

from __init__ import __version__

def flatten(seq):
    """
    Poached from http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python

    Don't flatten strings or dict-like objects.
    """
    for el in seq:
        if isinstance(el, Iterable) and not (isinstance(el, basestring) or hasattr(el, 'get')):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def get_outfile(args, label, ext = 'csv'):
    """
    Return a file-like object open for writing. `args` is expected to
    have attributes 'infile' (None or a string specifying a file
    path), 'outfile' (None or a file-like object open for writing),
    and 'outdir' (None or a string defining a dir-path). If
    `args.outfilr` is None, the name of the outfile is derived from
    the basename of `args.infile` and is written either in the same
    directory or in `args.outdir` if provided.
    """

    if args.outfile is None:
        dirname, basename = path.split(args.infile)
        outfile = open(
            path.join(
                args.outdir or dirname,
                '.'.join([path.splitext(basename)[0], __version__, label, 'csv'])
                ), 'w')
    else:
        outfile = args.outfile
        if not (hasattr(outfile, 'write') and not outfile.closed and 'w' in outfile.mode):
            raise OSError('`args.outfile` must be a file-like object open for writing')

    return outfile

def mkdir(dirpath, clobber = False):
    """
    Create a (potentially existing) directory without errors. Raise
    OSError if directory can't be created. If clobber is True, remove
    dirpath if it exists.
    """

    if clobber:
        shutil.rmtree(dirpath, ignore_errors = True)

    try:
        os.mkdir(dirpath)
    except OSError, msg:
        pass

    if not path.exists(dirpath):
        raise OSError('Failed to create %s' % dirpath)

    return dirpath

