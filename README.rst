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
    % git config filter.sha.clean 'echo _sha=\"\"'
    % git config filter.sha.smudge 'echo _sha=\".$(git --no-pager log --pretty=format:"%h" -1)\"' 



