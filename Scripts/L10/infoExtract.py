import sys
import re


fileIn=sys.argv[1]
fileInStat=sys.argv[2]
file_out=sys.argv[3]
fileElastic = open(fileIn)
fileStat=open(fileInStat)
fileOut=open(file_out,"a+")


linesElastic=fileElastic.readlines()
linesStat=fileStat.readlines()[-1]
outLine1=linesElastic[10]
outLine2=linesElastic[11]
    
match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')

cohEnergy=0.0433641153087705*[float(x) for x in re.findall(match_number,linesStat)][1]/1372.0
outData1 = [float(x) for x in re.findall(match_number, outLine1)][0]
outData2 = [float(x) for x in re.findall(match_number, outLine2)][1]

for line in linesElastic:
    word=line.split()
    if "Bulk" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        bulk = [float(x) for x in re.findall(match_number,word[2])]
    if "Shear" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        shear = [float(x) for x in re.findall(match_number,word[2])]
    
    if "Young's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        youngs = [float(x) for x in re.findall(match_number,word[3])]
     
    if "Poisson's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        poisson = [float(x) for x in re.findall(match_number,word[2])]

    if "Universal" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        universal = [float(x) for x in re.findall(match_number,word[3])]

    
 







#c|a|c/a|Bulk|Youngs|Elatic_anisotropy|Poissons_ratio|cohesiveEnergy
print("%s\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\n"%(fileIn[4:8],outData1/7.0,outData2/7.0,outData1/float(outData2),bulk[0],shear[0],poisson[0],cohEnergy))
fileOut.write("%s\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\n"%(fileIn[4:8],outData1/7.0,outData2/7.0,outData1/float(outData2),bulk[0],shear[0],poisson[0],cohEnergy))
fileOut.close()



