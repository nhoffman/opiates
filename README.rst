==========================================================
 opiates package: automated QA for an LC/MS opaites assay
==========================================================

versions
========

We use abbrevited git sha hashes to identify the software
version. This was set up as described in the pro-git book:
http://progit.org/book/ch7-2.html

Initial setup was performed like this::

    % echo "opiate/data/sha    filter=sha" > .gitattributes
    % git add .gitattributes

I couldn't figure out the quoting and escaping to update the local git
config file (``.git/config``) from the command line using ``git
config``, so I added the following section manually::

    % grep sha .git/config
    [filter "sha"]
	    clean = cat > /dev/null
	    smudge = echo "$(git --no-pager log --pretty=format:\"%h\" -1)"

Now checking out ``opiate/data/sha`` inserts the abbreviated hash
identifying the current commit. This is reflected in the version
number::

    % ./smack --version 
    0.1.f7fe0eb


The rub is that you need to check out ``opiate/data/sha`` to make its contents
describe the current commit. This can be done using ``dev/refresh_sha.sh``::

    % dev/refresh_sha.sh

    shafile=opiate/data/sha
    cat ${shafile:?}
    f7fe0eb
    rm -f ${shafile:?}
    git checkout ${shafile:?}
    cat ${shafile:?}
    f7fe0eb
    git --no-pager log -1
    commit f7fe0ebb28fe986199bb9f33e76a57c0e733477d
    Author: Noah Hoffman <noah.hoffman@gmail.com>
    Date:   Mon Nov 28 16:47:30 2011 -0800

	.gitattributes identified opiate/data/sha

This step needs to be performed before, running ``setup.py`` to
install the package, for example.

