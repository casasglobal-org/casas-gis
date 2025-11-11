#!/usr/bin/perl -w
# http://ekawas.blogspot.com/2008/11/perl-script-to-rename-your-files.html

# Authors: Edward Kawas, Luigi Ponti quartese gmail.com
# SPDX-License-Identifier: GPL-2.0-or-later

# e.g. 
# for %v in (*.txt) do perl fileRename.pl -u "s/cln//g" "%v"

BEGIN {
 use Getopt::Std;
 use vars qw/ $opt_h $opt_u /;
 getopt;

 # usage
        sub usage {
  print STDOUT <<'END_OF_USAGE';

  Usage: rename [-hu] sub_regex [files]

                sub_regex is any expression that you would like to
                apply to filename. You can use capturing or just 
                matching.

                -h .... shows this message ;-)
                -u .... makes first letter of each word uppercase

  examples:

                1.
         perl rename.pl "s/_/ /g" rename_me.txt
                   This renames rename_me.txt to "rename me.txt"

                2.
         perl rename.pl -u "s/_/ /g" rename_me.txt
                   This renames rename_me.txt to "Rename Me.txt"

                3. MS Windows example
         for %v in (*.mp3) do perl rename.pl -u "s/_/ /g" "%v"
                   This renames all mp3 files in the current directory such that
                   every word begins with a capital letter and all underscores
                   are replaced with spaces.


END_OF_USAGE

}
 if ($opt_h) {
                usage();
  exit(0);
 }

}

# get the substitution regex
$op = shift or (usage() and exit(1));

# go through file names
chomp(@ARGV = <STDIN>) unless @ARGV;
for (@ARGV) {
    $was = $_;
    eval $op;
    die $@ if $@;
    # cap first letter of each word
    my $newname = "";
    my @components = split(/ /, $_);
	print $_;
    foreach (@components) {
      my $x = $_;
      $x = ucfirst lc $x if $opt_u;
      $newname .= "$x";
    }
    rename($was,$newname) unless $was eq $newname;
}
