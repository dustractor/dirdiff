@echo off
set PATH=%HOMEDRIVE%%HOMEPATH%\ANACON~1;%PATH%
set PYTHONHOME=%HOMEDRIVE%%HOMEPATH%\anaconda3
call conda activate
%PYTHONHOME%\pythonw.exe .\dirdiff.py --path d:\zSamples --path e:\zSamples
