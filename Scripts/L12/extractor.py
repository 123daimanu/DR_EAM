import sys
import re

File=sys.argv[1]
lineNo=int(sys.argv[3])
FileOut=sys.argv[2]
i=int(sys.argv[4])
file1=open(File)
fileOut=open(FileOut,'a+')
lines1=file1.readlines()
outLine1=lines1[lineNo]
outLine2=lines1[lineNo+1]
outLine3=lines1[lineNo+2]
    
match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    
outData1 = [float(x) for x in re.findall(match_number, outLine1)][0]
outData2 = [float(x) for x in re.findall(match_number, outLine2)][1]
outData3 = [float(x) for x in re.findall(match_number, outLine3)][2]
print(outData1,outData2)
fileOut.write("%d\t%f\t%f\t%f\n"%(i,outData1,outData2,outData3))
fileOut.close()



