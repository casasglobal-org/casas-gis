REM Author: Luigi Ponti
REM SPDX-License-Identifier: GPL-2.0-or-later

for %%f in (*.txt) do perl -pi.bak -e "s/\//Per/g" %%f
