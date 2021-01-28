
for name in NiMg AgTi AlMg AlTi AuCu NiFe PdFe PdTi PtCo PtFe PtNi ZrMg
do

	i=1
	while [ $i -le 20 ]
	do
		echo "Running "$i" simulation"	
		if [ $i -eq 1 ]
		then

			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10.omd" -b > "Data"$name"New.elastic"
		#	~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10Zhou.omd" -b > "Data"$name"Zhou.elastic"
		else
			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10.eor" -b > "Data"$name"New.elastic"
		#	~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10Zhou.eor" -b > "Data"$name"Zhou.elastic"

		fi

	#	elasticConstants -i $name"L10.eor" -b > "Data"$m$rc$name".elastic"
	#	elasticConstants -i $name"L10Zhou.eor" -b > "Data"$m$rc$name"Zhou.elastic"


		python2.7 extractor.py "Data"$name"New.elastic" "box"$name"New.dat" 10 $i
		#python2.7 extractor.py "Data"$m$rc$name"Zhou.elastic" "box"$name"Zhou.dat" 10 $i

		i=$(( $i+1 ))
	done
done

