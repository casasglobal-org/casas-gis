#!/bin/bash
# set -x
############################################################################
#
# MODULE:       subtract.sh
#
# AUTHOR(S):    Luigi Ponti
#
# PURPOSE:      Makes a CASAS-mappable file subracting two model
#                      output files one from the other.
#
# NOTE:
#
#
# Copyright:    (c) 2008 Luigi Ponti, quartese at gmail.com
#                   CASAS (Center for the Analysis of Sustainable
#                   Agricultural Systems, https://www.casasglobal.org/)
#
#                   SPDX-License-Identifier: GPL-2.0-or-later
#
#############################################################################

# %Module
# % description: Makes a CASAS-mappable file subtracting two model output files
# % keyword: model
# % keyword: CASAS
# % keyword: subtraction
# %End
# %option
# % key: workDir
# % type: string
# % answer: /home/andy/outfiles/
# % gisprompt: old_file,file,input
# % description: Directory with input files
# % required: yes
# %End
# %option
# % key: warmFile
# % type: string
# % gisprompt: old_file,file,input
# % description: Warmed weather file
# % required: yes
# %End
# %option
# % key: obsFile
# % type: string
# % gisprompt: old_file,file,input
# % description: Observed weather file
# % required: yes
# %End
# %option
# % key: diffFile
# % type: string
# % gisprompt: new_file,file,output
# % description: New output file
# % required: yes
# %End

if [ -z "$GISBASE" ]; then
    echo "You must be in GRASS GIS to run this program." 1>&2
    exit 1
fi

if [ "$1" != "@ARGS_PARSED@" ]; then
    exec g.parser "$0" "$@"
fi

if [ -n "$GIS_OPT_workDir" ]; then
    workDir=$GIS_OPT_workDir
fi

if [ -n "$GIS_OPT_warmFile" ]; then
    warmFile=$GIS_OPT_warmFile
fi

if [ -n "$GIS_OPT_obsFile" ]; then
    obsFile=$GIS_OPT_obsFile
fi

if [ -n "$GIS_OPT_diffFile" ]; then
    diffFile=$GIS_OPT_diffFile
fi

perl ../PerlScripts/SubtractOutputGui.pl "$workDir" "$warmfile" "$obsFile" "$diffFile"
