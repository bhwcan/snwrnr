@echo off
CALL snvars.bat
setlocal
IF %1==1 SET "savefile=%PTSDATA%\CompleteSave.dat" & GOTO APP
IF %1==2 SET "savefile=%PTSDATA%\CompleteSave1.dat." & GOTO APP
IF %1==3 SET "savefile=%PTSDATA%\CompleteSave2.dat" & GOTO APP
if %1==4 SET "savefile=%PTSDATA%\CompleteSave3.dat" & GOTO APP
echo ... not valid slot ...
GOTO END
:APP
%PYTHON% %SNSRC%\settruck.py %savefile% %2
:END
endlocal
