@echo off
REM Author: Luigi Ponti quartese gmail.com
REM Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later

for /L %%G in (1,1,10) do (
if %%G EQU 3 (
echo %%G
) else (
echo %%G is not 3
)
)
