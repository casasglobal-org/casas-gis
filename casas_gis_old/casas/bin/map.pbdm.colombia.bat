@echo off
REM Author: Luigi Ponti quartese gmail.com
REM Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later

@set PATH=%GISBASE%\scripts\;C:\Program Files\Mozilla Firefox\;%PATH%
@"%GRASS_SH%" -c '"%HOME%/casas/grass_scripts/map.pbdm.colombia" %*'
