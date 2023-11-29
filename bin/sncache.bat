@ECHO OFF
tasklist /FI "IMAGENAME eq steam.exe" | find "steam.exe"
IF ERRORLEVEL 1 GOTO :BUILD
ECHO Steam is running unable to generate remotecache.vdf
EXIT /b 1
:BUILD
CALL snvars.bat
%PYTHON% %SNSRC%\sncache.py %STEAMDATA%
EXIT /b 0
