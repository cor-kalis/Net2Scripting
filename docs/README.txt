Net2Scripting
=============

The Net2Scripting program is an add-on for the Paxton Net2 software.
It offers the possibility to run Python scripts against the Net2 SDK or
straight against the Net2 database.
Using the SDK, you can access remote Net2 servers. Using the direct database
interface, only local access is possible.

Scripting allows ad-hoc functionality to be created, without compilation.
Useful for proof of concepts, filling Net2 with test data, simple door
control, Net2 data exports, etc.

REQUIREMENTS
* A PC running a recent Windows version. The software has been tested on
  WinXP(SP3), Win7 and Win8.
* Administrator rights.
* The Net2 V5.1 or higher software package.

INSTALLATION
* Run the installer program, which will create an IntoAccess folder in the 
  Programs menu with a shortcut to Net2Scripting, install the executable, 
  libraries, samples and documentation.
* Optionally edit the Net2Scripting.exe.config file that can be found in the
  program installation folder.
  (by default it contains a reference to a sample script 
   'samples/user_script.py')

USAGE
* Option 1: Edit the Net2Scripting.exe.config file, changing the
  'user_script' setting to point to your script. Run the Net2Scripting
  program.
* Option 2: Edit the Net2Scripting.exe.config file, adding more entries to
  the 'appSetting' section. Run the Net2Scripting program adding the parameter
  /k=<keyword>, where <keyword> points to the script you want to execute.
* Option 3: Run the Net2Scripting program, adding the path to the script you
  wish to execute as parameter.
* If you run the Net2Scripting using the explorer, you may want the window
  containing the script result to remain open. Set the appSetting 
  'confirm_wait' to 'true' to have it wait for the <enter> key before closing.
  If you want to run a script using a scheduler, set this option to 'false'.
* By default, the application logs fairly much and both to the console as
  well as to a (rolling) file. Change the root 'level' value from DEBUG to
  INFO, WARN, ERROR or FATAL to make it less verbose. You can add or remove
  any log4net conpatible log appenders to suit your needs.
  Beware that the scripting program locks the log file, so if you run more
  than one instance, it will complain about not being able to log.

DOCUMENTATION / HELP
* Some pydoc generated 'help' for the API is placed in the 'docs'
  subdirectory of the installation folder. It does not hurt however to also
  keep the Net2 API doc at hand while scripting.
* A number of script samples are provided, meant for those with some basic
  knowledge of Python. For a full Python language reference, check out
  http://www.python.org/doc/
  Not all Net2 SDK functions are available through the python api yet.
  If you would like to add stuff however, check out the'inheritance.py'
  sample to get you started.
* The (free) Net2Query tool, available at http://www.intoaccess.com, can 
  also of use to get some insight on available tables, column names and 
  data types.

BACKGROUND
* Originally created by CRC Value.
* Maintained (sort of) by IntoAccess from July 2017 - May 2018.
* Open source from May 2018 onward.
* The package websites:
  - http://www.net2scripting.nl
  - https://github.com/cor-kalis/Net2Scripting

ACKNOWLEDGEMENTS
* The Net2Scripting program is created using the following libraries/tools:
  - Python => http://www.python.org
  - Python.Net => http://pythonnet.sourceforge.net
  - Py2exe => http://www.py2exe.org
  - Paxton.Net2.OEMClientLibrary => http://www.paxton.co.uk
  - Inno Setup => http://www.jrsoftware.org

LICENSE
* MIT

DISCLAIMER
* You will use this software at your own risk. No responsibility is accepted for
  any damage it may accidentally cause.

HISTORY
* V1.0 was published in April 2013. Initial version
* V1.1 was published in July 2013.
  - Fixes a module scope issue (imported modules not recognized in functions).
  - User image manipulation.
  - Confirm wait, even on a sys.exit().
  - Allow remote native db access.
  - Net2Plus module detection using udp broadcasts.
  - SQLServer detection using udp broadcasts.
  - Default values for add_user and modify_user (less hassle).
* V1.2 was published in July 2013.
  - Enable linecache.getline by default, so 'list' in pdb.set_trace() shows
    something useful. (disable in config by setting 'linecache_enable' to false)
  - Added __scripting_version__ var, to test script compatibility.
  - Fixed bug in Net2XS.deactivate_user fuction.
* V1.3 was published in September 2013.
  - Fix / implement acu monitoring
  - Fix get_users / get_user_by_id bug
* V1.4 was published in October 2013.
  - Fix password encryption on remote native database connection
* V2.0 was published in April 2014.
  - Net2 V5 compatible.
* V2.1 was published in July 2014.
  - Fix hard coded event and subtype bug in add_event_record.
* V2.2 was published in October 2014.
  - Removed misplaced delete_image parameter in add_user
* V2.3 was published in December 2015.
  - Upgraded to Python 2.7.10 and included most standard Python modules.
* V2.4 was published in August 2016.
  - Added the option to use either a dotnet or python date time objects for
    the add_user and modify_user methods.
  - Added delete_card and get_cards methods.
* V3.0 was published in August 2017.
  - Upgrade to Python 3.4.4
* V4.0 was published in May 2018.
  - Made open source.
