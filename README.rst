==========================================================
 opiates package: automated QA for an LC/MS opaites assay
==========================================================

This project provides a program with a command-line interface for
processing XML-formatted output from a Waters LC/MS
instrument. Configuration of the Waters instrument is documented
elsewhere.

.. contents:: Table of Contents

dependencies
============

* Python 2.7.x
* A UNIX-like operating system (Linux, OS X). Not tested on Windows.

installation
============

Clone the project from the git repository::

    cd ~/src
    git clone git@uwmc-labmed.beanstalkapp.com:/opiates.git
    cd opiates

Now installation can be performed using the familiar mechanism
provided by ``distutils`` (which has no dependencies outside the
Python standard library)::

    sudo python setup.py install

or using ``pip`` (which must be installed separately)::

    sudo pip install .

Subsequent (re)installation with pip should be performed using the
``-U`` option::

    sudo pip install -U .

architecture
============

This project contains the following subdirectories::

    opiates % tree -d          
    .
    |-- dev
    |-- doc
    |-- opiate
    |   |-- data
    |   |-- scripts
    |   `-- subcommands
    |-- testfiles
    `-- tests

with contents as follows:

* ``dev`` - development tools not essential for the primary
   functionality of the softwarwe.
* ``doc`` - files related to project documentation.
* ``opiate`` - the Python package implementing most of the project
   functionality. This subdirectory is installed to the system.
* ``testfiles`` - files and data used for testing.
* ``tests`` - subpackage implementing unit tests.

execution
=========

The ``smack`` script provides the user interface, and uses standard
UNIX command line syntax. Note that for development, it is convenient
to run ``smack`` from within the project directory by specifying the
relative path to the script::

    % ./smack

Commands are constructed as follows. Every command starts with the
name of the script, followed by an "action" followed by a series of
required or optional "arguments". The name of the script, the action,
and options and their arguments are entered on the command line
separated by spaces. Help text is available for both the ``smack``
script and individual actions using the ``-h`` or ``--help`` options::

    % smack -h
    usage: smack [-h] [-V] [-v] [-q]
		 {info,help,results,qa,export,ion_ratios,config} ...

    Command line tool for opaites analysis.

    positional arguments:
      {info,help,results,qa,export,ion_ratios,config}
	help                Detailed help for actions using `help <action>`
	config              Show predefined QA values and other configuration
			    details.
	export              Extract contents of an XML file into another format.
	info                Describe an XML file.
	ion_ratios          Calculate average Ion Ratios for each compound.
	qa                  Perform QA calculations.
	results             Show concentration of each compound.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         Print the version number and exit
      -v, --verbose         Increase verbosity of screen output (eg, -v is
			    verbose, -vv more so)
      -q, --quiet           Suppress output

Help text for an individual action is available by including the name
of the action::

    % smack results -h
    usage: smack results [-h] [-o FILE] [-d DIRECTORY] [-n] [-s {word,firstsix}]
			 infile

    positional arguments:
      infile                Input xml or json file containing experimental data.

    optional arguments:
      -h, --help            show this help message and exit
      -o FILE, --outfile FILE
			    Output file in csv format. If this argument is not
			    provided, the output file name will be generated from
			    the input file name plus the version number. Use '-o
			    -' or '--outfile=-' to print to the screen.
      -d DIRECTORY, --outdir DIRECTORY
			    Optional output directory. Writes to same directory as
			    infile by default.
      -n, --no-calculate-ion-ratio-avg
			    By default, ion ratio averages are calculated from the
			    standards; providing this option causes QA to be
			    performed using 'ion_ratio_avg' from the qa
			    configuration file.
      -s {word,firstsix}, --split-desc {word,firstsix}
			    Method used to process the specimen description: word,
			    use the first whitespace-delimited word; firstsix, use
			    first six characters [default "word"].

So to put this together with the ``column`` command for formatting
tabular data for the screen::

    % ./smack results testfiles/oct24.json -o- | column -ts,
    label          1-UMORPH   2-UOXYM    3-UHMOR    4-UCOD     5-UOXCD    6-UHCOD    7-UMOR6
    Accession02 c  190.57     .          .          .          .          .          .
    Accession03 c  .          .          72.78      .          .          1684.36    .
    Accession04 c  425.36     11.35      .          FAIL       893.01     .          .
    Accession05 c  .          .          10.34      .          .          477.79     .
    Accession06 c  .          .          13.76      .          .          142.48     .
    Accession07 c  FAIL       .          16.98      .          .          1008.58    .
    label          8-UFENTM   9-UMPERM   10-UMPER   11-UFENT   12-UBUPR   13-UPPOX   14-UMETH
    Accession02 c  .          .          .          .          .          .          .
    Accession03 c  .          .          .          .          .          .          .
    Accession04 c  .          .          .          .          .          .          .
    Accession05 c  .          .          .          .          .          .          8786.45
    Accession06 c  .          .          .          .          .          .          .
    Accession07 c  .          .          .          .          .          .          .
    label          15-UMOR3G  16-UMOR6G  17-UHMORG  18-UOXYMG  19-UCOD6G  20-UNBUPG
    Accession02 c  POS        POS        POS        .          .          .
    Accession03 c  POS        POS        .          POS        FAIL       .
    Accession04 c  POS        POS        POS        POS        .          .
    Accession05 c  .          .          POS        .          FAIL       .
    Accession06 c  .          .          POS        .          FAIL       .
    Accession07 c  .          .          POS        .          FAIL       .


versions
========

We use abbrevited git sha hashes to identify the software version::

    % ./smack -V        
    0128.9790c13

The version information is saved in ``opiate/data`` when ``setup.py``
is run (on installation, or even by executing ``python setup.py -h``).

unit tests
==========

Unit tests are implemented using the ``unittest`` module in the Python
standard library. The ``tests`` subdirectory is in fact a Python
package that imports the local version (ie, the version in the project
directory, not the version installed to the system) ``opiate``
package. All unit tests can be run like this::

    opiates % ./testall   
    ...................................................
    ----------------------------------------------------------------------
    Ran 51 tests in 4.224s

    OK

A single unit test can be run by referring to a specific module,
class, or method within the ``tests`` package using dot notation::

    opiates % ./testone tests.test_calculations.TestMeanIonRatios 
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.004s

    OK

