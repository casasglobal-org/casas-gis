#!/usr/bin/perl -w
# Script developed to fix problem with Protheus
# climate data in CASAS model outputs. 
# Problem is due to 6-hourly data (e.g. precipitation) 
# needing to be averaged rather than summed up to get
# daily values. This holds true also for Solar Radiation,
# which was however already averaged during wx file
# compilation.

# Author: Luigi Ponti
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 3 June 2010

# Syntax:
# perl DivPrcpBy4.pl [input file]

# In DOS loop for multiple files:
# for %v in (cln*) do perl DivPrcpBy4.pl "%v"

use strict;
use Cwd;

my  $workDir = cwd;

# Read arguments.
my $inputFile = $ARGV[0];
my $outputFile = "prcpDivBy4" . $inputFile;

# Set variables.
my @inputTable;
my @outputTable;
my @inputTableRow;
my @outputTableRow;
my @ColumnNames;

# Read input file.
chdir ("$workDir"); 
open (INPUT, "<$inputFile") or die "Can't open$inputFile for reading: $!";
while (my $line = <INPUT>)
{
	$line =~ s/\s+$//;
	push(@inputTable, $line);
}
close INPUT;
# Copy headers to table for new file.
$outputTable[0] = $inputTable[0];
@ColumnNames = split(/\t/, $inputTable[0]);

# How many rows in input files?
my $numRows = scalar @inputTable;
print "\nNumber of rows is $numRows\n";
# Define a variable for number of columns.
my $numCols;
# Perform division.
for (my $row = 1; $row < $numRows; $row++)
{
	@inputTableRow = split(/\t/, $inputTable[$row]);
	# How many columns do we have?
	if ($row == 1)
	{
		$numCols = scalar @inputTableRow;
		print "\nNumber of columns is $numCols\n";
	}
	# Loop trough columns.
	for (my $col = 0; $col <  $numCols; $col++)
	{
		if ($ColumnNames[$col] eq "PrcpYrSum")
        {
        # Divide precipitation by four.
		$outputTableRow[$col] = $inputTableRow[$col] / 4;           
        }
        else
        {
        # Replace value in output table.
		$outputTableRow[$col] = $inputTableRow[$col];          
        }
	}
	# Now join the new table row.
	$outputTable[$row] = join("\t", @outputTableRow);	
	# And reset temporary rows.
	@inputTableRow = ();
	@outputTableRow = ();
}
# Save output file.
open (OUTFILE, ">$outputFile") or die "Can't open $outputFile for writing: $!";
print OUTFILE join ("\n", @outputTable); 
print OUTFILE "\n";
close OUTFILE;
