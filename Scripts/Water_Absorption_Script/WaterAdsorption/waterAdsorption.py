import numpy as num
import os
import sys
import re
from argparse import RawDescriptionHelpFormatter
import argparse
import textwrap
import frcWriter as frc

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
    near=num.argsort(dist)[0]
    return near,dist[near]

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


def error(omdfile,nMol,d0,E0,theta0,eRef):
    eorfile=omdfile[:-3]+"eor"
    extracted=DumpExtractor(eorfile,1,nMol)
    angleWater=angle(extracted['q'])
    near,distance=nearest(extracted["position"])
    energyS=StatExtractor(omdfile[:-3]+"stat")
    energy=energyS-eRef
    error=num.sqrt(((distance-d0))**2+((energy-E0))**2+((angleWater-theta0))**2)
    return error,distance,angleWater,energyS,energy

def gradE(fxph,fx,h):
    return (fxph-fx)/h

def changeFrc(em,er,sm,sr,frcFile):
    frc.writer(em,er,sm,sr,frcFile)

def runSimulation(omdFile):
    delete(omdFile)
    os.system("~/PERSONAL/OpenMD/build/bin/openmd %s"%(omdFile))



def delete(omdFile):
    name=omdFile[:-3]
    os.system("rm %sdump"%(name))
    os.system("rm %sstat"%(name))
    os.system("rm %seor"%(name))

def optimization(omdFile,nMol,em,er,sm,sr,d0,E0,theta0,eRef,frcFile,gamma,h):
    frcData=[em,er,sm,sr]
    errorData=[]
    for pos in range(-1,4):
        if pos==-1:
            changeFrc(em,er,sm,sr,frcFile)
            runSimulation(omdFile)
            erb=error(omdFile,nMol,d0,E0,theta0,eRef)
            errorBase=erb[0]
        else:
            frcData[pos]=frcData[pos]+h
            em1,er1,sm1,sr1=frcData
            changeFrc(em1,er1,sm1,sr1,frcFile)
            runSimulation(omdFile)
            err=error(omdFile,nMol,d0,E0,theta0,eRef)
            errorData.append(err[0])
            print(err)
            print(err)

    err=num.array(errorData)
    grad=gradE(err,errorBase,h)
    frcData=num.array([em,er,sm,sr]) 
    print(grad)
    newpara=num.subtract(frcData,gamma*grad)
    return(newpara)

def optimizePtWater(omdFile,nMol,em,er,sm,sr,d0,E0,theta0,eRef,frcFile,gamma,h,iterations,out):
    outFile=open(out+"GDResult.dat","w")
    outFile.write("d0\tAngle0\tEnergy0\tError\n")
    outFile.close()

    outFile1=open(out+"GDParam.dat","w")
    outFile1.write("em\ter\tsm\tsr\tError\n")
    outFile1.close()
    for coutIter in range(iterations):
        outFile=open(out+"Result.dat","a+")
        outFile1=open(out+"Param.dat","a+")
        print("\n%d iterations running"%(coutIter))
        em,er,sm,sr=optimization(omdFile,nMol,em,er,sm,sr,d0,E0,theta0,eRef,frcFile,gamma,h)
        changeFrc(em,er,sm,sr,frcFile)
        runSimulation(omdFile)
        err,dist,ang,eneS,ene=error(omdFile,nMol,d0,E0,theta0,eRef)
        print("em: %f er: %f sm: %f sr:%f Energy: %f"%(em,er,sm,sr,ene))
        print("\ndist: %f angle: %f energy: %f erro: %f" %(dist,ang,ene,err))
        outFile.write("%f\t%f\t%f\t%f\n" %(dist,ang,ene,err))
        outFile1.write(" %f\t%f\t%f\t%f\t%f\n"%(em,er,sm,sr,err))
        outFile.close()
        outFile1.close()

def GridSearch(omdFile,nMol,em,er,sm,sr,d0,E0,theta0,eRef,frcFile,iterations,deltaS,deltaE,out):
    paramOut=out+"GridParam.dat"
    resultOut=out+"GridResult.dat"
    outParam=open(paramOut,"w+")
    outResult=open(resultOut,"w+")
    outParam.write("em\ter\tsm\tsr\terror\n")
    outResult.write("d0\tAngle0\tEnergy0\terror\n")
    outParam.close()
    outResult.close()
    iterate=num.array(range(-iterations//2,iterations//2))
    emArray=em+iterate*deltaE
    erArray=er+iterate*deltaE
    smArray=sm+iterate*deltaS
    srArray=sr+iterate*deltaS
    param=[[x,y,z,p] for x in emArray for y in erArray for z in smArray for p in srArray]
    for parameters in param:
        emm,err,smm,srr=parameters
        changeFrc(emm,err,smm,srr,frcFile)
        runSimulation(omdFile)
        errSim,dist,angle,eneS,ene=error(omdFile,nMol,d0,E0,theta0,eRef)
        
        outParam=open(paramOut,"a+")
        outParam.write("%f\t%f\t%f\t%f\t%f\n"%(emm,err,smm,srr,errSim))
        outParam.close()
        
        outResult=open(resultOut,"a+")
        outResult.write("%f\t%f\t%f\t%f\n"%(dist,angle,ene,errSim))
        outResult.close()

    

def usage():
    print __doc__

def main(argv):
    parser = argparse.ArgumentParser(
        description='Run the calculations to tune the water and Metal potential',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""
                    Example: python2.7 waterAdsorption.py -i Pt1Water.omd -n 1372 -g 0.01 -dh 0.001 -d0 2.43 -t0 14 -e0 -7010.4 -er 900000 -f frc.frc -it 1000 -s 2 2 3 3
                """)
   
    parser.add_argument("-s","--start=", action="store",
                        dest="s",nargs="+",type=float,help="Starting value of em,er,sm,sr")
 
    parser.add_argument("-it","--itera=", action="store",
                        dest="iterations",type=int,default=10, help="number of iterations,default=10")
    parser.add_argument("-i","--input=", action="store",
                        dest="inFile", help="Input the .omd file")
    parser.add_argument("-g","--stepsize=", action="store",default=0.001, type=float,
                        dest="g", help="Step size used in gradient descent, default=0.0001")
    parser.add_argument("-dh","--delta=", action="store",default=0.001, type=float,
                        dest="dh", help="delta used to find derivaties, default=0.001")
    parser.add_argument("-d0","--distance=", action="store", type=float,
                        dest="d0", help="expected distance")
    parser.add_argument("-e0","--energy=", action="store", type=float,
                        dest="e0", help="expected energy")

    parser.add_argument("-t0","--angle=", action="store", type=float,
                        dest="t0", help="expected angle")

    parser.add_argument("-n","--number=", action="store", type=int,
                        dest="n", help="number of  atoms in system (metal atoms + 1)")
    parser.add_argument("-o","--output-file=", action="store", dest="outFile",help="output file to report all energy and parameters")
    parser.add_argument("-er","--ref-energy=", action="store", dest="er",type=float,help="reference energy of metal + water monomer without cross interactions")
    parser.add_argument("-f","--frc-file=", action="store", dest="f",help="Name of the forcefield file used")
    parser.add_argument("-m","--method=",action="store",dest="method",choices=('G','O'),default="G",help="[G/O] Choose the search method used G(Grid Search)/O(Gradient Descent optimization)")
    parser.add_argument("-dE","--deltaE=",action="store",dest="dE",type=float,default=0.1,help="Step size for epsilon for grid search,default=0.1")
    parser.add_argument("-dS","--deltaS=",action="store",dest="dS",type=float,default=0.01,help="Step size for sigma for grid search,default=0.01")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(2)

    args=parser.parse_args()


    if (not args.inFile):
        parser.error("No omd file specified")
    
    omdFile=args.inFile

    if ((not args.d0) or (not args.e0) or (not args.t0)):
        parser.error("Expected value of distance, energy or anlge missing")
    d0=args.d0
    e0=args.e0
    t0=args.t0

    if (not args.f):
        parser.error("Force field not given")

    if (not args.s):
        parser.error("Starting value missing")

    s=args.s

    if(len(s)!=4):
        parser.error("start values not in correct format")
                                                                        
    if (not args.er):
        parser.error("Reference energy of metal slab missing")

    eRef=args.er
    print(eRef)

    if (not args.n):
        parser.error("No of metal atoms not found")
    nMol=args.n
    print(nMol)

    if (not args.outFile):
        parser.error("Output file specified")

    outFile=args.outFile
    em,er,sm,sr=s

    if (args.method=="O"):
        optimizePtWater(omdFile,nMol,em,er,sm,sr,d0,e0,t0,eRef,args.f,args.g,args.dh,args.iterations,outFile)

    if (args.method=="G"):
        GridSearch(omdFile,nMol,em,er,sm,sr,d0,e0,t0,eRef,args.f,args.iterations,args.dS,args.dE,outFile)
 
    


if __name__ == "__main__":
    main(sys.argv[1:])


                            
