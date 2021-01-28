import sys
import re


file1=open(sys.argv[1])
k=sys.argv[2]
E=sys.argv[3]
width=sys.argv[4]
lines1=file1.readlines()
pxl=lines1[11]
pyl=lines1[12]
pzl=lines1[13]
match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
px = [float(x) for x in re.findall(match_number, pxl)]
py = [float(x) for x in re.findall(match_number, pyl)]
pz = [float(x) for x in re.findall(match_number, pzl)]
linestored="\n"+str(k)+"\t\t"+str(pz[0])+"\t\t"+str(pz[1])
file3=open(sys.argv[5]+"PolarizationZ"+width+"E"+E+".dat","a+")
file3.write(linestored)
file3.close()

