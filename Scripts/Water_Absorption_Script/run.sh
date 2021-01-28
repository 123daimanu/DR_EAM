#!/bin/sh'

rm "Result.dat"
echo "# em	er 	sm	sr	energy	distance	angle">"Result.dat"

energyMie=( 1.5 1.7 1.9)

energyRepulsive=(0.1)

sigmaMie=( 3.0 3.1 3.2 3.3)

sigmaRepulsive=(0.1 0.15 0.2)

fileName="metalWater.frc"

nMol=1537

omdFile="WaterAu.omd"

for em in "${energyMie[@]}"
do
	for er in "${energyRepulsive[@]}"
	do
		for sm in "${sigmaMie[@]}"
		do
			for sr in "${sigmaRepulsive[@]}"
			do
				#creates a new force field file
				python2.7 frcWriter.py $sm $em $sr $er  $fileName
		
				#runs simulation
				
				mpirun -np 2 openmd_MPI $omdFile>"status.file"
				echo $em $er $sm $sr $status
				tail -1 "status.file"
				echo "+++++++++++++++++++++++++"
				python2.7 outData.py $omdFile $em $er $sm $sr "Result.dat" $nMol

				rm {*.stat,*.eor,*.dump}

			done
      		done

	done

done

