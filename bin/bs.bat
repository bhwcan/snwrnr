@ECHO OFF
rem bs is for backup slots
CALL snvars.bat
set basename="ERROR"
for /f "delims=" %%i in ('%PYTHON% %SNSRC%\getname.py %SNBACKUP% %1') do set basename=%%i
IF "%basename%"=="ERROR" GOTO ERROR
ECHO %basename%
%PYTHON% %SNSRC%\slots.py "%SNBACKUP%\%basename%" 1
GOTO END
:ERROR
ECHO "Unable to find backup [%1]"
:END
