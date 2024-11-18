@echo off
REM Author: Luigi Ponti
REM SPDX-License-Identifier: GPL-2.0-or-later

@set PATH=%GISBASE%\scripts\;C:\Program Files\Mozilla Firefox\;%PATH%
@"%GRASS_SH%" -c '"%HOME%/casas/grass_scripts/map.pbdm.andalusia" %*'
