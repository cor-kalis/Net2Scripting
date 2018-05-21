Net2Scripting
===

Python scripting for the Paxton Net2 SDK.

This project builds a setup file, that will install a Python scripting environment
that can communicate with Paxton Net2, using the SDK (or a direct DB connection).


### Read this first
The scripts in this package are currently quite inflexible, in that they assume
that packages are installed in particular directories. For future versions this
should be changed to maybe an environment setting or a 'user' file containg the
definitions. (this file should be in .gitignore)

For now, the install directories are specificly marked in the requirements.

### Requirements
The NetScripting project relies on the following:
 * An x86 Windows environment (64-bit did not work). Windows7-32bit should be ok.
 * DotNet 4.0
   - Installing Paxton Net2 V5.x should take care of that
   - The Paxton Net2 OEMClientLibrary dlls (v5.01) are included in this package.
 * Python x86 3.4.4
   - Is the Python environment
   - Download from http://www.python.org
   - **Install in C:\WinPrg\Python34\ !!!**
 * pythonnet-2.3.0-cp34-cp34m-win32.whl
   - Is Python .net extension
   - Download from http://pythonnet.sourceforge.net
   - Install with pip install <wheel file>
 * py2exe-0.9.2.2-py33.py34-none-any.whl
   - To create a python executable
   - Download from http://www.py2exe.org
   - Install with pip install <wheel file>
   - Remove 'clr' in c:/WinPrg/Python34/lib/site-packages/py2exe/hooks.py !!!
   - Note that py2exe does/did not support 3.5 and up yet
 * Inno Setup 5.4.2 (higher versions most likely also work)
   - To create an installer (uses the inno_script.iss)
   - Download from http://www.jrsoftware.org   
   - **Install in C:\Program Files\Inno Setup 5\ !!!**

The following convenience batch files are available:
 * run.bat
   - To run de scripting tool while testing sample code
   - It will wait after execution and run again after pressing enter (ctrl C=exit)
   - Do no just click it in explorer; this will not work
   - Create a sendTo shortcut to it, to execute python scripts from the explorer. 
     + type "shell:sento" in the file explorer address bar to access the 
       SentTo folder
     + Create shortcut to run.bat and call it "Test with Net2Scripting"
 * make.bat
   - Creates an exe-based distro in ./dist
   - You can click it in explorer 
 * build_installer.bat
   - Requires make.bat to run first
   - Creates a 'SetupNet2Scripting.exe' in ./dist_installer
   - You can click it in explorer 

Beware of the following:
  * That the doc's generated, need to be defined in src/docgen.py
  * That for py2exe, new modules must be defined in 'Net2Scripting.py',
    to have py2exe include them in the exe generation.
  * That the makefile.bat will show warnings (which we ignore for now):
```
  8 missing Modules
  ------------------
? Paxton                              imported from net2xs
? _dbm                                imported from dbm.ndbm
? log4net                             imported from pylog4net
? multiprocessing.SimpleQueue         imported from concurrent.futures.process
? netbios                             imported from uuid
? win32evtlog                         imported from logging.handlers
? win32evtlogutil                     imported from logging.handlers
? win32wnet                           imported from uuid
```

### Configuration
Runtime configuration file is: src/Net2Scripting.exe.config
(complies to the dotnet standard)

### Version updates
To update the version number, adjust the following files:
 * inno_script.iss
 * src/settings.py
 * docs/README.txt

### License
MIT
