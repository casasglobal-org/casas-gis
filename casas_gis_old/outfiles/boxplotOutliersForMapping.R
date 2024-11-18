# Code notebook for Naples 2013.

# Author: Luigi Ponti quartese gmail.com
# Copyright: (c) 2013 CASAS (Center for the Analysis of Sustainable Agricultural Systems, https://www.casasglobal.org/)
# SPDX-License-Identifier: GPL-2.0-or-later

# Set working directory.
setwd("H:\\maxtor_mirror\\pending papers\\OliveFly_Desertification\\SPA-IntConference-Naples2013")

# Detect outliers not suitable for regression.

ERA40_water <- read.delim("Olive_era40_water020_years1990-2000_Avg.txt")
ERA40_nowat <- read.delim("Olive_era40_no-water_years1990-2000_Avg.txt")

NCDC_water <- read.delim("Olive_ncdc_water020_years1990-2000_Avg.txt")
NCDC_nowat <- read.delim("Olive_ncdc_no-water_years1990-2000_Avg.txt")


names(ERA40_water)
 [1] "Model"      "Date"       "Time"       "WxFile"     "Long"      
 [6] "Lat"        "JdStart"    "DysToOut"   "Month"      "Day"       
[11] "Year"       "dd"         "ddbZero"    "FruWgt"     "fruNum"    
[16] "Bloomday"   "BloomYr"    "DDBSum"     "ChillHD"    "PrcpYrSum" 
[21] "TempIncr"   "ddbMinus10" "ddbMinus83" "OFEgDays"   "OFLrDays"  
[26] "OFPuDays"   "OFAdDays"   "OfPupSum"   "DamFrSum"   "PrcntAtkd" 

names(ERA40_nowat)
 [1] "Model"      "Date"       "Time"       "WxFile"     "Long"      
 [6] "Lat"        "JdStart"    "DysToOut"   "Month"      "Day"       
[11] "Year"       "dd"         "ddbZero"    "FruWgt"     "fruNum"    
[16] "Bloomday"   "BloomYr"    "DDBSum"     "ChillHD"    "PrcpYrSum" 
[21] "TempIncr"   "ddbMinus10" "ddbMinus83" "OFEgDays"   "OFLrDays"  
[26] "OFPuDays"   "OFAdDays"   "OfPupSum"   "DamFrSum"   "PrcntAtkd" 


############## WORKFLOW for figures with outliers ################
#
# 1. Use boxplot.stats to get a customColorRule via 
#    getCustomColorRule.pl
#
# 2. Adapt obtained file using max and min values from summary(), 
#    rename to defaultColorRule, and move to /andy/
#
# 3. Put min,max whisker values for d.legend in MedPresentClimate
#    using -w flag and setting $LOWBARCOL and $UPBARCOL to boxplot 
#    whiskers
#
# 4. Run mapping cycle via Med Basin shell
#
##################################################################

# ncdc water020 #

for(i in c("FruWgt", "OfPupSum", "PrcpYrSum"))
{
    cat("\n")
    cat(i, "\n")
    cat("Summary:\t")
    cat(summary(NCDC_water[[i]]), "\n")
    # boxplot(NCDC_water[[i]])
    cat("Boxplot stats:\t")
    cat(boxplot.stats(NCDC_water[[i]])$stats, "\n\n")
}

FruWgt 
Summary:        0 0.0175 1598 2057 3705 6863 
Boxplot stats:  0 0.015 1597.905 3706.915 6862.65 

OfPupSum 
Summary:        0 0.127 1831 2950 5316 12270 
Boxplot stats:  0 0.125 1830.722 5319.064 12272.8 

PrcpYrSum 
Summary:        16.85 388.2 547.6 601.5 751 3935 
Boxplot stats:  16.85 387.22 547.59 751.805 1295.34 


###########

# ncdc no water #

for(i in c("FruWgt", "OfPupSum", "PrcpYrSum"))
{
    cat("\n")
    cat(i, "\n")
    cat("Summary:\t")
    cat(summary(NCDC_nowat[[i]]), "\n")
    # boxplot(NCDC_nowat[[i]])
    cat("Boxplot stats:\t")
    cat(boxplot.stats(NCDC_nowat[[i]])$stats, "\n\n")
}

FruWgt 
Summary:        0 772.4 5727 4766 7358 10380 
Boxplot stats:  0 748.15 5727.25 7366.405 10384.74 

OfPupSum 
Summary:        0 273.4 4501 4702 7989 20900 
Boxplot stats:  0 263.4065 4500.968 7991.394 18592.88 

PrcpYrSum 
Summary:        16.85 388.2 547.6 601.5 751 3935 
Boxplot stats:  16.85 387.22 547.59 751.805 1295.34 




###########

# era40 water020 #

for(i in c("FruWgt", "OfPupSum", "PrcpYrSum"))
{
    cat("\n")
    cat(i, "\n")
    cat("Summary:\t")
    cat(summary(ERA40_water[[i]]), "\n")
    # boxplot(ERA40_water[[i]])
    cat("Boxplot stats:\t")
    cat(boxplot.stats(ERA40_water[[i]])$stats, "\n\n")
}

FruWgt 
Summary:        0 0 0 975.7 1737 9142 
Boxplot stats:  0 0 0 1737.35 4342.29 

OfPupSum 
Summary:        0 0 0.048 841.2 1015 15240 
Boxplot stats:  0 0 0.048 1015.441 2537.379 

PrcpYrSum 
Summary:        25.6 511.6 1902 2096 3159 15270 
Boxplot stats:  25.6 511.28 1901.98 3158.82 7110.47 



OfPupSum_noOutliers <- ERA40_water$OfPupSum[ERA40_water$OfPupSum<=4394.253]
quantBrks(OfPupSum_noOutliers)

# Added use n=20 classes and set firt element to zero if it gets a slightly different value.
OfPupSum_noOutliers_brks <- c("0.00", "0.0260", "0.3150", "2.9132", "11.2520", "26.0970", "57.1096", "105.2551", "182.9168", "323.0763", "526.4510", "779.7342", "1004.2614", "1278.8831", "1552.5308", "1967.7235", "2454.6158", "2944.9340", "3363.4318", "3816.4473", "4394.2530", "4394.2530","17320")

h5JetHaxbyOutliers <- c("255:255:255","208:216:251","186:197:247","143:161:241","97:122:236","0:0:191","0:0:255","0:63:255","0:127:255","0:191:255","0:255:255","63:255:255","127:255:191","191:255:127","255:255:63","255:255:0","255:191:0","255:127:0","255:63:0","255:0:0","191:0:0","139:0:0","139:0:0")

cmnt <- "h5jet (NOT modified) with white (haxby) bottom and ouliers for ERA40_water$OfPupSum"
adaptedColorRule(OfPupSum_noOutliers_brks, h5JetHaxbyOutliers, cmnt)

filename <- "defaultColorRule_olive_OfPupSum_era40_water020_years1990-2000.txt"
sink(filename)
adaptedColorRule(OfPupSum_noOutliers_brks, h5JetHaxbyOutliers, cmnt)
sink()



FruWgt_noOutliers <- ERA40_water$FruWgt[ERA40_water$FruWgt<=9182.73]
quantBrks(FruWgt_noOutliers)

# Added use n=20 classes and set firt element to zero if it gets a slightly different value.
FruWgt_noOutliers_brks <- c("0.00", "0.48", "5.98", "52.53", "170.69", "343.68", "620.92", "942.25", "1420.73", "1982.31", "2510.61", "3014.68", "3460.18", "3935.02", "4347.23", "4787.47", "5291.75", "6041.69", "6600.15", "6997.84", "9182.73", "9182.73","9471")

h5JetHaxbyOutliers <- c("255:255:255","208:216:251","186:197:247","143:161:241","97:122:236","0:0:191","0:0:255","0:63:255","0:127:255","0:191:255","0:255:255","63:255:255","127:255:191","191:255:127","255:255:63","255:255:0","255:191:0","255:127:0","255:63:0","255:0:0","191:0:0","139:0:0","139:0:0")

cmnt <- "h5jet (NOT modified) with white (haxby) bottom and ouliers for ERA40_water$OfPupSum"
adaptedColorRule(FruWgt_noOutliers_brks, h5JetHaxbyOutliers, cmnt)

filename <- "defaultColorRule_olive_FruWgt_era40_water020_years1990-2000.txt"
sink(filename)
adaptedColorRule(FruWgt_noOutliers_brks, h5JetHaxbyOutliers, cmnt)
sink()


##############

# era40 no water #

for(i in c("FruWgt", "OfPupSum", "PrcpYrSum"))
{
    cat("\n")
    cat(i, "\n")
    cat("Summary:\t")
    cat(summary(ERA40_nowat[[i]]), "\n")
    # boxplot(ERA40_water[[i]])
    cat("Boxplot stats:\t")
    cat(boxplot.stats(ERA40_nowat[[i]])$stats, "\n\n")
}

FruWgt 
Summary:        0 2101 6736 5413 7921 11210 
Boxplot stats:  0 2100.24 6736.06 7921.58 11208.87 

OfPupSum 
Summary:        0 99.43 974.5 1764 2752 17950 
Boxplot stats:  0 99.386 974.4565 2752.554 6729.705 

PrcpYrSum 
Summary:        25.6 511.6 1902 2096 3159 15270 
Boxplot stats:  25.6 511.28 1901.98 3158.82 7110.47 

OfPupSum_noOutliers <- ERA40_nowat$OfPupSum[ERA40_nowat$OfPupSum<=6729.705]
quantBrks(OfPupSum_noOutliers)

# Added a zero value as first element -- they are breaks
OfPupSum_noOutliers_brks <- c("0","0.0010000", "0.7018947", "44.0196842", "86.4089474", "121.6968947", "169.9695263", "256.4865263", "510.4118947", "785.4937895", "1021.9079474", "1285.7892105", "1519.3088947", "1785.8554211", "2121.6944211", "2622.4101053", "3159.5985789", "3715.2554737", "4267.5177895", "5039.8649474", "6729.7050000","6729.7050000","17950")

h5JetHaxbyOutliers <- c("255:255:255","208:216:251","186:197:247","143:161:241","97:122:236","0:0:191","0:0:255","0:63:255","0:127:255","0:191:255","0:255:255","63:255:255","127:255:191","191:255:127","255:255:63","255:255:0","255:191:0","255:127:0","255:63:0","255:0:0","191:0:0","139:0:0","139:0:0")

cmnt <- "h5jet (NOT modified) with white (haxby) bottom and ouliers for ERA40_nowat$OfPupSum"
adaptedColorRule(OfPupSum_noOutliers_brks, h5JetHaxbyOutliers, cmnt)

filename <- "defaultColorRule_olive_OfPupSum_era40_no-water_years1990-2000.txt"
sink(filename)
adaptedColorRule(OfPupSum_noOutliers_brks, h5JetHaxbyOutliers, cmnt)
sink()


##############

## IDEA: Get quantile breaks for [min : whisker], then get adapted
## color rule up to whisker. Add in adaptedColorRule the last color
## for outliers 139:0:0 matched to maximum, e.g.

#~ 430.768 191:0:0
#~ 430.768 139:0:0
#~ 3000.000 139:0:0




# Function to get quartile breaks (11 bins for h5 Jet modified4)
quantBrks <- function(dataFrame)
{
    # Intervals
    library(classInt)
    q20 <- classIntervals(dataFrame[dataFrame>0], n = 20, style = "quantile")    
    # Plot ECDF.
    windows()
    plot(q20, pal = c("white", "black"), main = names(dataFrame))
    # Breaks for legend
    #cat("Quartile breaks for", names(dataFrame))
    cat("\"" )
    # Use one of the following formats as appropriate
    # cat(formatC(q11$brks, format="f", digits=3), sep = "\", \"") # use this as appropriate
    cat(format(q20$brks, scientific=FALSE, trim=TRUE), sep = "\", \"")
    cat("\"\n")
}


# Plot and print breaks.
quantBrks(grapeHareaPos_noOutliers)


# Function to get adapted color rule (check n of iterations -- the first is zero)
adaptedColorRule <- function(brks, clrs, cmnt)
{
    cat("#", cmnt)
    cat("\n")
    for (i in 1:23)
    {
        cat(brks[i], clrs[i])
        cat("\n")
    }
    cat ("end\n")
}






