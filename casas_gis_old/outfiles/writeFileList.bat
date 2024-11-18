:: Recreates GisFilesList.txt
@echo off

REM Author: Luigi Ponti
REM SPDX-License-Identifier: GPL-2.0-or-later

dir /B *txt | find /V /I "GisFilesList.txt" > GisFilesList.txt
