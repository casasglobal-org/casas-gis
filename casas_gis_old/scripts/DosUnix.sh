#!/bin/bash
# set -x
# Convert windows text file to a Unix text file.
cd ~/outfiles/;

echo ""

for i in `ls *.txt`
do
    echo "...converting text file $i"
	tr -d '\15\32' < $i > unix$i
	wait;
	rm $i
done

echo ""

for i in `echo unix*`
do
	echo "...renaming $i"
	mv $i ${i/unix/}
done

echo ""
echo "Done!"
echo ""

exit 0