import sys
import os

# Running as py2exe
if hasattr(sys, 'frozen'):
    DEBUG = False
    BASE_DIR = os.path.split(sys.executable)[0]
# Running as interpreter
else:
    DEBUG = True
    BASE_DIR = '.'

# Config file to use for dotnet stuff
CONFIG_FILE = os.path.join(
    BASE_DIR, 'Net2Scripting.exe.config')

# Generic lib dir
LIB_DIR = os.path.join(BASE_DIR, 'libs')

# Version
VERSION = '4.0'
