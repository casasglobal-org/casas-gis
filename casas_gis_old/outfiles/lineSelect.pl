#!/usr/bin/perl -w
# Script that select lines with a certain regex.
# This one selects grid points inside olive growing
# area (803 grid points result in 754 records because
# some of them were removed previously with
# lineRmove.pl being actrually sea location).

# Author: Luigi Ponti quartese gmail.com
# COPYRIGHT: (c) 2010 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 3 July 2010

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
        my $outfile = "ita_"."$file";
        open (OUTFILE, ">>$outfile") or die "Can't open $outfile for writing: $!";
        open (IN, "<$file") or die "Can't open $file for reading: $!";
        while (<IN>)
        {
            # Go to next line unless it includes some strings.
            # The string "Model" is to include header line.
            next unless $_ =~ /Model|ITA/;
            # Write new file without lines that include regular expressions.
            print OUTFILE "$_";
        }
    close OUTFILE;
    close IN;     
    }
}

closedir DIR;


