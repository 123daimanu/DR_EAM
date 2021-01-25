import numpy as num
import sys
#From .xyz file. The program deletes the line containing information about the snapshot.

# python xyzEditCharge.py Pt_test_diffusion.xyz Pt_test_diffusion.qd
infile=sys.argv[1]
outfile=sys.argv[2]


xyzFile=open(infile)
lines=xyzFile.readlines()
atoms=str.split(lines[0])[0]
length=len(lines[1])
linesAppend=[]
for line in lines:
	lineApp=str.split(line);
	if(lineApp[0]==atoms or len(line)==length):
		continue;
	last="\n"
	lineApp.append(last)
	sep="\t"
	linesAppend.append(sep.join(lineApp))
	
	
xyzFileNew=open(outfile,"w")
xyzFileNew.writelines(linesAppend)
