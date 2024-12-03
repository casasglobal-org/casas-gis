@echo off
REM Author: Luigi Ponti quartese gmail.com
REM Copyright: (c) 2011 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
REM SPDX-License-Identifier: GPL-2.0-or-later

c:\cygwin\bin\mount -f -s -b "C:/cygwin/bin" "/usr/bin"
c:\cygwin\bin\mount -f -s -b "C:/cygwin/lib" "/usr/lib"
c:\cygwin\bin\mount -f -s -b "C:/cygwin" "/"
c:\cygwin\bin\mount -s -b --change-cygdrive-prefix "/cygdrive"
