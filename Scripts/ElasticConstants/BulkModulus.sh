#!/bin/bash

# ./run.sh filename volumeOfCrystal lattice_parameter
#volume of crystal = actual volume 
#lattice_parameter=actual_lattice_parameter

path= pwd
rm -rf $path"BulkModulus"
mkdir $path"BulkModulus"

dataFile=bulkModulus.dat

echo -e "#delta\t\t\t\tEnergy_density">$path"BulkModulus/"$dataFile


for fraction in 0.91 0.92 0.93 0.94 0.95 0.96 0.97 0.98 0.99 1 1.01 1.02 1.03 1.04 1.05 1.06 1.07 1.08 1.09 
do
			
	orginalCrystal=$1
	volume=$2
	lattic=$3	
	affinedCrystal=$file"Frac_"$fraction
	finalVol=$(bc<<<"scale=8;$fraction*$volume")
	affineScale -m $orginalCrystal -o $affinedCrystal".omd" -v $finalVol

	mpirun -n 16 openmd_MPI $affinedCrystal".omd"

	#get last line of a file
	line=$( grep . $affinedCrystal".stat" | tail -1 )
	
	delta=$(bc<<< "scale=8;($finalVol-$volume)/$volume")
	echo $delta
	cohesive=$(echo $line| awk '{print $2}')
		
	cohesiveDensity=$(bc<<< "scale=8;$cohesive/$volume")
	echo $cohesiveDensity
	#echo $line display the value of line
	#awk '{print $2}',prints second field of previously displayed line
	#$(...) holds the output and let assign it to cohesive


	writelines=$(echo -e $delta"\t\t\t\t"$cohesiveDensity)


	#write to a file
	echo $writelines >> $path"BulkModulus/"$dataFile
	fileName=$path$affinedCrystal	
	mv {$fileName".omd",$fileName".stat",$fileName".eor",$fileName".dump"} $path"BulkModulus/."
	


done

