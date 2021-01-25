import sys

file_in=sys.argv[1]
file_out=sys.argv[2]
efield=str(float(sys.argv[3])*10**-1)

fileOmd=open(file_in)  

fileOut=open(file_out,"w")
lines=fileOmd.readlines()
lineNewFile=[]
change=True
for line in lines:
    words=line.split()

    if "uniformField" in words:
	line="uniformField = ( 0, 0 ,"+efield+");"
           
    
    lineNewFile.append(line)
fileOut.writelines(lineNewFile)
fileOut.close()   
