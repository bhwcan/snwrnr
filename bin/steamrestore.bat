@ECHO OFF
CALL snvars.bat
%PYTHON% %SNSRC%\restoreslot.py %STEAMDATA% %SNBACKUP% %1 %2
CALL sncache.bat
