REM Author: Luigi Ponti quartese gmail.com
REM Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later
REM Date: 16 December 2011

REM Make difference files for MedOlive major revision manuscript

:: ERA40 no fly
perl SubtractOutput.pl "" Olive_08dic11_Avg_ERA40_pl2_noFly.txt Olive_08dic11_Avg_ERA40_obs_noFly.txt Olive_08dic11_Avg_ERA40_Delta_noFly.txt
:: ERA40 with fly
perl SubtractOutput.pl "" Olive_08dic11_Avg_ERA40_pl2_withFly.txt Olive_08dic11_Avg_ERA40_obs_withFly.txt Olive_08dic11_Avg_ERA40_Delta_withFly.txt
:: EH5OM no fly
perl SubtractOutput.pl "" Olive_12dic11_Avg_EH5OM_A1B_noFly.txt Olive_12dic11_Avg_EH5OM_20C_noFly.txt Olive_12dic11_Avg_EH5OM_Delta_noFly.txt
:: EH5OM with fly
perl SubtractOutput.pl "" Olive_12dic11_Avg_EH5OM_A1B_withFly.txt Olive_12dic11_Avg_EH5OM_20C_withFly.txt Olive_12dic11_Avg_EH5OM_Delta_withFly.txt
