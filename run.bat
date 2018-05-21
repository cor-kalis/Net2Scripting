@echo off
cd src
:again
c:\WinPrg\Python34\python Net2Scripting.py %1
pause
goto again
