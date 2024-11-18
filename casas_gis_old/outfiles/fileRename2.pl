#!/usr/local/bin/perl
#
# Usage: perl fileNewName.pl perlexpr [files]
# Example: fileRename2.pl "s/med//" *.txt

# Author: Luigi Ponti
# SPDX-License-Identifier: GPL-2.0-or-later

use File::Glob qw(:glob);

($regexp = shift @ARGV) || die "Usage:  rename perlexpr [filenames]\n";

if (!@ARGV) {
   @ARGV = <STDIN>;
   chomp(@ARGV);
}


foreach $_ (bsd_glob(@ARGV, GLOB_NOCASE)) {
   $old_name = $_;
   eval $regexp;
   die $@ if $@;
   rename($old_name, $_) unless $old_name eq $_;
}

exit(0);
