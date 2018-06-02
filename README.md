Net2Scripting
===

Python scripting package for the Paxton Net2 SDK.

This project offers a Python interface to the Paxton Net2 Access Control
system, using the SDK or or a direct DB connection.

It was originally a closed source project, that used py2exe to create an 
executable. V4.0 was made open source, but still used py2exe.
From V5.0 onwards it will be a Python wheel package.

Have a look at the samples directory (github) to get an idea how to use it.
Note that it has slightly changed after becoming an installable Python package.

For the original py2exe version, pull the v4.0 tag.

### Requirements
The NetScripting project relies on the following:
 * A Windows environment.
 * DotNet 4.0 or higher.
   - Installing Paxton Net2 V5.x or higher should take care of that.
   - The Paxton Net2 OEMClientLibrary dlls (v5.01) are included in this package.
 * pythonnet
   - Should be automatically installed as a dependency.

### Configuration
To use the log4net logging, you need to call the init_logging() method before
doing anything else. If no parameter is given, the default log setting is 
used, which sets the application log level to DEBUG, the Paxton loglevel to 
ERROR and writes to both console and a rolling log file at
${SystemDrive}/Net2 Access Control/Net2Scripting.log.
If you require non default settings, provide a path to your own config file 
as parameter. There is a sample config file in the samples directory.

### Building the wheel package file
In the directory containing setup.py run:
```
python setup.py sdist bdist_wheel
```
The resulting wheel file should pop up in the dist directory.

### Install
 * Download the whl file from the dist directory.
 * pip install Net2Scripting-X.Y.Z-py3-none-any.whl

### Uninstall
 * pip uninstall Net2Scripting

### Todo
  * Unit tests
  * Add SDK features

### License
MIT
