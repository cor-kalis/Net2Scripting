@echo off

echo --- Cleaning...
del build\* /s/q > nul
del dist\* /s/q > nul
del docs\*.html /s/q > nul
echo --- Cleaning done

echo --- Generating docs
cd src
c:/WinPrg/Python34/python docgen.py
cd ..
echo --- Generating docs done

echo --- Building executable
cd src
c:/WinPrg/Python34/python setup.py py2exe
cd ..
echo --- Building executable done

pause
