
@ECHO OFF
echo Simple set up for Snowrunner scripts
echo ------------------------------------
rem Tries to find Epic, PTS, and Steam installs
rem Works fine on default single user installs however any deviation or added folders
rem can break it
set TOPDIR=snwrnr
set BINDIR=bin
set SRCDIR=src
set BACDIR=backup
echo Setting up top level directory "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%"
if not exist "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\" mkdir "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%"
echo Setting up bin directory for Windows batch files "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%"
if not exist "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\" mkdir "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%"
echo Setting up src directory for python scripts "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%SRCDIR%"
if not exist "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%SRCDIR%\" mkdir "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%SRCDIR%"
echo Setting up backup directory for saving game slots "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BACDIR%"
if not exist "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BACDIR%\" mkdir "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BACDIR%"
echo Creating snhome.bat to take you back to your home directory
echo @ECHO OFF > "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snhome.bat"
echo %%HOMEDRIVE%% >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snhome.bat"
echo CD %%HOMEPATH%% >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snhome.bat"
echo Checking if path variable is set up for the bin directory
call snhome.bat
IF ERRORLEVEL 1 GOTO :NOPATH
GOTO :SETVARS
:NOPATH
setx PATH "%PATH%;%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%"
IF ERRORLEVEL 1 GOTO :NOSETX
GOTO :SETVARS
:NOSETX
echo Manually set path to "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%" and rerun
GOTO :END
:SETVARS
echo Setting up snvars.bat to contain the paths to SnowRunner installations
echo rem Global variables may need tweaking do not rerun snenv.bat or it will lose changes > "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo set SNBACKUP="%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BACDIR%">> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo set SNSRC="%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%SRCDIR%">> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo python --version
python --version
IF ERRORLEVEL 1 GOTO :PY
echo set PYTHON=python>> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
GOTO :SETEPIC
:PY
echo py --version
py --version
IF ERRORLEVEL 1 GOTO :NOPY
echo set PYTHON=py>> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
GOTO :SETEPIC
:NOPY
echo Unable to find python please install and rerun
GOTO :END
:SETEPIC
echo Searching for Epic install
set EP="%HOMEDRIVE%%HOMEPATH%\Documents\My Games\SnowRunner\base\storage"
set name=none
for /f  "delims==" %%i in ('dir /ad /b %EP%\*')  do (
    if not "%%i"=="backupSlots" set name=%%i
)
if %name% == none GOTO :SETPTS
echo Found Epic creating snepic.bat to take you to the save files
echo set EPICDATA="%HOMEDRIVE%%HOMEPATH%\Documents\My Games\SnowRunner\base\storage\%name%">> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo @ECHO OFF > "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snepic.bat"
echo CALL snvars.bat >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snepic.bat"
echo IF %%ERRORLEVEL%% NEQ 0 EXIT /b 1 >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snepic.bat"
echo CD /D "%%EPICDATA%%" >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snepic.bat"
:SETPTS
echo Seaching for PTS installation
set EP="%HOMEDRIVE%%HOMEPATH%\Documents\My Games\SnowRunnerBeta\base\storage"
set name=none
for /f  "delims==" %%i in ('dir /ad /b %EP%\*')  do (
    if not "%%i"=="backupSlots" set name=%%i
)
if %name% == none GOTO :SETSTEAM
echo Found PTS creating snpts.bat to take you to the save files
echo set PTSDATA="%HOMEDRIVE%%HOMEPATH%\Documents\My Games\SnowRunnerBeta\base\storage\%name%">> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo @ECHO OFF > "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snpts.bat"
echo CALL snvars.bat >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snpts.bat"
echo IF %%ERRORLEVEL%% NEQ 0 EXIT /b 1 >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snpts.bat"
echo CD /D "%%PTSDATA%%" >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snpts.bat"
:SETSTEAM
echo Searching for Steam installation
set EP="C:\Program Files (x86)\Steam\userdata"
set name=none
for /f  "delims==" %%i in ('dir /ad /b %EP%\*')  do (
    set name=%%i
)
if %name% == none GOTO :END
echo Found Steam creating snsteam.bat to take you to the save files
echo set STEAMDATA="C:\Program Files (x86)\Steam\userdata\%name%\1465360\remote">> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snvars.bat"
echo @ECHO OFF > "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snsteam.bat"
echo CALL snvars.bat >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snsteam.bat"
echo IF %%ERRORLEVEL%% NEQ 0 EXIT /b 1 >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snsteam.bat"
echo CD /D "%%STEAMDATA%%" >> "%HOMEDRIVE%%HOMEPATH%\%TOPDIR%\%BINDIR%\snsteam.bat"
:END
echo Done.
pause
EXIT /b 0
