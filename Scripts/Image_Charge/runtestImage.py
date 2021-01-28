import sys
import argparse
import textwrap
import numpy as num
import os
import subprocess
from argparse import RawDescriptionHelpFormatter


def usage():
    print __doc__


def getEnergy(filename):
    en=float(os.popen("tail -1 %s"%(filename)).read().split()[1])
    return en

def getPEnergy(filename):
    pe=float(os.popen("tail -1 %s"%(filename)).read().split()[2])
    return pe

def getKEnergy(filename):
    ke=float(os.popen("tail -1 %s"%(filename)).read().split()[3])
    return ke

def runSimulation(fileIn):
    os.system("mpirun -n 4 openmd_MPI %s"%(fileIn))
    #subprocess.call(["openmd",fileIn])
    
def moveChlorine(filename,position,newfile):
    l=open(filename);
    lines=l.readlines()
    f=open(newfile,'w')
    lines[-4]=position
    newstring=''.join(lines)
    f.write(newstring)
    l.close()
    f.close()

def moveChlorineWriteCharge(filename,position,newfile,nMatoms,charge):
    l=open(filename);
    lines=l.readlines()
    f=open(newfile,'w')
    lines[-4]=position
    last=lines.pop() #saves </OpenMD>
    last2=lines.pop() #saves </Snapshot>
    lines.append("<SiteData>\n")
    chargePerAtom=charge/float(nMatoms)
    for atomIndex in range(nMatoms):
        lines.append(chargeSites(atomIndex,chargePerAtom))
    lines.append("%d cw 0 0 \n"%(nMatoms))
    lines.append("</SiteData>\n")
    lines.append(last2)
    lines.append(last)
    newstring=''.join(lines)

    f.write(newstring)
    l.close()
    f.close()



def stringPos(n,x,y,z):
    return('\t%d \tpv\t%f\t%f\t%f\t0\t0\t0\n'%(n,x,y,z))

def chargeSites(n,c):
    return('\t%d \tcw\t%f\t%f\n'%(n,c,0))
    

def atop(x,y):
    return x,y

def bridge(x1,y1,x2,y2):
    return (x1+x2)/2.0,(y1+y2)/2.0

def hollow(x1,x2,x3,y1,y2,y3):
    return (x1+x2+x3)/3.0,(y1+y2+y3)/3.0

def imageCharge(fileIn,fileOut,x1,y1,x2,y2,x3,y3,x4,y4,zPlane,save,f,n,c):
    outTag=fileOut

    fTOutput=open("%stop.dat"%(outTag),"w")
    fBOutput=open("%sbridge.dat"%(outTag),"w")
    fHOutput=open("%shollow.dat"%(outTag),"w")


    fTOutput.write("#z=%f\tenergy\tKE\tPE\n"%(zPlane))
    fBOutput.write("#z=%f\tenergy\tKE\tPE\n"%(zPlane))
    fHOutput.write("#z=%f\tenergy\tKE\tPE\n"%(zPlane))

    fTOutput.close()
    fBOutput.close()
    fHOutput.close()





    if (f=="111"):
        xT,yT=atop(x1,y1)
        xB,yB=bridge(x1,y1,x2,y2)
        xH,yH=hollow(x1,x2,x3,y1,y2,y3)
    else:
        xT,yT=atop(x1,y1)
        xB,yB=bridge(x1,y1,x2,y2)
        xH,yH=bridge(x1,x3,y1,y3)
    
    Z=num.linspace(zPlane+1,25,20)

    i=1
    for z1 in Z:
        if (save=='true'):
             fTOmd="%stop%d.omd"%(outTag,i)
             fBOmd="%sbridge%d.omd"%(outTag,i)
             fHOmd="%shollow%d.omd"%(outTag,i)
   
             fTStat="%stop%d.stat"%(outTag,i)
             fBStat="%sbridge%d.stat"%(outTag,i)
             fHStat="%shollow%d.stat"%(outTag,i)
        else:
             fTOmd=outTag+"top.omd"
             fBOmd=outTag+"bridge.omd"
             fHOmd=outTag+"hollow.omd"
   
             fTStat=outTag+"top.stat"
             fBStat=outTag+"bridge.stat"
             fHStat=outTag+"hollow.stat"



 
        tString=stringPos(n,xT,yT,z1)
        bString=stringPos(n,xB,yB,z1)
        hString=stringPos(n,xH,yH,z1)

        if c==0:

            moveChlorine(fileIn,tString,fTOmd)
            moveChlorine(fileIn,bString,fBOmd)
            moveChlorine(fileIn,hString,fHOmd)

        else:

            moveChlorineWriteCharge(fileIn,tString,fTOmd,n,c)
            moveChlorineWriteCharge(fileIn,bString,fBOmd,n,c)
            moveChlorineWriteCharge(fileIn,hString,fHOmd,n,c)
 


         
        print("Running for z = %f atop site"%(z1))
        runSimulation(fTOmd)
        
        print("Running for z = %f bridge site"%(z1))
        runSimulation(fBOmd)
        
        print("Running for z = %f hollow site"%(z1))
        runSimulation(fHOmd)
 
   
        
        tEnergy=getEnergy(fTStat)
        bEnergy=getEnergy(fBStat)   
        hEnergy=getEnergy(fHStat)

        tKEnergy=getKEnergy(fTStat)
        bKEnergy=getKEnergy(fBStat)
        hKEnergy=getKEnergy(fHStat)

        tPEnergy=getPEnergy(fTStat)
        bPEnergy=getPEnergy(fBStat)
        hPEnergy=getPEnergy(fHStat)
    
    
        fTOutput=open("%stop.dat"%(outTag),"a+")
        fBOutput=open("%sbridge.dat"%(outTag),"a+")
        fHOutput=open("%shollow.dat"%(outTag),"a+")


    
        fTOutput.write("%f\t%f\t%f\t%f\n"%(z1-zPlane,tEnergy,tKEnergy,tPEnergy))
        fBOutput.write("%f\t%f\t%f\t%f\n"%(z1-zPlane,bEnergy,bKEnergy,bPEnergy))
        fHOutput.write("%f\t%f\t%f\t%f\n"%(z1-zPlane,hEnergy,hKEnergy,hPEnergy))


        fTOutput.close()
        fBOutput.close()
        fHOutput.close()

        i=i+1
  

def main(argv):
    parser = argparse.ArgumentParser(
        description='Run the calculations for generating the potential for Image charge.',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""
                    Example: python2.7 -i PtWithChloride.omd -c1 [x1,y1] -c2 [x2,y2] -c3 [x3,y3] -z 14.44 -o PtImage -s true -n 1372 -f 111
                    
                                        c1---------c2                            c1                              O Cl-
                                        |           |                           / |                              |
                                        |           |                          /  |                              | 
                                        |           |                         /   |                     ---------------------- z=+Z
                                        |           |                        /    |    
                                        |           |                       /     |                     
                                        c4----------c3                     c3-----c2                   ------------------------- -

                                      for  110 FCC Facet                for 111 FCC facet                z=a is positive top most plane
                    """)

    parser.add_argument("-i","--input=", action="store",
                        dest="inFile", help="Input the .omd file")
    parser.add_argument("-c1","--co-ordinate1=", action="store",nargs="+", type=float,
                        dest="co1", help="coordinate of first vertex of triange")
    parser.add_argument("-c2","--co-ordinate2=", action="store",nargs="+", type=float,
                        dest="co2", help="coordinate of second vertex of triange")
    parser.add_argument("-c3","--co-ordinate3=", action="store",nargs="+", type=float,
                        dest="co3", help="coordinate of third vertex of triange")
    parser.add_argument("-c4","--co-ordinate4=", action="store",nargs="+", type=float,
                        dest="co4", help="coordinate of fourth vertex of of rectangle")

    parser.add_argument("-z","--zcoordinate=", action="store", type=float,
                        dest="z", help="z coordinate of plane of triangle")

    parser.add_argument("-n","--number=", action="store", type=int,
                        dest="n", help="number of metal atoms in system")
    parser.add_argument("-o","--output-file=", action="store", dest="outFile",help="tag for the output file")
    parser.add_argument("-s","--save-file=", action="store", dest="save",choices=('true','false'),default='false',help="true/false for saving the dump files")
    parser.add_argument("-f","--face=", action="store", dest="f",choices=('110','111','100'),help="(111/110/100) the exposed surface")
    parser.add_argument("-c","--charge=", action="store", dest="c",type=float,default=0,help="Total charge of metallic slab")



    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(2)
    
    args=parser.parse_args()


    if (not args.inFile):
        parser.error("No omd file specified")
    
    if ((not args.co1) or (not args.co2) or (not args.co3)):
        parser.error("Vertices of triangle missing")

    x1,y1=args.co1
    x2,y2=args.co2
    x3,y3=args.co3
    x4,y4=0,0
    if ((not args.f)):
        parser.error("Exposed facet missing")
    f=args.f

    if (f=='110' or f =='100'):
        if (not args.co4):
            parser.error("Cooridinate of rectangle missing")
        x4,y4=args.co4
 

    if (not args.z):
        parser.error("Z plane of triangle not specified")

    z=args.z
    
    if (not args.n):
        parser.error("No of metal atoms not found")
    n=args.n

    if (not args.outFile):
        parser.error("No tag for output file specified")

    s=args.save
    
    imageCharge(args.inFile,args.outFile,x1,y1,x2,y2,x3,y3,x4,y4,z,s,f,int(n),args.c)



if __name__ == "__main__":
    main(sys.argv[1:])




