"""
Main program for Net2Scripting.
Basically just intializes the log4net.
"""
import sys
import Net2Scripting.settings


def init_logging(config_file=None):
    """Init logging
    """
    # If no config file is given, use the default
    if not config_file:
        config_file = settings.CONFIG_FILE

    # Setup logging first
    from Net2Scripting.pylog4net import Log4Net
    try:
        Log4Net.read_config(config_file)
    except Exception as e:
        print('Log error: %s' % (str(e)))
        sys.exit(1)

    from Net2Scripting.config import Config
    try:
        cfg = Config(settings.CONFIG_FILE)
    except Exception as e:
        print('Config error: %s' % (str(e)))
        sys.exit(1)
