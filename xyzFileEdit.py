#!/usr/bin/python
import numpy as num
from sys import argv
IFile=argv[1]
OFile=argv[2]

# Program that edits .xyz file making the charge of sodium 0 so that we can see correct distribution of charge in the jmol.



xyzFile=open(IFile)			#opens the initial .xyz file
lines=xyzFile.readlines()
linesAppend=[]
for line in lines:
	lineApp=str.split(line);
	if(lineApp[0]=="Na+"):
		lineApp[4]="0";  # edits the charge of Sodium to 0
	last="\n"
	lineApp.append(last)
	sep="\t"
	linesAppend.append(sep.join(lineApp))
xyzFileNew=open(OFile,"w")
xyzFileNew.writelines(linesAppend)
xyzFileNew.close()
