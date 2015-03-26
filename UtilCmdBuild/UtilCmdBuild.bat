@echo off
set /p args=<args.txt
set filename=UtilCmdBuild.zip
echo Executing %filename%!!
%PYPATH%  %filename% %args%
pause 