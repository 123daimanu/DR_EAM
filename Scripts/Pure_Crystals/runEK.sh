#!/bin/sh'`
rm "Result.dat"
for name in Pt Ag Al Au Cu Fe Mo Ni Pb Pd Pt Ta Mg Co Ti Zr W
do

      	file=$name".omd"


		



	#openmd $editedFile".omd"
	echo $file" Running !!!!!!"
	~/PERSONAL/OpenMD/build/bin/openmd $file


	python2.7 MakeVaccum.py $name".omd" $name"Vaccum.omd"
	python2.7 RipOneAtomOut.py	$name".omd" $name"Vacancy.omd"
	
	echo $name"Vaccum.omd file running!!!!!"
	~/PERSONAL/OpenMD/build/bin/openmd $name"Vaccum.omd"

	echo $name"Vacancy.omd file running!!!!"
	~/PERSONAL/OpenMD/build/bin/openmd $name"Vacancy.omd"

	cp $file $name"Elastic.omd"
	echo $name"Elastic.omd file running!!!"
	~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"Elastic.omd" -m "energy" >$name"Elastic.dat"
	
	
	python2.7 outData.py $name "Result.dat"
		



done
