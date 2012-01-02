from collections import Iterable

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
    if args.outfile is None:
        dirname, basename = path.split(args.infile)
        outfile = open(
            path.join(
                args.outdir or dirname,
                '.'.join([path.splitext(basename)[0], __version__, label, 'csv'])
                ), 'w')
    else:
        outfile = args.outfile
                
