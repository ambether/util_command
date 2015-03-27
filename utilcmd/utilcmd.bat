@echo off
set /p args=<args.txt
set filename=utilcmd.zip
echo Executing %filename%!!
%PYPATH%  %filename% %args%
pause 