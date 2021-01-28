path="../Simulation/"


for E in 0 2
do
	for thickness in 9 12 15 18 21 24
	do
		file=$path"PtSlab111Z"$thickness"K_14E_"$E
		fileShrink=$file"Shrink"

		python2.7 omdShrink -s 100 -m $file".dump" -o $file".dump"


	done
done
