#!/usr/bin/perl -w
# Script that writes color rules file based on a list 
# of colors and the range of data.

# Can use any combination of colors.
# The central color may be placed at an arbitrary value ($scaleCenter).
# getBoxplotColorRule.pl whiskerLow whiskerHigh absMin absMax zeroCentered(divNo|divYes) rasterMapName

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2013 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 14 October 2013

use strict;
use Cwd;

# Set some variables.
my $HomeDir = cwd;

# Color list.
# GMT_panoply.cpt
my $rule ="255:255:204-217:240:163-217:240:163-173:221:142-173:221:142-120:198:121-120:198:121-65:171:93-65:171:93-35:132:67-35:132:67-0:90:50"
;
# https://www.colorspire.com/rgb-color-wheel/
my $outlierLow = "255:255:204";
my $outlierHigh = "0:90:50";

# See bottom of file for sample color strings.

# Cutting points.
my $lowCut = "na";
my $hiCut = "na";
# Position of central color.
my $scaleCenter = 0;
# Range of values.
my $min = $ARGV[0];
my $max = $ARGV[1];
# Whiskers for boxpolot.
my $absMin = $ARGV[2];
my $absMax = $ARGV[3];
# Divergent?
my $divergentRule = $ARGV[4];
# Reverse color order?
my $reverseColors = "no";
# Percent or absolute value?
my $percent = $ARGV[5];
# Map name
my $rasterMapName = $ARGV[6];

my $rule_file_header = "# Viridis modified from http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/viridis.cpt\n# to raster $rasterMapName\n";

my @table;
my @range;

# Check if cutting points influence the range.
if ($hiCut ne "na")
{
	$max = $hiCut if $hiCut < $max;
}
if ($lowCut ne "na")
{
    $min = $lowCut if $lowCut > $min;
}

# Initialize color rule file.
chdir ("$HomeDir");
my $output = "$rasterMapName" . '_boxplot_color_rule.txt';
print $output . "\n";

# Put colors into an array.
my @colors = split(/-/, $rule);
if ($reverseColors eq "yes")
{
    @colors = reverse(@colors)
}

# Compute number of colors and bands.
my $numOfColors = scalar @colors;
my $NumOfBands = $numOfColors - 1;
my $halfNumOfBands = int($NumOfBands / 2);

if ($divergentRule eq "divNo")
{
	# Build array of coefficients.
	my $baseCoeff = 1 / $NumOfBands;
	my @coefficients;
	push(@coefficients, $min);
	for (my $i = 1; $i <= ($NumOfBands - 1); $i++)
	{
		push(@coefficients, ($min + ($i * $baseCoeff * ($max - $min))))
	}
	push(@coefficients, $max);
	
	# Print color rule file.
    # Following code can be compressed a lot by using a string variable
    # in place of ' ' versue '% ' in case of absolute vs. percent rules.
	open (OUTFILE, ">$output") or die "Can't open $output for writing: $!";
    print OUTFILE $rule_file_header;
    if ($percent)
	{
        # Outlier low
        if ($absMin != $min)
        {
            print OUTFILE join('',  sprintf("%.3f", $absMin), '% ', "$outlierLow\n");
            print OUTFILE join('',  sprintf("%.3f", $min), '% ', "$outlierLow\n");
        }        
        # Non outlier part
        for (my $k = 0; $k < $numOfColors; $k++)
        {
            print OUTFILE join('',  sprintf("%.3f", $coefficients[$k]), '% ', "$colors[$k]\n");
            # print OUTFILE "$coefficients[$i]% $colors[$i]\n"
        }
        # Outlier high
        if ($absMax != $max)
        {
            print OUTFILE join('',  sprintf("%.3f", $max), '% ', "$outlierHigh\n");
            print OUTFILE join('',  sprintf("%.3f", $absMax), '% ', "$outlierHigh\n");
        }
        
    }
    else
    {
        # Outlier low
        if ($absMin != $min)
        {
            print OUTFILE join('',  sprintf("%.3f", $absMin), ' ', "$outlierLow\n");
            print OUTFILE join('',  sprintf("%.3f", $min), ' ', "$outlierLow\n");
        }
        # Non outlier part
        for (my $k = 0; $k < $numOfColors; $k++)
        {         
            print OUTFILE join('',  sprintf("%.3f", $coefficients[$k]), ' ', "$colors[$k]\n");
            # print OUTFILE "$coefficients[$i]% $colors[$i]\n"
        }
        # Outlier high
        if ($absMax != $max)
        {
            print OUTFILE join('',  sprintf("%.3f", $max), ' ', "$outlierHigh\n");
            print OUTFILE join('',  sprintf("%.3f", $absMax), ' ', "$outlierHigh\n");
        }        
    }
	print OUTFILE "end\n";
	close OUTFILE;
}
elsif ($divergentRule eq "divYes")
{
    my @coefficients;
    if ($min < 0)
    {    
        if ($scaleCenter == 0)
        {
            # Build array of coefficients.
            my $baseCoeff = 1 / $halfNumOfBands;
            push(@coefficients, $min);
            for (my $i = ($halfNumOfBands -1); $i >= 1; $i--)
            {
                push(@coefficients, ($i * $baseCoeff  * ($scaleCenter + $min)))
            }	
            if (($numOfColors % 2) == 1)
            {
                push(@coefficients, $scaleCenter)
            }
            else
            {
                push(@coefficients, ($scaleCenter, $scaleCenter))
            }
            for (my $i = 1; $i <= ($halfNumOfBands - 1); $i++)
            {
                push(@coefficients, ($i * $baseCoeff * ($max - $scaleCenter)))
            }
            push(@coefficients, $max);
        }
        elsif ($scaleCenter != 0) ## ARRIVED HERE put scale center where it belongs -- i.e. sort array
        {
            # Build array of coefficients.
            my $baseCoeff = 1 / $halfNumOfBands;
            push(@coefficients, $min);
            for (my $i = ($halfNumOfBands -1); $i >= 1; $i--)
            {
                push(@coefficients, ($i * $baseCoeff  * ($min - $scaleCenter)) + $scaleCenter)
            }	
            if (($numOfColors % 2) == 1)
            {
                push(@coefficients, $scaleCenter)
            }
            else
            {
                push(@coefficients, ($scaleCenter, $scaleCenter))
            }
            for (my $i = 1; $i <= ($halfNumOfBands - 1); $i++)
            {
                push(@coefficients, ($i * $baseCoeff * ($max - $scaleCenter)) + $scaleCenter)
            }
            push(@coefficients, $max);
        }
        
    }
    else
    {
        # Build array of coefficients.
        my $baseCoeff = 1 / ($halfNumOfBands );
        push(@coefficients, $min);
        for (my $i = 1; $i <= ($halfNumOfBands - 1); $i++)
        {
            push(@coefficients, ($i * $baseCoeff  * ($scaleCenter - $min)))
        }	
        if (($numOfColors % 2) == 1)
        {
            push(@coefficients, $scaleCenter)
        }
        else
        {
            push(@coefficients, ($scaleCenter, $scaleCenter))
        }
        for (my $i = 1; $i <= ($halfNumOfBands -1); $i++)
        {
            push(@coefficients, ($scaleCenter + ($i  * $baseCoeff * ($max - $scaleCenter))))
        }
        push(@coefficients, $max);
    }
	# Print color rule file.
	open (OUTFILE, ">$output") or die "Can't open $output for writing: $!";
    if ($percent)
	{
        # Outlier low
        if ($absMin != $min)
        {
            print OUTFILE join('',  sprintf("%.3f", $absMin), '% ', "$outlierLow\n");
            print OUTFILE join('',  sprintf("%.3f", $min), '% ', "$outlierLow\n");
        } 
        # Non outlier part
        for (my $k = 0; $k < $numOfColors; $k++)
        {
            print OUTFILE join('',  sprintf("%.3f", $coefficients[$k]), '% ', "$colors[$k]\n"); # Add % if needed
        }
        # Outlier high
        if ($absMax != $max)
        {
            print OUTFILE join('',  sprintf("%.3f", $max), '% ', "$outlierHigh\n");
            print OUTFILE join('',  sprintf("%.3f", $absMax), '% ', "$outlierHigh\n");
        }        
    }
    else
    {
        # Outlier low
        if ($absMin != $min)
        {
            print OUTFILE join('',  sprintf("%.3f", $absMin), ' ', "$outlierLow\n");
            print OUTFILE join('',  sprintf("%.3f", $min), ' ', "$outlierLow\n");
        }
        # Non outlier part
        for (my $k = 0; $k < $numOfColors; $k++)
        {
            print OUTFILE join('',  sprintf("%.3f", $coefficients[$k]), ' ', "$colors[$k]\n"); # Add % if needed
        }
        # Outlier high
        if ($absMax != $max)
        {
            print OUTFILE join('',  sprintf("%.3f", $max), ' ', "$outlierHigh\n");
            print OUTFILE join('',  sprintf("%.3f", $absMax), ' ', "$outlierHigh\n");
        }        
    }
	print OUTFILE "end\n";
	close OUTFILE;
}

#~ # Print file with the minimum value of data range.
#~ my $minFile = "min.txt";
#~ open (MIN, ">$minFile") or die "Can't open $minFile for writing: $!";
#~ print MIN "$min";
#~ close MIN;
#~ # Print file with the maximum value of data range.
#~ my $maxFile = "max.txt";
#~ open (MAX, ">$maxFile") or die "Can't open $maxFile for writing: $!";
#~ print MAX "$max";
#~ close MAX;

# This product includes color specifications and designs
# developed by Cynthia Brewer (http://colorbrewer.org/).
# http://soliton.vm.bytemark.co.uk/pub/cpt-city/cb/seq/YlGn_07.cpt
# "255:255:204-255:255:204-217:240:163-217:240:163-173:221:142-173:221:142-120:198:121-120:198:121-65:171:93-65:171:93-35:132:67-35:132:67-0:90:50-0:90:50"


# Viridis modified from http://soliton.vm.bytemark.co.uk/pub/cpt-city/mpl/viridis.cpt
# "68:1:84-68:2:86-69:4:87-69:5:89-70:7:90-70:8:92-70:10:93-70:11:94-71:13:96-71:14:97-71:16:99-71:17:100-71:19:101-72:20:103-72:22:104-72:23:105-72:24:106-72:26:108-72:27:109-72:28:110-72:29:111-72:31:112-72:32:113-72:33:115-72:35:116-72:36:117-72:37:118-72:38:119-72:40:120-72:41:121-71:42:122-71:44:122-71:45:123-71:46:124-71:47:125-70:48:126-70:50:126-70:51:127-70:52:128-69:53:129-69:55:129-69:56:130-68:57:131-68:58:131-68:59:132-67:61:132-67:62:133-66:63:133-66:64:134-66:65:134-65:66:135-65:68:135-64:69:136-64:70:136-63:71:136-63:72:137-62:73:137-62:74:137-62:76:138-61:77:138-61:78:138-60:79:138-60:80:139-59:81:139-59:82:139-58:83:139-58:84:140-57:85:140-57:86:140-56:88:140-56:89:140-55:90:140-55:91:141-54:92:141-54:93:141-53:94:141-53:95:141-52:96:141-52:97:141-51:98:141-51:99:141-50:100:142-50:101:142-49:102:142-49:103:142-49:104:142-48:105:142-48:106:142-47:107:142-47:108:142-46:109:142-46:110:142-46:111:142-45:112:142-45:113:142-44:113:142-44:114:142-44:115:142-43:116:142-43:117:142-42:118:142-42:119:142-42:120:142-41:121:142-41:122:142-41:123:142-40:124:142-40:125:142-39:126:142-39:127:142-39:128:142-38:129:142-38:130:142-38:130:142-37:131:142-37:132:142-37:133:142-36:134:142-36:135:142-35:136:142-35:137:142-35:138:141-34:139:141-34:140:141-34:141:141-33:142:141-33:143:141-33:144:141-33:145:140-32:146:140-32:146:140-32:147:140-31:148:140-31:149:139-31:150:139-31:151:139-31:152:139-31:153:138-31:154:138-30:155:138-30:156:137-30:157:137-31:158:137-31:159:136-31:160:136-31:161:136-31:161:135-31:162:135-32:163:134-32:164:134-33:165:133-33:166:133-34:167:133-34:168:132-35:169:131-36:170:131-37:171:130-37:172:130-38:173:129-39:173:129-40:174:128-41:175:127-42:176:127-44:177:126-45:178:125-46:179:124-47:180:124-49:181:123-50:182:122-52:182:121-53:183:121-55:184:120-56:185:119-58:186:118-59:187:117-61:188:116-63:188:115-64:189:114-66:190:113-68:191:112-70:192:111-72:193:110-74:193:109-76:194:108-78:195:107-80:196:106-82:197:105-84:197:104-86:198:103-88:199:101-90:200:100-92:200:99-94:201:98-96:202:96-99:203:95-101:203:94-103:204:92-105:205:91-108:205:90-110:206:88-112:207:87-115:208:86-117:208:84-119:209:83-122:209:81-124:210:80-127:211:78-129:211:77-132:212:75-134:213:73-137:213:72-139:214:70-142:214:69-144:215:67-147:215:65-149:216:64-152:216:62-155:217:60-157:217:59-160:218:57-162:218:55-165:219:54-168:219:52-170:220:50-173:220:48-176:221:47-178:221:45-181:222:43-184:222:41-186:222:40-189:223:38-192:223:37-194:223:35-197:224:33-200:224:32-202:225:31-205:225:29-208:225:28-210:226:27-213:226:26-216:226:25-218:227:25-221:227:24-223:227:24-226:228:24-229:228:25-231:228:25-234:229:26-236:229:27-239:229:28-241:229:29-244:230:30-246:230:32-248:230:33-251:231:35-253:231:37"
# my $outlierLow = "40:0:50";
# my $outlierHigh = "255:255:0";


# h5jetModified4 with white (haxby) bottom "255:255:255-208:216:251-186:197:247-143:161:241-97:122:236-0:0:255-0:63:255-0:127:255-0:191:255-63:255:255-255:255:63-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0"

# NASA luigi reversed "158:0:0-213:0:0-255:0:0-255:72:0-255:144:0-255:196:0-255:235:0-255:254:71-206:255:255-175:245:255-156:238:255-134:217:255-109:193:255-65:150:255-32:80:255-4:14:216";

# NASA Luigi "4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0";

# NASA Luigi with white bottom from haxby 255:255:255-208:216:251-186:197:247-143:161:241-97:122:236-4:14:216-32:80:255-65:150:255-109:193:255-134:217:255-156:238:255-175:245:255-206:255:255-255:254:71-255:235:0-255:196:0-255:144:0-255:72:0-255:0:0-213:0:0-158:0:0

# h5 Jet 0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-63:255:255-127:255:191-191:255:127-255:255:63-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0

# h5 Jet modified for zero centered bar "0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-63:255:255-255:255:63-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0";

# h5 Jet modified2 - smooth with minimal green in the middle 0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0

# h5 Jet modified3 - is the same as that for the zero centered bar. 0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-63:255:255-255:255:63-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0

# h5 Jet modified4 - similar to modified2 but leaving hopefully very limited green in the middle "0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-63:255:255-255:255:63-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0";

# h5 Jet modified2 with top 50% of color bar faded from red to white 0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0-238:80:78-255:90:90-255:124:124-255:158:158-245:179:174-255:196:196-255:215:215-255:225:225-255:235:235-255:245:245-255:255:255

# h5 Jet modified2 with bottom 50% of color bar faded from blue to white 255:255:255-255:255:255-255:255:255-208:216:251-208:216:251-186:197:247-186:197:247-143:161:241-143:161:241-97:122:236-97:122:236-97:122:236-97:122:236-0:0:191-0:0:255-0:63:255-0:127:255-0:191:255-0:255:255-255:255:0-255:191:0-255:127:0-255:63:0-255:0:0-191:0:0

# Prcp 17 November 2010 105:0:0-158:0:0-213:0:0-255:0:0-255:72:0-255:144:0-255:196:0-255:235:0-255:254:71-206:255:255-175:245:255-156:238:255-134:217:255-109:193:255-65:150:255-32:80:255-4:14:216-black

#~  NASA ocean color string:  144:0:111-141:0:114-138:0:117-135:0:120-132:0:123-129:0:126-126:0:129-123:0:132-120:0:135-117:0:138-114:0:141-111:0:144-108:0:147-105:0:150-102:0:153-99:0:156-96:0:159-93:0:162-90:0:165-87:0:168-84:0:171-81:0:174-78:0:177-75:0:180-72:0:183-69:0:186-66:0:189-63:0:192-60:0:195-57:0:198-54:0:201-51:0:204-48:0:207-45:0:210-42:0:213-39:0:216-36:0:219-33:0:222-30:0:225-27:0:228-24:0:231-21:0:234-18:0:237-15:0:240-12:0:243-9:0:246-6:0:249-0:0:252-0:0:255-0:5:255-0:10:255-0:16:255-0:21:255-0:26:255-0:32:255-0:37:255-0:42:255-0:48:255-0:53:255-0:58:255-0:64:255-0:69:255-0:74:255-0:80:255-0:85:255-0:90:255-0:96:255-0:101:255-0:106:255-0:112:255-0:117:255-0:122:255-0:128:255-0:133:255-0:138:255-0:144:255-0:149:255-0:154:255-0:160:255-0:165:255-0:170:255-0:176:255-0:181:255-0:186:255-0:192:255-0:197:255-0:202:255-0:208:255-0:213:255-0:218:255-0:224:255-0:229:255-0:234:255-0:240:255-0:245:255-0:250:255-0:255:255-0:255:247-0:255:239-0:255:231-0:255:223-0:255:215-0:255:207-0:255:199-0:255:191-0:255:183-0:255:175-0:255:167-0:255:159-0:255:151-0:255:143-0:255:135-0:255:127-0:255:119-0:255:111-0:255:103-0:255:95-0:255:87-0:255:79-0:255:71-0:255:63-0:255:55-0:255:47-0:255:39-0:255:31-0:255:23-0:255:15-0:255:0-8:255:0-16:255:0-24:255:0-32:255:0-40:255:0-48:255:0-56:255:0-64:255:0-72:255:0-80:255:0-88:255:0-96:255:0-104:255:0-112:255:0-120:255:0-128:255:0-136:255:0-144:255:0-152:255:0-160:255:0-168:255:0-176:255:0-184:255:0-192:255:0-200:255:0-208:255:0-216:255:0-224:255:0-232:255:0-240:255:0-248:255:0-255:255:0-255:251:0-255:247:0-255:243:0-255:239:0-255:235:0-255:231:0-255:227:0-255:223:0-255:219:0-255:215:0-255:211:0-255:207:0-255:203:0-255:199:0-255:195:0-255:191:0-255:187:0-255:183:0-255:179:0-255:175:0-255:171:0-255:167:0-255:163:0-255:159:0-255:155:0-255:151:0-255:147:0-255:143:0-255:139:0-255:135:0-255:131:0-255:127:0-255:123:0-255:119:0-255:115:0-255:111:0-255:107:0-255:103:0-255:99:0-255:95:0-255:91:0-255:87:0-255:83:0-255:79:0-255:75:0-255:71:0-255:67:0-255:63:0-255:59:0-255:55:0-255:51:0-255:47:0-255:43:0-255:39:0-255:35:0-255:31:0-255:27:0-255:23:0-255:19:0-255:15:0-255:11:0-255:7:0-255:3:0-255:0:0-250:0:0-245:0:0-240:0:0-235:0:0-230:0:0-225:0:0-220:0:0-215:0:0-210:0:0-205:0:0-200:0:0-195:0:0-190:0:0-185:0:0-180:0:0-175:0:0-170:0:0-165:0:0-160:0:0-155:0:0-150:0:0-145:0:0-140:0:0-135:0:0-130:0:0-125:0:0-120:0:0-115:0:0-110:0:0-105:0:0

# dkbluered  7:0:51-17:0:79-17:0:79-25:0:107-25:0:107-28:0:135-28:0:135-25:0:163-25:0:163-22:0:191-22:0:191-15:0:219-15:0:219-2:0:247-2:0:247-20:33:255-20:33:255-56:76:255-56:76:255-89:117:255-89:117:255-122:153:255-122:153:255-155:186:255-155:186:255-191:211:255-191:211:255-224:237:255-224:237:255-255:255:255-255:255:255-255:237:224-255:237:224-255:211:191-255:211:191-255:186:155-255:186:155-255:153:122-255:153:122-255:117:89-255:117:89-255:76:56-255:76:56-255:33:20-255:33:20-247:0:2-247:0:2-219:0:15-219:0:15-191:0:22-191:0:22-163:0:25-163:0:25-135:0:28-135:0:28-107:0:25-107:0:25-79:0:17-79:0:17-53:0:7

# green-red-blue-cyan profile alarm.p1.1.0 Designed by Duncan Carr Agnew, IGPP/SIO 224:255:216-219:255:200-219:255:200-218:255:185-218:255:185-222:255:169-222:255:169-229:255:154-229:255:154-242:255:138-242:255:138-255:251:122-255:251:122-255:229:106-255:229:106-255:204:91-255:204:91-255:174:75-255:174:75-255:140:59-255:140:59-255:102:44-255:102:44-255:59:28-255:59:28-255:59:28-255:59:28-255:12:120-255:12:120-255:12:229-255:12:229-173:12:255-173:12:255-65:12:255-65:12:255-12:67:255-12:67:255-12:176:255-12:176:255-12:255:225

# green-red-blue-cyan profile alarm.p4.0.1 Designed by Duncan Carr Agnew, IGPP/SIO 244:255:242-255:12:208-186:12:255-114:12:255-62:12:255-20:12:255-12:38:255-12:68:255-12:95:255-12:118:255-12:140:255-12:159:255-12:176:255-12:192:255-12:208:255-12:223:255-12:236:255-12:249:255-12:255:249-12:255:237-12:255:225

# Panoply PAL-1, the default color map in Panoply http://www.giss.nasa.gov/tools/panoply/ "4:14:216-4:14:216-32:80:255-32:80:255-65:150:255-65:150:255-109:193:255-109:193:255-134:217:255-134:217:255-156:238:255-156:238:255-175:245:255-175:245:255-206:255:255-206:255:255-255:254:71-255:254:71-255:235:0-255:235:0-255:196:0-255:196:0-255:144:0-255:144:0-255:72:0-255:72:0-255:0:0-255:0:0-213:0:0-213:0:0-158:0:0-158:0:0"

# black & white modified form colorbrewer.org "37:37:37-82:82:82-82:82:82-189:189:189-189:189:189-217:217:217";

# Modified from http://soliton.vm.bytemark.co.uk/pub/cpt-city/gmt/tn/GMT_no_green.png.index.html
#"32:96:255-32:159:255-32:191:255-0:207:255-42:255:255-85:255:255-127:255:255-170:255:255-255:255:84-255:240:0-255:191:0-255:168:0-255:138:0-255:112:0-255:77:0-255:0:0";

# Modified from http://soliton.vm.bytemark.co.uk/pub/cpt-city/gmt/tn/GMT_no_green.png.index.html
# The white part is from # http://soliton.vm.bytemark.co.uk/pub/cpt-city/jjg/misc/tn/seminf-haxby.png.index.html
#"255:255:255-208:216:251-186:197:247-143:161:241-97:122:236-32:96:255-32:159:255-32:191:255-0:207:255-42:255:255-85:255:255-127:255:255-170:255:255-255:255:84-255:240:0-255:191:0-255:168:0-255:138:0-255:112:0-255:77:0-255:0:0";


