#!/bin/sh'`
rm "Result.dat"
for name in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta W Mg Co Ti Zr
do
	echo $name	
	python2.7 outData.py $name "Result.dat"
		
done
