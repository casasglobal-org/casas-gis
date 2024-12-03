:: Recreates GisFilesList.txt
@echo off

REM Author: Luigi Ponti quartese gmail.com
REM Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later

dir /B *txt | find /V /I "GisFilesList.txt" > GisFilesList.txt
