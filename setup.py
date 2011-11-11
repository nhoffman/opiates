"""
Create unix package:    python setup.py sdist
"""

from distutils.core import setup

# try:
#     from setuptools import setup, find_packages
# except ImportError:
#     import distribute_setup
#     distribute_setup.use_setuptools()
#     from setuptools import setup, find_packages

from opiate import __version__

params = {'author': 'Noah Hoffman',
          'author_email': 'ngh2@uw.edu',
          'description': 'Analysis of LC/MS opiates assay',
          'name': 'opiate',
          'packages': ['opiate','opiate.scripts','opiate.subcommands'],
          'package_dir': {'opiate': 'opiate'},
          'scripts': ['smack'],
          'version': __version__,
          # 'install_requires': ['sqlalchemy', 'decorator'],
          'package_data': {'opiate': ['data/qa.csv']}
          }

setup(**params)

