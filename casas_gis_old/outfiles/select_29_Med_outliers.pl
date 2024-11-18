#!/usr/bin/perl -w
# Script that removes lines with a certain regex by writing

# Author: Luigi Ponti quartese gmail.com
# COPYRIGHT: (c) 2009 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 20 July 2009

use strict;
use Cwd;

my $mainDir = cwd;

# Import weather files for reading.
opendir(DIR, "$mainDir") || die "can't opendir $mainDir: $!";
# Read files.
while (my $file = readdir(DIR))
{
	if ($file =~ /.\.txt/)
	{
        my $outfile = "cln"."$file";
        open (OUTFILE, ">$outfile") or die "Can't open $outfile for writing: $!";
        open (IN, "<$file") or die "Can't open $file for reading: $!";
        while (<IN>)
        {
            # Go to next line unless it includes some strings.
            # Below a list of strings to prevent "Gibraltar overshooting".
            next if $_ =~ /grid_100_60|grid_104_67|grid_108_43|grid_109_62|grid_110_66|grid_113_66|grid_128_44|grid_140_52|grid_143_39|grid_14_80|grid_16_85|grid_18_63|grid_60_60|grid_62_78|grid_70_45|grid_76_88|grid_91_73|grid_92_70|grid_96_66|grid_97_63|grid_99_65|grid_19_63|grid_19_64|grid_137_66|grid_130_62|grid_12_77|grid_123_79|grid_114_62|grid_125_64/;
            # Write new file without lines that include regular expressions.
            print OUTFILE "$_";
        }
    close OUTFILE;
    close IN;     
    }
}

closedir DIR;
