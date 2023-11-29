@ECHO OFF
CALL snvars.bat
set basename="ERROR"
for /f "delims=" %%i in ('%PYTHON% %SNSRC%\nextname.py %SNBACKUP% %2') do set basename="%%i"
IF %basename%=="ERROR" GOTO ERROR
rem ECHO %basename%
%PYTHON% %SNSRC%\backupslot.py %STEAMDATA% %SNBACKUP% %1 %basename%
GOTO END
:ERROR
ECHO "Unable to backup [%2]"
:END