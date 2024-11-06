Script to generate the images on this page:
by H.Bowman (GRASS wiki license)

#!/bin/sh

# customize this:
ADDON_DIR="/path/to/grass/svn/grass-addons/raster/r.colors.tools/palettes"

g.region n=100 s=0 w=0 e=450 res=1

d.mon x0
d.resize h=100 w=450

COLOR_DIR="$GISBASE/etc/colors/"
cd "$COLOR_DIR"
RELATIVE=`grep '%' * | cut -f1 -d: | grep -v "matches" | uniq`
ABSOLUTE=`grep -v '%' * | cut -f1 -d: | grep -v "matches" | uniq`
MIXED=`grep '%' $ABSOLUTE | cut -f1 -d: | grep -v "matches" | uniq`

GRASS_OVERWRITE=1
export GRASS_OVERWRITE

OUTPUT_DIR=/tmp/grass/colortables/
rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
cd $OUTPUT_DIR


draw_and_output()
{
  d.erase
  d.font Vera

  d.legend grad -c at=55,90,4,96 --quiet

  echo "$1" | d.text at=50,22 align=lc size=20 color=black

  d.out.file Colortable_$1 --quiet --overwrite
}

### relative scales.  run first so tables like differences with both
###  will overwrite
r.mapcalc "grad = row()/1.0"

for CTABLE in $RELATIVE ; do
  echo "[$CTABLE]"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

  #read
done


### absolute scales.
for CTABLE in $ABSOLUTE ; do
  MIN=`awk '{print $1}' "$COLOR_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' |  head -n 1`
  MAX=`awk '{print $1}' "$COLOR_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' |  tail -n 1`

  if [ `echo "$MIN" | grep -c '%'` -gt 0 ] || \
     [ `echo "$MAX" | grep -c '%'` -gt 0 ] ; then
       continue
  fi

  if [ $CTABLE = "population" ] ; then
    MAX=2500000
  fi

  echo "[$CTABLE $MIN $MAX]"

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

done


### mixed scales
for CTABLE in $MIXED ; do
  MIN=-0.04
  MAX=0.04

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

done



### custom scales
for CTABLE in `ls $ADDON_DIR` ; do
  MIN=`awk '{print $1}' "$ADDON_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' | head -n 1`
  MAX=`awk '{print $1}' "$ADDON_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' | tail -n 1`
  echo "[$CTABLE $MIN $MAX]"

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad rules="$ADDON_DIR/$CTABLE" --quiet
  draw_and_output $CTABLE

done

echo "Files written to <$OUTPUT_DIR>"


Script to generate mini-thumbnail versions:
by H.Bowman (GRASS wiki license) Requires GRASS 6.5+ newer than Sept. 2009.

#!/bin/sh

# customize this:
ADDON_DIR="/path/to/grass/svn/grass-addons/raster/r.colors.tools/palettes"

g.region n=85 s=0 w=0 e=15 res=1

d.mon x0
d.resize h=85 w=15

COLOR_DIR="$GISBASE/etc/colors/"
cd "$COLOR_DIR"

RELATIVE=`grep '%' * | cut -f1 -d: | grep -v "matches" | uniq`
ABSOLUTE=`grep -v '%' * | cut -f1 -d: | grep -v "matches" | uniq`
MIXED=`grep '%' $ABSOLUTE | cut -f1 -d: | grep -v "matches" | uniq`

GRASS_OVERWRITE=1
export GRASS_OVERWRITE

OUTPUT_DIR=/tmp/grass/colortables/
rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
cd $OUTPUT_DIR

draw_and_output()
{
  d.erase
  d.colortable -n grad
  d.out.file Colortable_$1 --quiet --overwrite
  convert -rotate 90 Colortable_$1.png Colortable_$1.png
}

### relative scales.  run first so tables like differences with both
###  will overwrite
g.region -d res=600 -a
r.mapcalc "grad = row()/1.0"

for CTABLE in $RELATIVE ; do
  echo "[$CTABLE]"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

  #read
done


### absolute scales.
for CTABLE in $ABSOLUTE ; do
  MIN=`awk '{print $1}' "$COLOR_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' |  head -n 1`
  MAX=`awk '{print $1}' "$COLOR_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' |  tail -n 1`

  if [ `echo "$MIN" | grep -c '%'` -gt 0 ] || \
     [ `echo "$MAX" | grep -c '%'` -gt 0 ] ; then
       continue
  fi

  if [ $CTABLE = "population" ] ; then
    MAX=2500000
  fi

  echo "[$CTABLE $MIN $MAX]"

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

done


### mixed scales
for CTABLE in $MIXED ; do
  MIN=-0.04
  MAX=0.04

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad color=$CTABLE --quiet
  draw_and_output $CTABLE

done



### custom scales
for CTABLE in `ls $ADDON_DIR` ; do
  MIN=`awk '{print $1}' "$ADDON_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' | head -n 1`
  MAX=`awk '{print $1}' "$ADDON_DIR/$CTABLE" | sort -n | grep -v '^#\|^nv' | tail -n 1`
  echo "[$CTABLE $MIN $MAX]"

  GRASS_VERBOSE=0 \
    r.mapcalc "grad = if(row()==1, 1.0 * $MIN, $MAX)"

  r.colors grad rules="$ADDON_DIR/$CTABLE" --quiet
  draw_and_output $CTABLE

done

echo "Files written to <$OUTPUT_DIR>"
