@ECHO OFF
CALL snvars.bat
IF %ERRORLEVEL% NEQ 0 EXIT /b 1
%PYTHON% %SNSRC%\copytruck.py %1 %2 %3
