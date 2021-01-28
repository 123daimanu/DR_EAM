#!/bin/sh'`
for host in Pt Ag Al Au Cu Fe Mo Ni Pb Pd Pt Ta
do
	
	for impurity in Pt Ag Al Au Cu Fe Mo Ni Pb Pd Pt Ta
	do
		if [ $host != $impurity ]
		then
			echo "Host = "$host" :: Impurity = "$impurity	
			charge= tail -4 $host$impurity".eor"|head -1
			echo $charge
			echo "-------------------------------------"
		fi
done	
done
