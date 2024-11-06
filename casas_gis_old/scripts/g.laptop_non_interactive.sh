#!/bin/sh

#############################################################################
#
# MODULE:       g.laptop_non_interactive.sh
#
# AUTHOR(S):    Otto Dassau <dassau@gbd-consult.de>
#               Cleaned-up and edited by Luigi Ponti lponti inbox com
#               to run in non interactive mode via the g.parser interface.
#
# PURPOSE:      Script to extract raster and vector data from current
#               location into a new one. Data can be copied or extracted
#		        in current or original resolution and region extent.
#
# COPYRIGHT:    (C) 2002-2012 by the GRASS Development Team
#
#               This program is free software under the GNU General Public
#               License (>=v2). Read the file COPYING that comes with GRASS
#               for details.
#
# COMMENTS:     Sometimes extracting vector maps at current region extent
#               with v.extract doesn't work properly - use copy instead!!
#
#############################################################################

# %module
# %  description: Makes a copy of the current location
# %end

# %option
# % guisection: Main
# % key: newLocation
# % type: string
# % description: New (target) location name
# % required: yes
# %end

# %option
# % key: rasterList
# % type: string
# % answer: all
# % description: List of raster maps to copy (separated by space)
# %end

# %option
# % key: vectorList
# % type: string
# % description: List of vector maps to copy (separated by space)
# %end

# %flag
# % key: r
# % answer: 1
# % description: Export raster maps at original instead of current resolution
# %end

# %flag
# % key: v
# % description: Clip vector maps to current region extent
# %end

# %flag
# % key: t
# % description: Put new location in a compressed *.tar.gz archive
# %end

# %flag
# % key: d
# % description: Delete uncompressed location after *.tar.gz archive creation
# %end

if [ -z "$GISBASE" ] ; then
    echo "You must be in GRASS GIS to run this program." 1>&2
    exit 1
fi

if [ "$1" != "@ARGS_PARSED@" ] ; then
    exec g.parser "$0" "$@"
fi

# Get path for current location

eval `g.gisenv`
: ${GISBASE?} ${GISDBASE?} ${LOCATION_NAME?} ${MAPSET?}
LOCATION=$GISDBASE/$LOCATION_NAME/$MAPSET

### cleanup in case of ERROR
cleanup()
	{
 	if test $LOCNAME
	then
	echo "delete already build location $LOCNAME?"
	 \rm -ir $GISDBASE/$LOCNAME/
	 \rm -rf $CURRWD/tmp/$LOCNAME/
	 g.remove vect=mxy999
	fi
	}

### restore .grassrc6 in case of ERROR
restore()
	{
	 if test -f $CURRWD/tmp/$LOCNAME/$LOCNAME.grassrc6 ; then
	   mv $CURRWD/tmp/$LOCNAME/$LOCNAME.grassrc6 $HOME/.grassrc6
	 fi
	}

### what to do in case of user break:
exitprocedure()
	{
	echo ""
 	echo "User break!"
 	cleanup
	restore
	echo "cleanup temporary files and restore .grassrc6"
 	exit 1
	}

### shell check for user break (signal list: trap -l)
trap "exitprocedure" 2 3 9 15

# Set script parameters
if [ -n "$GIS_OPT_NEWLOCATION" ] ; then
	LOCNAME="$GIS_OPT_NEWLOCATION"
fi

if [ -n "$GIS_OPT_RASTERLIST" ] ; then
	LISTR="$GIS_OPT_RASTERLIST"
fi

if [ -n "$GIS_OPT_VECTORLIST" ] ; then
	LISTV="$GIS_OPT_VECTORLIST"
fi

# Create new location or exit if it exists already
if test -d "$GISDBASE/$LOCNAME" ; then
	echo ""
	echo "Location $LOCNAME exists already"
	echo ""
	echo "choose another name"
	exit 1
else
	mkdir -p $GISDBASE/$LOCNAME/PERMANENT/
fi

### manage linked grassdata files
CGISDBASE=$GISDBASE
CURRWD=$HOME
VECTLOC=$GISDBASE/$LOCNAME/PERMANENT
cd $GISDBASE/$LOCATION_NAME/PERMANENT
cp -f PROJ_INFO PROJ_UNITS DEFAULT_WIND $VECTLOC

cd $LOCATION
cp -f WIND $VECTLOC


#cp WIND $VECTLOC/DEFAULT_WIND
cd $CURRWD

### Copy rasters

mkdir -p $CURRWD/tmp/$LOCNAME/rast/
mkdir $VECTLOC/colr

### save current region and resolution for later restore
CEWRES=`g.region -p | awk '/ewres:/ {printf "%i\n",$2}'`
CNSRES=`g.region -p | awk '/nsres:/ {printf "%i\n",$2}'`

#CEWRES=`g.region -p | awk '/ewres:/ {printf "%.2f\n",$2}'`
#CNSRES=`g.region -p | awk '/nsres:/ {printf "%.2f\n",$2}'`

if [ "$LISTR" = "all" ] ; then
    for i in `ls $VECTLOC/cell/`
    do
        echo "COPY $i DATA TO $LOCNAME"
        ### Find mapset data and copy to new location
        g.findfile el=colr file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.col
        RASTCOL=`cat $CURRWD/tmp/$LOCNAME/rast/$i.col | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTCOL" = "" ] ; then
            echo "map $i has no colortable file"
        else
            if [ -d $VECTLOC/colr ] ; then
                cp $RASTCOL $VECTLOC/colr/
                echo "copy colr/$i"
            fi
        fi

        g.findfile el=cell file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.cell
        RASTCELL=`cat $CURRWD/tmp/$LOCNAME/rast/$i.cell | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTCELL" = "" ] ; then
            echo "cell/$i doesn't exist"
        else
            if [ -d $VECTLOC/cell ] ; then
                cp $RASTCELL $VECTLOC/cell/
                echo "copy cell/$i"
            else
                mkdir $VECTLOC/cell
                cp $RASTCELL $VECTLOC/cell
                echo "copy cell/$i"
            fi
        fi

        g.findfile el=cellhd file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.cellhd
        RASTCHD=`cat $CURRWD/tmp/$LOCNAME/rast/$i.cellhd | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTCHD" = "" ] ; then
            echo "cellhd/$i doesn't exist"
        else
            if [ -d $VECTLOC/cellhd ] ; then
                cp $RASTCHD $VECTLOC/cellhd/
                echo "copy cellhd/$i"
            else
                mkdir $VECTLOC/cellhd
                cp $RASTCHD $VECTLOC/cellhd/
				echo "copy cellhd/$i"
            fi
        fi

        g.findfile el=cell_misc file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.cell_misc
        RASTCMISC=`cat $CURRWD/tmp/$LOCNAME/rast/$i.cell_misc | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTCMISC" = "" ] ; then
            echo "/cell_misc/$i doesn't exist"
         else
            if [ -d "$VECTLOC/cell_misc/$i" ] ; then
                cp -r $RASTCMISC/* $VECTLOC/cell_misc/$i
                echo "copy cell_misc/$i"
            else
                mkdir -p $VECTLOC/cell_misc/$i
                cp -r $RASTCMISC/* $VECTLOC/cell_misc/$i
                echo "copy cell_misc/$i"
            fi
        fi

        g.findfile el=fcell file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.fcell
        RASTFCELL=`cat $CURRWD/tmp/$LOCNAME/rast/$i.fcell | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTFCELL" = "" ] ; then
            echo "fcell/$i doesn't exist"
            else
                if [ -d $VECTLOC/fcell ] ; then
				    cp $RASTFCELL $VECTLOC/fcell/
					echo "copy fcell/$i"
                else
                    mkdir $VECTLOC/fcell
                    cp $RASTFCELL $VECTLOC/fcell/
					echo "copy fcell/$i"
                fi
            fi

        g.findfile el=dcell file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.dcell
        RASTDCELL=`cat $CURRWD/tmp/$LOCNAME/rast/$i.dcell | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTDCELL" = "" ] ; then
				echo "dcell/$i doesn't exist"
        else
            if [ -d $VECTLOC/dcell ] ; then
                cp $RASTDCELL $VECTLOC/dcell
                echo "copy dcell/$i"
            else
                mkdir $VECTLOC/dcell
                cp $RASTDCELL $VECTLOC/dcell/
                echo "copy dcell/$i"
            fi
        fi

        g.findfile el=g3dcell file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.g3dcell
        RASTGD=`cat $CURRWD/tmp/$LOCNAME/rast/$i.g3dcell | grep "file" | cut -b 7- | sed -e "s/'//g"`
        if [ "$RASTGD" = "" ] ; then
            echo "g3dcell/$i doesn't exist"
            echo ""
        else
            if [ -d $VECTLOC/g3dcell ] ; then
                cp $RASTGD $VECTLOC/g3dcell/
                echo "copy g3dcell/$i"
                echo ""
            else
                mkdir $VECTLOC/g3dcell
                cp $RASTGD $VECTLOC/g3dcell/
                echo "copy g3dcell/$i"
                echo ""
            fi
        fi
    done
else
    for i in $LISTR
    do
        ### Find mapset data and copy to new location
        g.findfile el=colr file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.col
        RASTCOL=`cat $CURRWD/tmp/$LOCNAME/rast/$i.col | grep "file" | cut -b 7- | sed -e "s/$i'//g"`
        if [ -f $RASTCOL$i ] ; then
            cp $RASTCOL$i $CURRWD/tmp/$LOCNAME/rast/$i.colr
        else
            echo "map $i has no colortable file"
        fi
        if [ "$GIS_FLAG_R" -eq 1 ] ; then
            ### Find original data resolution for export
            g.findfile el=cellhd file=$i > $CURRWD/tmp/$LOCNAME/rast/$i.hd
            RASTHD=`cat $CURRWD/tmp/$LOCNAME/rast/$i.hd | grep "file" | cut -b 7- | sed -e "s/'//g"`
            OEWRES=`cat $RASTHD | awk '/e-w resol:/ {printf "%i\n",$3}'`
            ONSRES=`cat $RASTHD | awk '/n-s resol:/ {printf "%i\n",$3}'`
#			OEWRES=`cat $RASTHD | awk '/e-w resol:/ {printf "%.2f\n",$3}'`
#			ONSRES=`cat $RASTHD | awk '/n-s resol:/ {printf "%.2f\n",$3}'`
            g.region ewres=$OEWRES nsres=$ONSRES -a
            ### Export map
            echo "export raster map $i for later import"
            r.out.ascii in=$i out=$CURRWD/tmp/$LOCNAME/rast/$i.asc
            echo ""
        else
            ### Export map
            echo "export raster map $i for later import"
            r.out.ascii in=$i out=$CURRWD/tmp/$LOCNAME/rast/$i.asc
            echo ""
        fi
    done
fi

### Copy vectors

mkdir -p $CURRWD/tmp/$LOCNAME/vector

# Get current region extent as area map
if [ "$GIS_FLAG_V" -eq 1 ] ; then
    v.in.region output=mxy999 type=area
fi

### extract vector data into new location

if [ "$LISTV" = "all" ] ; then
    $LISTV = `ls $VECTLOC/vector/`
fi

for i in $LISTV
do
    if [ "$GIS_FLAG_V" -eq 1 ] ; then
        echo "extract vector map $i from current region extent"
        g.findfile el=vector file=$i > $CURRWD/tmp/$LOCNAME/vector/$i
        VECTMAP=`cat $CURRWD/tmp/$LOCNAME/vector/$i | grep "file" | cut -b 7- | sed -e "s/$i'//g"`
        if [ -d $VECTLOC/vector/ ] ; then
            v.select ainput=$i binput=mxy999 output=mxyarea999
            cp -r $VECTMAP../vector/mxyarea999 $VECTLOC/vector/$i
        else
            mkdir -p $VECTLOC/vector/
            v.select ainput=$i binput=mxy999 output=mxyarea999
            cp -r $VECTMAP../vector/mxyarea999 $VECTLOC/vector/$i
        fi
        if [ -f $VECTMAP../dbf/$i ] ; then
            if [ -d $VECTLOC/dbf/ ] ; then
                cp $VECTMAP../dbf/mxyarea999.dbf $VECTLOC/dbf/$i.dbf
            else
                mkdir -p $VECTLOC/dbf
                cp $VECTMAP../dbf/mxyarea999.dbf $VECTLOC/dbf/$i.dbf
            fi
        fi
        g.remove -f vect=mxyarea999
        g.remove -f vect=mxy999
    else
        ### copy vector data into new location
        echo "copy vector map $i"
        g.findfile el=vector file=$i > $CURRWD/tmp/$LOCNAME/vector/$i
        VECTMAP=`cat $CURRWD/tmp/$LOCNAME/vector/$i | grep "file" | cut -b 7- | sed -e "s/$i'//g"`
        if [ -d $VECTLOC/vector/ ] ; then
            cp -r $VECTMAP../vector/$i $VECTLOC/vector/
        else
            mkdir -p $VECTLOC/vector/
            cp -r $VECTMAP../vector/$i $VECTLOC/vector
        fi
        if [ -f $VECTMAP../dbf/$i.dbf ] ; then
            if [ -d $VECTLOC/dbf/ ] ; then
                cp $VECTMAP../dbf/$i.dbf $VECTLOC/dbf/
            else
                mkdir -p $VECTLOC/dbf/
                cp $VECTMAP../dbf/$i.dbf $VECTLOC/dbf/
            fi
        fi
    fi
done

### In case no files were chosen for export at all
if [ "$LISTR" = "" -a "$LISTV" = "" ] ; then
	echo "No files chosen - sorry!"
	echo "...removing already created location $LOCNAME"
	rm -ir $GISDBASE/$LOCNAME
    cleanup
	exit 1
fi

### If no raster import is needed
if [ "$LISTR" = "" -o "$LISTR" = "all" ] ; then
    if [ "$GIS_FLAG_T" -eq 1 ] ; then
        cd $GISDBASE
        tar czvf ~/$LOCNAME.tar.gz $LOCNAME/*
        if [ "$GIS_FLAG_D" -eq 1 ] ; then
            rm -ir $GISDBASE/$LOCNAME/
        else
            echo ""
            echo "Location $LOCNAME kept in $GISDBASE"
        fi
	else
		echo ""
		echo "Location $LOCNAME created in $GISDBASE"
		echo ""
		echo "bye..."
    fi
else
    ### Else raster import into new location is needed
    ### save .grassrc6
	if test -e $HOME/.grassrc6 ; then
   		mv $HOME/.grassrc6 $CURRWD/tmp/$LOCNAME/$LOCNAME.grassrc6
	fi

    ### change to new location for import of raster data
    LOCATION_NAME=$LOCNAME
    GISDBASE=$CGISDBASE
    MAPSET=PERMANENT
    LOCATION=$GISDBASE/$LOCATION_NAME/$MAPSET

     echo "LOCATION_NAME: $LOCNAME"  > $HOME/.grassrc6
     echo "MAPSET: PERMANENT"   	>> $HOME/.grassrc6
     echo "DIGITIZER: none"    	>> $HOME/.grassrc6
     echo "GISDBASE: $GISDBASE"	>> $HOME/.grassrc6

     export LOCATION_NAME=$LOCNAME
     export GISBASE=$GISBASE
     export GISRC=$HOME/.grassrc6
     export PATH=$PATH:$GISBASE/bin:$GISBASE/scripts

    ### import raster files
     echo ""
     echo "import raster maps to location $LOCNAME"
     echo ""
     echo "!! changed into new location $LOCNAME for import !!"
     cd $CURRWD/tmp/$LOCNAME/rast

    LISTRA=`ls *.asc`
    for i in $LISTRA
        do
        NEWNAME=`basename $i .asc`
        r.in.ascii in=$i out=$NEWNAME
#		r.support -r $NEWNAME
    done

	LISTC=`ls *.colr`
    mkdir -p $GISDBASE/$LOCNAME/PERMANENT/colr
    for i in $LISTC
        do
        NEWNAME2=`basename $i .colr`
        cp $CURRWD/tmp/$LOCNAME/rast/$i $GISDBASE/$LOCNAME/PERMANENT/colr/$NEWNAME2
    done

    ### restore .grassrc6 and cleanup
    restore
    echo ""
    echo "!! changed back into current location !!"

    #cleanup
    g.region nsres=$CNSRES ewres=$CEWRES -a

    ### Tar the new location if requested
    if [ "$GIS_FLAG_T" -eq 1 ] ; then
		cd $GISDBASE
		tar czvf ~/$LOCNAME.tar.gz $LOCNAME/*
		echo ""
		echo "$LOCNAME.tar.gz written to $HOME"
		echo ""
        if [ "$GIS_FLAG_D" -eq 1 ] ; then
            rm -rf $GISDBASE/$LOCNAME/
        else
            echo ""
            echo "Location $LOCNAME kept in $GISDBASE"
        fi
	else
		echo ""
		echo "Location $LOCNAME created in $GISDBASE"
		echo ""
		echo "bye..."
    fi
fi

#restore .grassrc6 and cleanup
restore
rm -rf $CURRWD/tmp
g.region nsres=$CNSRES ewres=$CEWRES -a

