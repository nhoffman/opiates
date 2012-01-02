import glob
from os.path import splitext, split, join
import argparse

def itermodules(subcommands_path, root=__name__):

    commands = [x for x in [splitext(split(p)[1])[0] for p in glob.glob(join(subcommands_path, '*.py'))] if not x.startswith('_')]

    for command in commands:
        yield command, __import__('%s.%s' % (root, command), fromlist=[command])

def add_infile(parser):        
    parser.add_argument('infile', help='Input xml or json file containing experimental data.')

def add_outfile(parser):
    parser.add_argument(
        '-o','--outfile', metavar = 'FILE', default = None,
        type = argparse.FileType('w'), help = """Output file in csv
        format. If this argument is not provided, the output file name
        will be generated from the input file name plus the version
        number. Use '-o -' or '--outfile=-' to print to the screen.""")

def add_outdir(parser):
    parser.add_argument(
        '-d','--outdir', metavar = 'DIRECTORY', default = None,
        help = """Optional output directory. Writes to same directory
        as infile by default.""")

def add_no_calculate_ion_ratio_avg(parser):    
    parser.add_argument(
        '-n','--no-calculate-ion-ratio-avg', help = """By default, ion
        ratio averages are calculated from the standards; providing
        this option causes QA to be performed using 'ion_ratio_avg'
        from the qa configuration file.""",
        action = 'store_false', dest = 'calculate_ion_ratios',
        default = True)

def add_split_desc(parser):
    parser.add_argument(
        '-s','--split-desc', default = 'word', choices = ['word','firstsix'],
        help = """Method used to process the specimen description:
        word, use the first whitespace-delimited word; firstsix, use
        first six characters [default "%(default)s"].""")
    
