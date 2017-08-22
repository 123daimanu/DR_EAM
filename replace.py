import sys

file_in=sys.argv[1]
run=sys.argv[3]

fileOmd=open(file_in)  

lines=fileOmd.readlines()
lineNewFile=[]
for line in lines:
    words=line.split()

    if "runTime" in words:
	line="runTime = "+str(run)+" ;\n"
    if "sampleTime" in words:
	line="sampleTime ="+str(float(run)/float(100))+" ;\n"
           
    
    lineNewFile.append(line)
fileOmd.close()
file_out=sys.argv[2]

fileOut=open(file_out,"w")
fileOut.writelines(lineNewFile)
fileOut.close()   
