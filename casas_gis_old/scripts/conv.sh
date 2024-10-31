#!/bin/bash
cd ~/outfiles/;
echo
echo "Please move files you want to convert into the \"outfiles\" folder,"
echo
echo "then press [ENTER]..."
echo
read franco
#~ for i in `ls *.txt`;
for i in *.txt;
do
    echo "Converting text file $i ...";
	tr -d '\15\32' < $i > unix$i;
	rm $i
	wait;
done

#~ for i in `echo unix*`;
for i in unix*;
do
	mv $i ${i/unix/};
	wait;
done
echo "Done."

echo
echo "Please press [ENTER] to quit."
echo
read franco

exit


