#!/bin/bash
for i in {0..4096};
do
    l=`./bashloop $i`
	if [ "$l" != "Nope. Pick another number between 0 and 4096" ]
	then
	    echo $l
	fi
done   