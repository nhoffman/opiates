==========================================================
 opiates package: automated QA for an LC/MS opaites assay
==========================================================

installation
============

Installation to the system is performed either in the standard way for
a Python package::

    sudo python setup.py install

or using `pip`::

    sudo pip install .

Subsequent (re)installation with pip should be performed using the
``-U`` option::

    sudo pip install -U .

versions
========

We use abbrevited git sha hashes to identify the software
version. This was set up as described in the pro-git book:
http://progit.org/book/ch7-2.html

Initial setup was performed like this::

    % echo "opiate/data/sha    filter=sha" > .gitattributes
    % git add .gitattributes

A newly cloned repo contains `.gitattributes`, so this doesn't need to
be repeated. However, some local configuration does need to be
performed before the version will be defined properly in
`setup.py`. This one-time configuration is taken care of when
`setup.py` is first run.

In addition, before each installation, `opiate/data/sha`, the file
containing the abbreviated git sha, needs to be updated to contain the
hash representing the current commit. This is also taken care of when
`setup.py` is run. Note, however, that all changes must be committed
before installation, or the version hash will not accurately reflect
the current state of the code.


