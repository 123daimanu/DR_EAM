rm "Result.dat"
for name in Cu Ag Au Ni Pd Pt Al Pb Fe Mo Ta Co
do

	tail -1 $name"Vacancy.stat"
done
