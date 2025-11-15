#!/usr/bin/env Rscript
# Script to compute GIS file with average, standard deviation,
# and coefficient of variation. Let us have statistical software
# compute the statistics.

# Author: Luigi Ponti quartese at gmail.com
# SPDX-License-Identifier: GPL-2.0-or-later
# Date: 7 April 2010

# Updated 13 November 2010: fixedPart <- aggregate
# replace by a simple array selection by rows and cols.

# Updated 22 June 2012: outputs an *_ALL.txt file with
# with contents of yearly files merged for computations
# and or spreadsheet manipulation. Different from the
# *Summaries.txt file that models may already produce
# because the first year of simulation is not included
# in the *_ALL.txt file.

# Updated 17 July  2013: It now also autputs a file called 
# SummaryStats.txt that includes summary stats for all
# variables as well as black and white color rules to map
# yearly data using the same color bar.


# Set working directory.
require(tcltk)
require(plyr)
current.dir <- tkchooseDirectory()
setwd(tclvalue(current.dir))
getwd()
cat("Importing files...\n")

fileNames <- readLines("GisFilesList.txt")

# No-loop alternative from http://www.mail-archive.com/r-help@r-project.org/msg63148.html
# mylist <- lapply(fileNames, read.delim)
mylist <- llply(fileNames, read.delim, .progress = progress_text(style = 3))
allData <- do.call('rbind', mylist)

############################# Get fixed part #################################

# Get fixed part of the table that is the same for all stats
# except Year column that becomes either Mean, SD, or CV.
cat("Aggregating fixed part of files... ...please, wait...\n")

#~ fixedPart <- aggregate(allData[, 1:11], 
				#~ by = list(WxFile <- allData$WxFile), 
				#~ FUN = function(x) paste(x[1]))

selectCols <- (dim(allData)[1]/length(mylist))
fixedPart <- allData[1:selectCols, 1:11]

# Make year column suitable for GIS legend
mean.data <- fixedPart
mean.data$Year <- "Avg"
sd.data <- fixedPart
sd.data$Year <- "Std"
cv.data <- fixedPart
cv.data$Year <- "CV"

##############################################################################

# Function for coefficient of variation.
# http://sci.tech-archive.net/Archive/sci.stat.math/2006-09/msg00312.html
coeff.var <- function(x, na.rm = TRUE) {
	((sd(x, na.rm = na.rm) / mean(x, na.rm = na.rm)) * 100)
}

########################### Compute Avg, SD, CV ##############################

cat("Computing statistics on variables...\n")
# With this you get varnames after fixedPart
varNames <- names(allData[, -1:-11])
# Set up progress bar.
iterations <- length(varNames)
pb <- txtProgressBar(min = 0, max = iterations, style = 3)
currentIteration <- 1
# Then you can do a for loop along varNames
for ( i in seq(along = varNames) ) {
	setTxtProgressBar(pb, currentIteration)
	##### Bloomday #####
	if ( varNames[i] == "Bloomday" ) {
		# Compute average bloom date.
		# Put missing values in place of zeros where olive did not bloom.
		is.na(allData[[varNames[i]]]) <- allData[[varNames[i]]] == 0	
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = mean, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		# Replace NaN with zeros.
		# See https://stat.ethz.ch/pipermail/r-help/2008-August/171180.html
		y[is.na(y)] <- 0.0
		mean.data <- merge(mean.data, y, by = "WxFile")		
		remove(y)		
		# Compute SD of bloom date.
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = sd, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		# Replace NaN with zeros.
		y[is.na(y)] <- 0.0
		sd.data <- merge(sd.data, y, by = "WxFile")
		remove(y)		
		# Compute CV of bloom date.
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = coeff.var, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		# Replace NaN with zeros.
		y[is.na(y)] <- 0.0
		cv.data <- merge(cv.data, y, by = "WxFile")
		remove(y)		
	##### BloomYr #####		
	} else if ( varNames[i] == "BloomYr" ) { # Sum up bloom years.
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = sum, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		mean.data <- merge(mean.data, y, by = "WxFile")
		sd.data <- merge(sd.data, y, by = "WxFile") # No change in SD
		cv.data <- merge(cv.data, y, by = "WxFile") # No change in CV
		remove(y)		
	##### Regular variables #####		
	} else { # Carry out plain loop on remaining vars.
		# Compute average.
		#~ is.na(allData[[varNames[i]]]) <- allData[[varNames[i]]] < 1	
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = mean, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		mean.data <- merge(mean.data, y, by = "WxFile") 
		remove(y)
		
		# Compute SD.
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = sd, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		# Replace NaN with zeros.
		y[is.na(y)] <- 0.0
		sd.data <- merge(sd.data, y, by = "WxFile") 
		remove(y)
		
		# Compute CV.
		y <- aggregate(allData[[varNames[i]]],
						by = list(WxFile = allData$WxFile), 
						FUN = coeff.var, na.rm = TRUE)
		names(y)[2] <- paste(varNames[i])
		# Replace NaN with zeros.
		y[is.na(y)] <- 0.0
		cv.data <- merge(cv.data, y, by = "WxFile")
		remove(y)		
	}	
	currentIteration <- currentIteration + 1
} 

##############################################################################

# Remove extra column "Group.1" and get original column order.
mean.data <- subset(mean.data, select = names(allData))
sd.data <- subset(sd.data, select = names(allData))
cv.data <- subset(cv.data, select = names(allData))

# Write output files.
baseFileName <- substr(fileNames[1], 1, 14)
write.table(mean.data, file = paste(baseFileName, "Avg.txt", sep = ""), 
			quote=FALSE,  sep="\t", 
			row.names = FALSE, col.names = TRUE)
write.table(sd.data, file = paste(baseFileName, "Std.txt", sep = ""), 
			quote=FALSE,  sep="\t", 
			row.names = FALSE, col.names = TRUE)
write.table(cv.data, file = paste(baseFileName, "CV.txt", sep = ""), 
			quote=FALSE,  sep="\t", 
			row.names = FALSE, col.names = TRUE)
write.table(allData, file = paste(baseFileName, "ALL.txt", sep = ""), 
			quote=FALSE,  sep="\t", 
			row.names = FALSE, col.names = TRUE)

# Print summary statistics.
sink(file = paste(baseFileName, "SummaryStats.txt", sep = ""))

cat ("#########################################\n")
cat ("# Summary statistics for all variables. #\n")
cat ("#########################################\n")
cat ("\n")


lapply(allData[, -1:-11], function(x) cbind(summary(x, digits=getOption("digits"))))

cat ("\n")
cat ("#############################################\n")
cat ("# Black and white color rules for mapping   #\n")
cat ("# multiple years using the same color rule. #\n")
cat ("#############################################\n")
cat ("\n")

#  Vectors including colors and where to place them in relative terms.
breaksBW = c(0.00, 0.25, 0.25, 0.50, 0.50, 0.75, 0.75, 1.00)
colorSquenceBW = c("255:255:255", "204:204:204", "150:150:150",
    "150:150:150", "99:99:99", "99:99:99", "37:37:37", "37:37:37")

# Function to print the color rule.
greyColorRule <- function(relativeBreaks, colorSquence, listWithVar)
{
    varMin = min(listWithVar)
    varMax = max(listWithVar)
    varRange = varMax - varMin
    absoluteBreaks = (relativeBreaks * varRange) + varMin
    
    cat("#", names(listWithVar))
    cat("\n")
    for (i in 1:8)
    {
        cat(absoluteBreaks[i], colorSquence[i])
        cat("\n")
    }
    cat ("end\n")
}

# Loop  over all variables.
for ( i in seq(along = varNames) )
{
    greyColorRule(breaksBW, colorSquenceBW, allData[varNames[i]])
    cat("\n")    
}
# Close output file and progress bar.
sink()
close(pb)
