@echo off
REM Author: Luigi Ponti quartese gmail.com
REM COPYRIGHT: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later

REM ~ Glynn Clements's suggestion:
REM ~ If you start MSys via the msys.bat it will set PATH, but it will also
REM ~ run in an rxvt Window, which is rather unreliable.

REM ~ I suggest creating a batch file, e.g.:

	REM ~ set HOME=%HOMEDRIVE%%HOMEPATH%
	REM ~ set PATH=C:\msys\1.0\bin;C:\MinGW\bin;%PATH%
	REM ~ start C:\msys\1.0\bin\sh.exe

REM ~ Change the paths as appropriate for your system.

REM ~ That will start a shell in a command window. From there, you will need
REM ~ to start GRASS before you can use any GRASS commands.

rem Set language to untranslated strings
rem See http://osgeo-org.1803224.n2.nabble.com/v-in-ascii-fails-with-long-text-file-in-WinGRASS-6-4-0-1-tp5530777p5558403.html
set LC_ALL=C
set LANG=C

rem Set GRASS Installation Directory Variable
set GRASSDIR=C:\Program Files (x86)\GRASS GIS 6.4.4

set GISBASE=C:/Program Files (x86)/GRASS GIS 6.4.4

rem Directory where your .grassrc6 file will be stored
set HOME=C:\cygwin\home\andy

rem Name of the wish (Tk) executable
set GRASS_WISH=wish.exe
set GRASS_GUI=tcltk

rem Path to the shell command
set GRASS_SH=%GRASSDIR%\msys\bin\sh.exe

rem Path to the proj files (notably the epsg projection list)
set GRASS_PROJSHARE=%GRASSDIR%\proj

rem Path to the python directory
set PYTHONHOME=%GRASSDIR%\Python25
if "x%GRASS_PYTHON%" == "x" set GRASS_PYTHON=python

rem Default browser
set GRASS_HTML_BROWSER=firefox

rem Firefox is used in the CASAS script.
set PATH=C:\Program Files\Mozilla Firefox;%PATH%

rem Set Path to utilities (libraries and bynaries) used by GRASS
set PATH=%GRASSDIR%\msys\bin;%PATH%
set PATH=%GRASSDIR%\extrabin;%GRASSDIR%\extralib;%PATH%
set PATH=%GRASSDIR%\tcl-tk\bin;%GRASSDIR%\sqlite\bin;%GRASSDIR%\sqlite\lib;%PATH%
set PATH=%GRASSDIR%\gpsbabel;%PATH%
set PATH=%GRASSDIR%\bin;%GRASSDIR%\lib;%PATH%
set PATH=%GRASSDIR%\scripts;%GRASSDIR%\etc;%PATH%
set PATH=%GRASSDIR%\sqlite\lib;%GRASSDIR%\sqlite\bin;%PATH%

rem CASAS stuff
set PATH=%HOME%\casas\bin;%HOME%\casas\grass_scripts;%PATH%
set GRASS_ADDON_PATH=%HOME%\casas\bin
set GRASS_ADDON_ETC=C:\cygwin\home\andy\casas\etc

rem Set GRASS message format.
rem set GRASS_MESSAGE_FORMAT=silent

set GIS_LOCK=1
set GRASS_VERSION=6.4.4

set WD=%HOMEDRIVE%%HOMEPATH%\AppData\Roaming\GRASS6
set UNIQUE=%RANDOM%
set GISRC=%WD%\grassrc6
REM ~ set GISRC=%WD%\gisrc_%UNIQUE%
REM ~ copy %WD%\.grassrc6 %GISRC%

cd C:\cygwin\home\andy

echo  ************************************
echo    GRASS shell for Andalusia
echo    running through a DOS box.
echo    For batch process, please type:
echo    "C:\Program Files (x86)\GRASS GIS 6.4.4\msys\bin\sh.exe" batch_olive_andalusia.sh
echo  ************************************
echo.


cmd.exe



