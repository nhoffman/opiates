==========================================================
 opiates package: automated QA for an LC/MS opaites assay
==========================================================

versions
========

We use abbrevited git sha hashes to identify the software
version. This was set up as described in the pro-git book:
http://progit.org/book/ch7-2.html

Initial setup was performed like this::

    % echo "opiate/_sha.py    filter=sha" > .gitattributes
    % git add .gitattributes

I couldn't figure out the quoting and escaping to update the local git
config file (``.git/config``) from the command line using ``git
config``, so I added the following section manually::

    % grep sha .git/config
    [filter "sha"]
        clean = python -c \"print '_sha = None'\"
        smudge = echo "_sha=\"$(git --no-pager log --pretty=format:\"'.%h'\" -1)\""

Now checking out ``opiate/_sha.py`` inserts the abbreviated hash
identifying the current commit. This is reflected in the version
number::



