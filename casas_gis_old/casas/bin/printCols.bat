@echo off
REM Author: Luigi Ponti
REM SPDX-License-Identifier: GPL-2.0-or-later

@set PATH=%GISBASE%\scripts\;C:\Program Files\Mozilla Firefox\;%PATH%
@perl "%HOME%/PerlScripts/printCols.pl" "%HOME%"
