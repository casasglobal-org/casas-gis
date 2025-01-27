#!/usr/bin/perl -w
use strict;
############################################################################
#
# MODULE:       diff.pl
#
# AUTHOR(S):    Luigi Ponti
#
# PURPOSE:      Makes a CASAS-mappable file by subracting two model
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
# % description: Makes a CASAS-mappable file subracting two model output files
# %End

# %option
# % key: working_directory
# % type: string
# % answer: /home/andy/outfiles/
# % gisprompt: old_file,file,input
# % description: Directory where input files are
# % required: yes
# %end

# %option
# % key: warmest_file
# % type: string
# % gisprompt: old_file,file,input
# % description: Warmed weather file
# % required: yes
# %end

# %option
# % key: observed_file
# % type: string
# % gisprompt: old_file,file,input
# % description: Observed weather file
# % required: yes
# %end

# %option
# % key: diff_file
# % type: string
# % gisprompt: new_file,file,output
# % description: New output file
# % required: yes
# %end

if (!$ENV{'GISBASE'})
{
    printf(STDERR  "You must be in GRASS GIS to run this program.\n");
    exit 1;
}

if ($ARGV[0] ne '@ARGS_PARSED@')
{
    my $arg = "";
    for (my $i=0; $i < @ARGV; $i++)
	{
        $arg .= " $ARGV[$i] ";
    }
    system("$ENV{GISBASE}/bin/g.parser $0 $arg");
    exit;
}

if ( $ENV{'GIS_OPT_workDir'} eq "1" )
{
	my $workDir = $ENV{'GIS_OPT_workDir'};
}

if ( $ENV{'GIS_OPT_warmFile'} eq "1" )
{
	my $warmFile =  $ENV{'GIS_OPT_warmFile'};
}

if ( $ENV{'GIS_OPT_obsFile'} eq "1" )
{
	my $obsFile = $ENV{'GIS_OPT_obsFile'};
}

if ( $ENV{'GIS_OPT_diffFile'} eq "1" )
{
	my $diffFile = $ENV{'GIS_OPT_diffFile'};
}

# Read arguments.
my $workDir = $ENV{'GIS_OPT_workDir'};
my $warmFile = $ENV{'GIS_OPT_warmFile'};
my $obsFile = $ENV{'GIS_OPT_obsFile'};
my $diffFile = $ENV{'GIS_OPT_diffFile'};

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
