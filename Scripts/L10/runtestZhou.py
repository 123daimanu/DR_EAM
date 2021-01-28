import os
import numpy as num
import subprocess
import sys
import re

def getEnergy(filename):
    en=float(os.popen("tail -1 %s"%(filename)).read().split()[1])
    return en

def getEOF(filename):
    eof=os.popen("tail -1 %s"%(filename)).read().split()[0]
    return eof
def getBoxGeometry(filename):
    box=os.popen("grep Hmat %s"%(filename)).read()
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    lx = [float(x) for x in re.findall(match_number, box)][0]
    ly = [float(x) for x in re.findall(match_number, box)][4]
    lz = [float(x) for x in re.findall(match_number, box)][8]
    return lx,ly,lz
def getrCut(filename):
    r=os.popen("grep cutoffRadius %s"%(filename)).read()
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    rCut = [float(x) for x in re.findall(match_number, r)]
    return rCut[0]

def sampleCA(lx,ly,lz,rCut,delta,points):
    c,a=lx,ly
    interval=num.arange(points)-points//2
    caSampling=[[c+x*delta,a+y*delta] for x in interval for y in interval if (c+x*delta>2*rCut and a+y*delta>2*rCut)]
    return caSampling

def scaledStructure(fileIn,fileOut,latticeInfo):
    os.system("affineScale -m %s -o %s -x %f -y %f -z%f>log.txt"%(fileIn,fileOut,latticeInfo[0],latticeInfo[1],latticeInfo[1]))


def runSimulation(fileIn):
    os.system("~/PERSONAL/OpenMD/build/bin/openmd %s"%(fileIn))
    #subprocess.call(["openmd",fileIn])
    

def affineScaled(fileIn,fileOut,omdFile):
    c,a=os.popen("tail -1 %s"%(fileIn)).read().split()[1:3]
    c,a=float(c),float(a)
    print([c,a])
    os.system("affineScale -m %s -o %s -x %f -y %f -z %f"%(omdFile,fileOut,c,a,a))

def extract(fileName,lineNo):
    file1=open(fileName)
    lines1=file1.readlines()
    outLine1=lines1[lineNo]
    outLine2=lines1[lineNo+1]
    outLine3=lines1[lineNo+2]
    
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    
    outData1 = [float(x) for x in re.findall(match_number, outLine1)][0]
    outData2 = [float(x) for x in re.findall(match_number, outLine2)][1]
    outData3 = [float(x) for x in re.findall(match_number, outLine3)][2]

    return outData1,outData2,outData3


path="../L10/"
points = 20
delta = 0.1
n = 3

#true if the structure is optimized first and false if we are doing raw search from initial random configuration
baseOpto=True


systemName=["AgTi","AlMg","AlTi","AuCu","NiFe","NiMg","PdFe","PdTi","PtCo","PtFe","PtNi","ZrMg"]
#systemName=["AuCu","NiMg","PtFe","PtNi"]
for name in systemName:
    elandScape=[]
    if baseOpto:
        fileIn=path+"boxSD8"+name+"Zhou.dat"
        eorfile=path+name+"L10Zhou.eor"
        omdfile=path+name+"L10Zhou.omd"
        affineScaled(fileIn,eorfile,omdfile)
    else:
        eorfile=path+name+"L10Zhou.omd"
    rCut=getrCut(eorfile)
    lx,ly,lz=getBoxGeometry(eorfile)
    caList=sampleCA(lx,ly,lz,rCut,delta,points)
    scaledfile=path+"ScaledZhou.omd"
    scaledfileStat=path+"ScaledZhou.stat"
    scaledfiledump=scaledfile[:-3]+"dump"
 
    landScape=path+name+".Zhoulandscape"
    fileLS=open(landScape,'w')
    fileLS.write("#c\t#a\tEnergy\n")
    for data in caList:
        print("Running for "+str(data)+name)
        try:
            scaledStructure(eorfile,scaledfile,data)
            runSimulation(scaledfile)
            eof=getEOF(scaledfiledump)
            if eof == "</OpenMD>":
                print("Sim Success")
                energy=getEnergy(scaledfileStat)
                fileLS=open(landScape,'a')
                fileLS.write("%f\t%f\t%f\n"%(data[0]/(2*n+1),data[1]/(2*n+1),energy/(4*(2*n+1)**3)))
                fileLS.close()
            else:
                print("Crashed")
        except:
            print("Crashed!!!!")


    fileLS.close()
