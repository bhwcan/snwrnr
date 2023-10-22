@ECHO OFF
CALL snvars.bat
%PYTHON% %SNSRC%\restoreslot.py %EPICDATA% %SNBACKUP% %1 %2
