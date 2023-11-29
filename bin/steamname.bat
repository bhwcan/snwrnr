@echo off
setlocal
IF %1==1 SET "savefile=%STEAMDATA%\CompleteSave.cfg" & GOTO APP
IF %1==2 SET "savefile=%STEAMDATA%\CompleteSave1.cfg." & GOTO APP
IF %1==3 SET "savefile=%STEAMDATA%\CompleteSave2.cfg" & GOTO APP
if %1==4 SET "savefile=%STEAMDATA%\CompleteSave3.cfg" & GOTO APP
echo ... not valid slot ...
GOTO END
:APP
%PYTHON% %SNSRC%\settruck.py %savefile% %2
:END
endlocal
