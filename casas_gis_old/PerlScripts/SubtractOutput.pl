#!/usr/bin/perl -w
# Script developed to calculate the difference
# between observed and warming weather scenarios
# in CASAS model outputs. NOTE: the script is supposed
# to use files with the same number of rows & columns.

# Author: Luigi Ponti
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 22 January 2008

# Syntax:
# perl SubtractOutput.pl [directory where files are] [warming file] [observed file] [new file]
# Example:
# perl SubtractOutput.pl "C:/models/oliveGIS/" Olive_17gen08_AvgPlus3.txt Olive_17gen08_AvgObs.txt Olive_17gen08_AvgDiff3.txt

use strict;

# Read arguments.
my $workDir = $ARGV[0];
my $warmFile = $ARGV[1];
my $obsFile = $ARGV[2];
my $diffFile = $ARGV[3];

# Set variables.
my @warmTable;
my @obsTable;
my @diffTable;
my @warmTableRow;
my @obsTableRow;
my @diffTableRow;

# Read warmer weather file.
chdir ("$workDir"); 
open (WARM, "<$warmFile") or die "Can't open $warmFile for reading: $!";
while (my $line = <WARM>)
{
	$line =~ s/\s+$//;
	push(@warmTable, $line);
}
close WARM;

# Read observed weather file.
open (OBS, "<$obsFile") or die "Can't open $obsFile for reading: $!";
while (my $line = <OBS>)
{
	$line =~ s/\s+$//;
	push(@obsTable, $line);
}
close OBS;

# Copy headers to table for new file.
$diffTable[0] = $obsTable[0];

# How many rows in input files (should be the same for both)?
my $numRows = scalar @obsTable;
# Define a variable for number of columns.
my $numCols;
# Perform subtraction.
for (my $row = 1; $row < $numRows; $row++)
{
	@warmTableRow = split(/\t/, $warmTable[$row]);
	@obsTableRow = split(/\t/, $obsTable[$row]);
	# How many columns do we have?
	if ($row == 1)
	{
		$numCols = scalar @warmTableRow;
		print "$numCols\n\n";
	}
	# First 11 column should not be different -- nothing to compute.
	for (my $col = 0; $col < 11; $col++)
	{
		# Use the value of the observed weather file for the new file.
		$diffTableRow[$col] = $obsTableRow[$col];
	}
	# The rest of the columns need computations only if numeric.
	for (my $col = 11; $col < $numCols; $col++)
	{
		if ($warmTableRow[$col] !~ /[a-zA-Z]/) # If there is no letter in the cell.
		{
			# Get the difference and put that in the new table.
			$diffTableRow[$col] = $warmTableRow[$col] - $obsTableRow[$col];			
		}
		else
		{
			# Just use the value of the observed weather file.
			$diffTableRow[$col] = $obsTableRow[$col];
		}
	}
	# Now join the new table row.
	$diffTable[$row] = join("\t", @diffTableRow);	
	# And reset temporary rows.
	@warmTableRow = ();
	@obsTableRow = ();
	@diffTableRow = ();
}
# Save new file which contains differences.
open (OUTFILE, ">$diffFile") or die "Can't open $diffFile for writing: $!";
print OUTFILE join ("\r\n", @diffTable); 
print OUTFILE "\r\n";
close OUTFILE;
