@ECHO OFF
CALL snvars.bat
IF %ERRORLEVEL% NEQ 0 EXIT /b 1
IF NOT EXIST %PTSDATA%\CommonSslSave.dat (
   ECHO ... game files not found ...
   EXIT /b 1
)
%PYTHON% %SNSRC%\slots.py %PTSDATA%
