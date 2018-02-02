#!/bin/sh'
base=2
thickness="8"
for name in Pt
do
	for E in 0.5 1 1.5 2 2.5 3
	do
		for k in 200 250 300 350 400 450 500 550
		do
			
                        file="PtSlab111Z_"$thickness
			
			editedFile=$file"E_"$E



			#change electric field of the omd file
			python2.7 efieldEdit.py $file".omd" $editedFile".omd" $E

			rm metalsFQ.frc

			#change k value on the frc file
			python frcWriter.py $name $k 


			
			file_stat=$file"K_"$k"E_"$E".stat"
			file_dump=$file"K_"$k"E_"$E".dump"
			file_eor=$file"K_"$k"E_"$E".eor"

			mpirun -n 16 openmd_MPI $editedFile".omd"

			mv $editedFile".stat" $file_stat
			mv $editedFile".dump" $file_dump
			mv $editedFile".eor" $file_eor
			
		        #write the polarization in the file name
			
			python polarization.py $editedFile".report" $k $E $thickness
		done
	done
done

