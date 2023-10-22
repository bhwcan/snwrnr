@echo off
setlocal
IF %1==1 SET "savefile=%EPICDATA%\CompleteSave.dat" & GOTO APP
IF %1==2 SET "savefile=%EPICDATA%\CompleteSave1.dat." & GOTO APP
IF %1==3 SET "savefile=%EPICDATA%\CompleteSave2.dat" & GOTO APP
if %1==4 SET "savefile=%EPICDATA%\CompleteSave3.dat" & GOTO APP
echo ... not valid slot ...
GOTO END
:APP
%PYTHON% %SNSRC%\settruck.py %savefile% %2
:END
endlocal
