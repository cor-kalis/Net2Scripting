import os

from distutils.core import setup
from glob import glob
import py2exe

# Data files (resources)
data_files = [('.', ['Net2Scripting.exe.config']),
              ('.', glob(r'../runtime/*.*')),
              ('libs/log4netdll', glob(r'libs/log4netdll/*.*')),
              ('libs/paxton', glob(r'libs/paxton/*.*')),
              ('resources', glob(r'../resources/*.*')),
              ('docs', glob(r'../docs/*.*')),
              ('samples', glob(r'samples/*.py'))]

# Source files (python modules)
source_files = [os.path.splitext(os.path.basename(f))[0] for f in glob('*.py')]

setup(
    # basic console exe
    console=[{'script': 'Net2Scripting.py',
              'icon_resources': [(1, '../resources/Net2Scripting.ico')]}],
    py_modules=source_files,
    data_files=data_files,
#    zipfile=None,
#    options={'py2exe': {'bundle_files': 1, 'compressed': True}}    
    options={
        'py2exe': {
            'dist_dir': '../dist',
        },
        'build': {
            'build_base': '../build'
        }
    }
)
