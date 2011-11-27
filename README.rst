==========================================================
 opiates package: automated QA for an LC/MS opaites assay
==========================================================

versions
========

We use abbrevited git sha hashes to identify the software
version. This was set up as described in the pro-git book:
http://progit.org/book/ch7-2.html

Initial setup was performed like this::

    % cat .gitattributes
    opiate/__init__.py	filter=sha
    % git add .gitattributes
    % git config --global filter.sha.clean dev/clean.py
    % git config --global filter.sha.smudge dev/smudge.py



