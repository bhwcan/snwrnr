@ECHO OFF 
CALL snvars.bat 
IF %ERRORLEVEL% NEQ 0 EXIT /b 1 
CD /D "%PTSDATA%" 
