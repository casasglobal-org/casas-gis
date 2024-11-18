@echo off
REM Author: Luigi Ponti
REM SPDX-License-Identifier: GPL-2.0-or-later

for /L %%G in (1,1,10) do (
if %%G EQU 3 (
echo %%G
) else (
echo %%G is not 3
)
)
