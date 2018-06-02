"""
Module to use log4net from python
"""
import os
import clr
import sys

import Net2Scripting.settings as settings

# Add path lib to search path
LOG4NET_LIB_DIR = os.path.join(settings.LIB_DIR, 'log4netdll')
if LOG4NET_LIB_DIR not in sys.path:
    sys.path.append(LOG4NET_LIB_DIR)

clr.AddReference('log4net')
import log4net as log4net
from log4net.Config import XmlConfigurator
clr.AddReference('System.Xml')
from System.Xml import XmlDocument


class Log4NetError(Exception):
    """Log4Net exception class
    """
    pass


class Log4Net(object):
    """Class that offers log4net usage, taking its config from an xml file
    """

    @classmethod
    def read_config(cls, config_file):
        """Read and process config file
        """
        if not os.path.isfile(config_file):
            raise Log4NetError('Failed to find config file "%s"' % config_file)

        # Read document
        doc = XmlDocument()
        try:
            doc.Load(config_file)
        except Exception as e:
            raise Log4NetError(str(e))

        # Obtain 1st element with log4net tag
        for element in doc.GetElementsByTagName('log4net'):
            XmlConfigurator.Configure(element)
            break

    @classmethod
    def get_logger(cls, name):
        """Obtain logger instance
        """
        return log4net.LogManager.GetLogger(name)

    @classmethod
    def get_file_appender_logfile(cls):
        """Obtain file appender log file
        """
        for appender in log4net.LogManager.GetRepository().GetAppenders():
            if isinstance(appender, log4net.Appender.FileAppender):
                return str(appender.File)
        return None
