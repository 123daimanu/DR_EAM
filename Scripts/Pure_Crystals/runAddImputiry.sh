#!/bin/sh'`
for host in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta W Co Ti Zr
do
	
	for impurity in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta W Co Ti Zr
	do
		if [ $host != $impurity ]
		then
			echo "Host = "$host" :: Impurity = "$impurity	
			python2.7 AddImpurity.py $host".omd" $host$impurity".omd" $impurity"_FQ"
			openmd $host$impurity".omd"
		fi
done	
done
