@echo off
setlocal
IF %2==1 SET "savefile=CompleteSave." & SET "stsfile=sts" & SET "fogfile=fog" & SET "fieldfile=field" & GOTO PLATFORM
IF %2==2 SET "savefile=CompleteSave1." & SET "stsfile=1_sts" & SET "fogfile=1_fog" & SET "fieldfile=1_field" & GOTO PLATFORM
IF %2==3 SET "savefile=CompleteSave2." & SET "stsfile=2_sts" & SET "fogfile=2_fog" & SET "fieldfile=2_field" & GOTO PLATFORM
if %2==4 SET "savefile=CompleteSave3." & SET "stsfile=3_sts" & SET "fogfile=3_fog" & SET "fieldfile=3_field" & GOTO PLATFORM
echo ... not valid slot ...
GOTO END
:PLATFORM
IF %1==steam GOTO STEAMDIR
IF %1==epic GOTO EPICDIR
IF %1==pts GOTO PTSDIR
echo ... not valid platform ...
GOTO END
:STEAMDIR
IF NOT EXIST %HOMEDRIVE%%HOMEPATH%\bin\snsteam.bat (
   echo .. not installed ...
   GOTO END
)
CALL %HOMEDRIVE%%HOMEPATH%\bin\snsteam.bat
IF %ERRORLEVEL% NEQ 0 EXIT /b 1
GOTO LISTFILES
:EPICDIR
IF NOT EXIST %HOMEDRIVE%%HOMEPATH%\bin\snepic.bat (
   echo .. not installed ...
   GOTO END
)
CALL %HOMEDRIVE%%HOMEPATH%\bin\snepic.bat
IF %ERRORLEVEL% NEQ 0 EXIT /b 1
GOTO LISTFILES
:PTSDIR
IF NOT EXIST %HOMEDRIVE%%HOMEPATH%\bin\snpts.bat (
   echo .. not installed ...
   GOTO END
)
CALL %HOMEDRIVE%%HOMEPATH%\bin\snpts.bat
IF %ERRORLEVEL% NEQ 0 EXIT /b 1
GOTO LISTFILES
:LISTFILES
DIR "%savefile%*"
DIR "%stsfile%*"
DIR "%fogfile%*"
DIR "%fieldfile%*"
:PROMPT
SET /P AREYOUSURE=Are you sure (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END
DEL "%savefile%*"
DEL "%stsfile%*"
DEL "%fogfile%*"
DEL "%fieldfile%*"
:END
endlocal
