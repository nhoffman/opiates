"""
Create unix package:    python setup.py sdist
"""

import os
import subprocess
import shutil
from distutils.core import setup
from os.path import join

with open(os.devnull, 'w') as stdout, open(os.devnull, 'w') as stderr:
    outputs = {'stdout': stdout, 'stderr': stderr}
    # outputs = {}
    try:
        subprocess.check_call(['git', 'status'], **outputs) 
    except subprocess.CalledProcessError:
        git_available = False
    else:
        git_available = True

    # The first time a repo is cloned, the local configuration needs
    # to be updated to add the attributes 'filter.sha.clean' and
    # 'filter.sha.smudge'. Do this now if necessary.        
    if git_available and subprocess.call(['git', 'config', '--get-regexp', 'filter.sha'], **outputs) != 0:
        print 'updating git config'
        subprocess.call(['git', 'config', '--remove-section', 'filter.sha'], **outputs)    
        gitconf = '.git/config'
        shutil.copyfile(gitconf, 'git-config.bak')
        with open(gitconf, 'a') as fobj:
            fobj.write('\n[filter "sha"]\n')
            fobj.write('clean = cat > /dev/null\n')
            fobj.write(r'smudge = echo "$(git --no-pager log --pretty=format:\"%h\" -1)"')
        subprocess.call(['git', 'config', '--get-regexp', 'filter.sha'])

    # Make sure that the version number is up to date if we're
    # installig from a git repo. Note that the version number is
    # performed even if installation is not (eg, 'python setup.py
    # -h'). The version number is stored in `shafile`; we must make
    # sure that the shafile retains its original attributes since this
    # command may be run as root.
    if git_available:
        shafile = 'opiate/data/sha'
        stats = os.stat(shafile)
        os.rename(shafile, shafile+'.bak')
        subprocess.check_call(['git', 'checkout', shafile], **outputs)
        os.chown(shafile, stats.st_uid, stats.st_gid)
        new, old = [open(f).read().strip() for f in [shafile, shafile+'.bak']]
        if old != new:
            print 'updated version sha: %s --> %s' % (old, new)
        
from opiate import __version__

params = {'author': 'Noah Hoffman',
          'author_email': 'ngh2@uw.edu',
          'description': 'Analysis of LC/MS opiates assay',
          'name': 'opiate',
          'packages': ['opiate','opiate.scripts','opiate.subcommands'],
          'package_dir': {'opiate': 'opiate'},
          'scripts': ['smack'],
          'version': __version__,
          'package_data': {'opiate': [join('data',f) for f in ['qa.csv','matrix.csv','sha']]}
          }
    
setup(**params)

