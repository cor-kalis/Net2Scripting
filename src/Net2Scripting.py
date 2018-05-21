"""
Main program for Net2Scripting.
"""
import os
import sys
import settings
import traceback

# This is just to force py2exe to include these packages
if False == True:    
    import net2xs
    import net2dbxs
    import network
    # Not required but nice to have
    import abc
    import aifc
    import antigravity
    import argparse
    import ast
    import asynchat
    import asyncio
    import asyncore
    import base64
    import bdb
    import binhex
    import bisect
    import bz2
    import cProfile
    import calendar
    import cgi
    import cgitb
    import chunk
    import cmd
    import code
    import codecs
    import codeop
    import collections
    import colorsys
    import compileall
    import concurrent
    import configparser
    import contextlib
    import copy
    import copyreg
#    import crypt
    import csv
    import ctypes
#    import curses
    import datetime
#    import dbm
    import decimal
    import difflib
    import dis
    import distutils
    import doctest
    import threading
    import email
    import encodings
#    import ensurepip
    import enum
    import filecmp
    import fileinput
    import fnmatch
    import formatter
    import fractions
    import ftplib
    import functools
    import genericpath
    import getopt
    import getpass
    import gettext
    import glob
    import gzip
    import hashlib
    import heapq
    import hmac
    import html
    import http
    import idlelib
    import imaplib
    import imghdr
    import imp
    import importlib
    import inspect
    import io
    import ipaddress
    import json
    import keyword
    import lib2to3
    import linecache
    import locale
    import logging
    import lzma
#    import macpath
#    import macurl2path
    import mailbox
    import mailcap
    import mimetypes
    import modulefinder
    import msilib
#    import multiprocessing
    import netrc
    import nntplib
    import ntpath
    import nturl2path
    import numbers
    import opcode
    import operator
    import optparse
    import os
    import pathlib
    import pdb
    import pickle
    import pickletools
    import pipes
    import pkgutil
    import platform
    import plistlib
    import poplib
    import posixpath
    import pprint
    import profile
    import pstats
    import pty
    import pyclbr
    import pydoc
    import pydoc_data
    import queue
    import quopri
    import random
    import re
    import reprlib
    import rlcompleter
    import runpy
    import sched
    import selectors
    import shelve
    import shlex
    import shutil
    import site
#    import smtpd
    import smtplib
    import sndhdr
    import socket
    import socketserver
    import sqlite3
#    import compile
#    import constants
#    import parse
    import ssl
    import stat
    import statistics
    import string
    import stringprep
    import struct
    import subprocess
    import sunau
    import symbol
    import symtable
    import sysconfig
    import tabnanny
    import tarfile
    import telnetlib
    import tempfile
    import test
    import textwrap
    import this
    import threading
    import timeit
    import tkinter
    import token
    import tokenize
    import trace
    import traceback
    import tracemalloc
    import tty
    import turtle
    import turtledemo
    import types
    import unittest
    import urllib
    import uu
    import uuid
    import venv
    import warnings
    import wave
    import weakref
    import webbrowser
    import wsgiref
    import xdrlib
    import xml
    import xmlrpc
    import zipfile


# Setup logging first
from pylog4net import Log4Net
try:
    Log4Net.read_config(settings.CONFIG_FILE)
except Exception as e:
    print('Log error: %s' % (str(e)))
    sys.exit(1)

from config import Config
try:
    cfg = Config(settings.CONFIG_FILE)
except Exception as e:
    print('Config error: %s' % (str(e)))
    sys.exit(1)

# Running as py2exe: check if linecache should be enabled
# if hasattr(sys, 'frozen'):
#     if cfg.get("enable_linecache", True, bool):
#         # Monkey patch it back to the original value
#         import linecache
#         linecache.getline = linecache.orig_getline
#         del linecache

# Log4net logger
logger = Log4Net.get_logger('Net2Scripting')


def run(script_file):
    """Run script file
    """
    try:
        if not os.path.isfile(script_file):
            raise Exception("User script '%s' does not exist!" % (script_file))

        # Get script dir and add it to the module search path
        sys.path.insert(0, os.path.dirname(script_file))

        print("Press '<ctrl> C' to quit...")
        logger.Debug("Calling user script '%s'" % (script_file))
        try:
            # Strip Net2Scripting param from arguments
            sys.argv = sys.argv[1:]            
            # Explicitly provide dict, to prevent scope issues
            with open(script_file) as f:
                code = compile(f.read(), script_file, 'exec')
                exec(code, 
                     {"__name__": "__main__",
                      "__file__": script_file,
                      "__scripting_version__": settings.VERSION})
        except KeyboardInterrupt:
            logger.Debug("User interrupt")

    except Exception as ex:

        msg = "Fatal error: " + str(ex)
        if cfg.get("log_stacktrace", default=False, vtype=bool):
            msg += "\n" + traceback.format_exc()
        logger.Fatal(msg)
        return 1


def run_key(script_key):
    """Run file referenced by setting keyword
    """
    try:
        script_key = script_key.strip()
        if not script_key:
            raise "The provided script keyword is empty!"

        # Fetch setting from config
        cfg.check_required([(script_key, str)])

        return run(cfg.get(script_key))

    except Exception as ex:
        logger.Fatal("Fatal error: " + str(ex))
        return 1


def confirm_wait():
    """Wait for user confirmation
    """
    # Fetch setting from config
    wait = cfg.get("confirm_wait", default=False, vtype=bool)
    if wait:
        print()
        input("Press enter to continue: ")


# Main program entry
if __name__ == '__main__':

    ret_val = 0

    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1]

            if arg == "/?":
                print()
                print("Net2Scripting V%s, by Net2 Solutions" % (settings.VERSION))
                print()
                print("  /? = help")
                print("  /k:keyword = run script referenced by appSettings keyword")
                print("  <script file path> = run given script")
                print()
                print("  By default, the script referenced by the 'user_script' setting is run.")
                print("  Settings are located in the 'Net2Scripting.exe.config' file.")
                print("  Also modify this file if you prefer different log settings.")
                print
                ret_val = 1

            # Run by keyword
            elif arg.startswith("/k:"):
                ret_val = run_key(arg.split(":", 1)[1])

            # Run as file
            elif not arg.startswith("/"):
                ret_val = run(arg)

            # Unknown option
            else:
                print("Unknown parameter: " + arg)
                ret_val = 1
        else:
            # Run as default
            ret_val = run_key("user_script")

    finally:
        # Wait for user confirmation when required
        confirm_wait()

    # Return with value
    sys.exit(ret_val)
