#!/bin/sh'
rm hostImpurity.dat
for host in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta W Co Ti Zr
do
	
	for impurity in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta W Co Ti Zr
	do
		if [ $host != $impurity ]
		then
			echo "Host = "$host" :: Impurity = "$impurity	
			python2.7 hostImpurity.py $host $impurity hostImpurity.dat
		fi
done	
done
