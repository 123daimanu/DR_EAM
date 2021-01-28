import sys

file_in=sys.argv[1]
file_out=sys.argv[2]
efield=str(float(sys.argv[3]))
print("Efield is %s"%(sys.argv[3]))
fileOmd=open(file_in)  

fileOut=open(file_out,"w")
lines=fileOmd.readlines()
lineNewFile=[]
change=True
for line in lines:
    words=line.split()

    if "uniformField" in words:
	line="uniformField = ( 0, 0 , "+efield+");\n"
           
    
    lineNewFile.append(line)
fileOut.writelines(lineNewFile)
fileOut.close()   
