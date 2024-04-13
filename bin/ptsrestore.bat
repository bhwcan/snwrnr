@ECHO OFF
CALL snvars.bat
%PYTHON% %SNSRC%\restoreslot.py %PTSDATA% %SNBACKUP% %1 %2
