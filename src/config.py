"""
Module to read dot type config settings from python
"""
import os
import re

from datetime import datetime
from xml.etree import ElementTree as ET


class ConfigError(Exception):
    """Config exception class
    """
    pass


class Config(object):
    """Class for reading and writing to the config file
    """

    def __init__(self, config_file):
        """Read config file
        """
        self.config_file = config_file

        self._app_settings = {}

        if not os.path.isfile(config_file):
            raise ConfigError('Failed to find config file "%s"' % config_file)

        # Read document
        tree = ET.ElementTree()

        tree.parse(config_file)

        # Obtain appSettings
        element = tree.find('appSettings')
        if element is None:
            raise ConfigError(
                'Required "appSettings" section is missing in config file' %
                self.config_file)
        for item in element.findall('add'):
            if 'key' in item.attrib and 'value' in item.attrib:
                key = item.attrib['key']
                val = item.attrib['value']
                self._app_settings[key] = val
            else:
                raise ConfigError(
                    'Encountered appSetting with missing attributes')

    def _parse_as_datetime(self, val):
        """Attempt to parse val as datetime
        """
        if re.match(r'\d+:\d+:\d+', val):
            fmt = '%H:%M:%S'
        elif re.match(r'\d\d\d\d-\d+-\d+', val):
            fmt = '%Y-%m-%d'
        elif re.match(r'\d\d\d\d-\d+-\d+ \d+:\d+:\d+', val):
            fmt = '%Y-%m-%d %H:%M:%S'
        else:
            raise ValueError('Illegal datetime format')

        return datetime.strptime(val, fmt)

    def check_required(self, item_list):
        for key, vtype in item_list:
            val = self._app_settings.get(key)
            if val is None:
                raise ConfigError('Required setting for "%s" is missing' % key)
            if vtype != str:
                try:
                    if vtype == datetime:
                        self._parse_as_datetime(val)
                    else:
                        vtype(val)
                except ValueError:
                    raise ConfigError(
                        'Required setting for "%s" (%s), is no %s type' %
                        (key, val, vtype.__name__))

    def get(self, key, default=None, vtype=str):
        """Obtain typecasted value
        """
        val = self._app_settings.get(key, default)
        if val is None:
            return None
        if vtype == str:
            return val
        if vtype == datetime:
            try:
                return self._parse_as_datetime(val)
            except ValueError:
                return default
        if vtype == bool:
            return val.lower() == 'true'
        try:
            return vtype(val)
        except ValueError:
            return default
