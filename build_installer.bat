@echo off
del dist_installer\* /s/q > nul

rem taskkill /IM explorer.exe /F
rem cd /d %userprofile%\AppData\Local
rem del IconCache.db /a
rem start explorer.exe

"C:\Program Files\Inno Setup 5\ISCC.exe" inno_script.iss
pause
