#!/bin/sh'
base=2
E=0
buildPath="/home/hbhattar/PERSONAL/build/bin/"
outFrc="../forcefield/"
outSim="../Simulation/"
outData="../Data/"
name="Pt"
NDATA=15
for ((k=${OMPI_COMM_WORLD_RANK};k<${NDATA};k=${k}+${PBS_NP}))
do
	echo ${OMPI_COMM_WORLD_RANK}"simulating for vale of" ${k}
	for E in  0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09
	do
		for thickness in 21 
		do
			
                        file="PtSlab111Z"$thickness
			
			
			editedFile=$file"O_6E_"$E
			file_stat=$file"O_6K_"$k"E_"$E".stat"
			file_dump=$file"O_6K_"$k"E_"$E".dump"
			file_eor=$file"O_6K_"$k"E_"$E".eor"
			file_report=$file"O_6K_"$k"E_"$E".report"
			file_omd=$file"O_6K_"$k"E_"$E".omd"
	


			#change electric field of the omd file
			python2.7 efieldEdit.py $outSim$file".omd" $editedFile".omd" $E

			rm $outFrc"metalsFQ.frc"

			#change k value on the frc file
			python frcWriter.py $name $k $outFrc


			
			echo "K= "$k"_______ E= "$E
			#openmd $editedFile".omd"
			mpirun -np 9 openmd_MPI $editedFile".omd"
			# mpirun -np 4 $buildPath"openmd_MPI" $editedFile".omd"
		        #write the polarization in the file name
			python polarization.py $editedFile".report" $k $E $thickness $outData
			
			mv $editedFile".stat" $outSim$file_stat
			mv $editedFile".dump" $outSim$file_dump
			mv $editedFile".eor" $outSim$file_eor
			mv $editedFile".report" $outSim$file_report
			mv $editedFile".omd" $outSim$file_omd

			
		done
	done
done

