#!/bin/bash

# ./run.sh filename  volume -x x-length 
# x-length = actual x-length of crystal
#volume= actual volume of crystal
#-x direction of extension
path= pwd
rm -rf $path"YoungsModulus"
mkdir $path"YoungsModulus"

dataFile=youngsModulus.dat

echo -e "#delta\t\t\t\tEnergy_density">$path"YoungsModulus/"$dataFile

for fraction in 0.995 0.996 0.997 0.998 0.999 1 1.001 1.002 1.003 1.004 1.005 
do
			
	orginalCrystal=$1
	xlen=$4
	volume=$2
	affinedAxis=$3
	affinedCrystal=$file"Frac_Lx"$fraction
	finalXLen=$(bc<<<"scale=8;$fraction*$xlen")
	affineScale -m $orginalCrystal -o $affinedCrystal".omd" $affinedAxis $finalXLen

	mpirun -n 16 openmd_MPI $affinedCrystal".omd"

	#get last line of a file
	line=$( grep . $affinedCrystal".stat" | tail -1 )
	
	delta=$(bc<<< "scale=8;($finalXLen-$xlen)/$xlen")
	echo $delta
	cohesive=$(echo $line| awk '{print $2}')
		
	cohesiveDensity=$(bc<<< "scale=8;$cohesive/$volume")
	echo $cohesiveDensity
	#echo $line display the value of line
	#awk '{print $2}',prints second field of previously displayed line
	#$(...) holds the output and let assign it to cohesive


	writelines=$(echo -e $delta"\t\t\t\t"$cohesiveDensity)


	#write to a file
	echo $writelines >> $path"YoungsModulus/"$dataFile
	fileName=$path$affinedCrystal	
	mv {$fileName".omd",$fileName".stat",$fileName".eor",$fileName".dump"} $path"YoungsModulus/."
			
done

