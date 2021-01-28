#!/bin/sh'
for name in Pt Ag Al Au Cu Fe Mo Ni Pb Pd Pt Ta
do
	echo $name	
	python2.7 omdEdit.py $name".omd" $name".omd"
		
done
