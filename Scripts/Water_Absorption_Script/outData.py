import numpy as num
import os
import sys
import re


def DumpExtractor(filename,frames,atomNumber):


    """
infoDict=DumpExtractor(filename,frames,atomNumber,atomPlate)


Function that extracts the information from the .dump file created by openmd


    Inputs:
  ===========


   filename:

               Path of the dump file from which the information is to be extracted

    frame:

                Total number of frames in the dump file

    atomNumber:

                Totla number of atoms in the slab or crystal

    atomPlate:

                Total number of atoms in the capacitor plates



    Outputs:
 =============

 infoDict:

         Dictonary containing position, velocity, chargeQV, electricField, plateEQV.
         Postion is a list of [x,y,z] and each x,y,z are array of x[frames][sites]
         velocity is a list of [vx,vy,vz] and each vx,vy,vz are array of vx[frames][sites]
         chargeQV is a lisf of [c,cv] and each c and cv are array of c[frame][sites]
         electric field is list of [ex,ey,ez] and each are array of ex[frame][sites]
         plateEQV is the list of [pex,pey,pez,pc,pcv] and each are array of pex[frames][sites]
"""
    fileDump=open(filename)  #dump file for info extraction
    linesDump=fileDump.readlines()

    if(linesDump[-1]!="</OpenMD>\n"):
        print("Error: Incomplete file")
        sys.exit();
    processP="Wait"
    processC="Wait"


    #information storage matrix
    #posiiton and velocity storage
    x=num.zeros((frames,atomNumber))
    y=num.zeros((frames,atomNumber))
    z=num.zeros((frames,atomNumber))
    vx=num.zeros((frames,atomNumber))
    vy=num.zeros((frames,atomNumber))
    vz=num.zeros((frames,atomNumber))
    q=num.zeros(4)
    j=num.zeros(3)

    #charge and velocity storage matrix
    c=num.zeros((frames,atomNumber))
    cv=num.zeros((frames,atomNumber))
    ex=num.zeros((frames,atomNumber))
    ey=num.zeros((frames,atomNumber))
    ez=num.zeros((frames,atomNumber))
    efieldConverter=1.0/23.0609 # converts kcal mol^-1 to V/A
    #frame count initilization
    fCount=0
    index=0  #index for the atoms
    for line in linesDump:
        linesSplit=str.split(line)
        length=len(linesSplit)

        if(length!=0 and linesSplit[0]=="<StuntDoubles>" and processP=="Wait"):
            processP="Start"
            continue;

        elif(length!=0 and linesSplit[0]=="</StuntDoubles>" and processP=="Start"):
            processP="Wait"
            index=0
            continue;

        elif(length!=0 and linesSplit[0]=="<SiteData>" and processC=="Wait"):
            processC="Start"
            continue;

        elif(length!=0 and linesSplit[0]=="</SiteData>" and processC=="Start"):
            fCount=fCount+1
            index=0;
            processC="Wait"
            continue;

        elif(fCount>=frames):
            break;

        else:
            processP=processP;
            processC=processC;



        if (processP=="Start"):
            x[fCount][int(linesSplit[0])]=float(linesSplit[2])
            y[fCount][int(linesSplit[0])]=float(linesSplit[3])
            z[fCount][int(linesSplit[0])]=float(linesSplit[4])
            vx[fCount][int(linesSplit[0])]=float(linesSplit[5])
            vy[fCount][int(linesSplit[0])]=float(linesSplit[6])
            vz[fCount][int(linesSplit[0])]=float(linesSplit[7])

            if (linesSplit[1]=="pvqj"):
                q[0]=float(linesSplit[8])
                q[1]=float(linesSplit[9])
                q[2]=float(linesSplit[10])
                q[3]=float(linesSplit[11])
                j[0]=float(linesSplit[12])
                j[1]=float(linesSplit[13])
                j[2]=float(linesSplit[14])

        if(processC=="Start"):
            if int(linesSplit[0])<atomNumber-1:
                c[fCount][int(linesSplit[0])]=float(linesSplit[3])
                cv[fCount][int(linesSplit[0])]=float(linesSplit[4])



    position=[x,y,z]
    velocity=[vx,vy,vz]
    chargeQV=[c,cv]
    electricField=[ex,ey,ez]


    infoDict={"position":position,"velocity":velocity,"chargeQV":chargeQV,"electricField":electricField,"q":q,"j":j}
    return infoDict

def nearest(xyz):
    x=xyz[0][0][:-1]
    xw=xyz[0][0][-1]

    y=xyz[1][0][:-1]
    yw=xyz[1][0][-1]

    z=xyz[2][0][:-1]
    zw=xyz[2][0][-1]

    dist=num.sqrt((x-xw)**2+(y-yw)**2+(z-zw)**2)
    nearest=num.argsort(dist)[0]
    return nearest,dist[nearest]

def angle(q):
    costheta=q[0]**2-q[1]**2-q[2]**2+q[3]**2
    theta=num.arccos(costheta)*180/num.pi
    return theta

def ReportExtractor(reportFile,lineNo):
    file1=open(reportFile)
    lines1=file1.readlines()
    outLine=lines1[lineNo]
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    outData = [float(x) for x in re.findall(match_number, outLine)]
    return outData

def StatExtractor(statFile):
    try:
        fileStat=open(statFile)
        lines=fileStat.readlines()
        for line in lines:
            pass
        energy=float(line.split()[1])
        return energy
    except:
        print("Error: Reading statFile")
        return 999999
omdfile=sys.argv[1]
em=sys.argv[2]
er=sys.argv[3]
sm=sys.argv[4]
sr=sys.argv[5]
outfile=sys.argv[6]
nMol=int(sys.argv[7])
eorfile=omdfile[:-3]+"eor"
extracted=DumpExtractor(eorfile,1,nMol)
angleWater=angle(extracted['q'])
nearest,distance=nearest(extracted["position"])
#energy=ReportExtractor(omdfile[:-3]+"report",5)
energy=StatExtractor(omdfile[:-3]+"stat")

fileOpen=open(outfile,'a')
fileOpen.write("\n%s\t\t%s\t\t%s\t\t%s\t\t%f\t\t%f\t\t%f"%(em,er,sm,sr,energy,distance,angleWater))
fileOpen.close()
