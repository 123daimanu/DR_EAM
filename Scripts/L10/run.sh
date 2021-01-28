rm "Result1.dat"
rm "ResultZhou1.dat"
outFile="Result1.dat"
outFileZhou="ResultZhou1.dat"
for name in PdFe AlMg NiMg ZrMg AgTi
do
		
	echo $A "running..."

	
	
	i=1
	while [ $i -le 20 ]
	do
		echo "Running "$i" simulation for "$name
		
		if [ $i -eq 1 ]
		then
			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10.omd" -b > "Data"$name".elastic"
			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10Zhou.omd" -b > "Data"$name"Zhou.elastic"
		
		else

			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10.eor" -b > "Data"$name".elastic"
			~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10Zhou.eor" -b > "Data"$name"Zhou.elastic" 		
		fi	
			
		python2.7 extractor.py "Data"$name".elastic" "box"$name".dat" 10 $i
		python2.7 extractor.py "Data"$name"Zhou.elastic" "box"$name"Zhou.dat" 10 $i

		i=$(( $i+1 ))
	done
	
	~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10.eor" -b > "Data"$name".elastic"
	~/PERSONAL/OpenMD/build/bin/elasticConstants -i $name"L10Zhou.eor" -b > "Data"$name"Zhou.elastic" 		
	
	python2.7 infoExtract.py "Data"$name".elastic" $name"L10.stat" $outFile
	python2.7 infoExtract.py "Data"$name"Zhou.elastic" $name"L10Zhou.stat" $outFileZhou	


done
