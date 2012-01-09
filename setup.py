"""
Create unix package:    python setup.py sdist
"""

import os
import subprocess
import shutil
from distutils.core import setup
from os.path import join

subprocess.call('git log --pretty=format:%h -n 1 > opiate/data/sha', shell = True)
subprocess.call('git shortlog --format="XXYYXX%h" | grep -c XXYYXX > opiate/data/ver', shell = True)

from opiate import __version__

params = {'author': 'Noah Hoffman',
          'author_email': 'ngh2@uw.edu',
          'description': 'Analysis of LC/MS opiates assay',
          'name': 'opiate',
          'packages': ['opiate','opiate.scripts','opiate.subcommands'],
          'package_dir': {'opiate': 'opiate'},
          'scripts': ['smack'],
          'version': __version__,
          'package_data': {'opiate': [join('data',f) for f in ['qa.csv','matrix.csv','sha','ver']]}
          }
    
setup(**params)

