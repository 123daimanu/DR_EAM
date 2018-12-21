
# extract information from dump file.
import numpy as num
import os
import sys
import argparse
from argparse import RawDescriptionHelpFormatter
sys.path.append("/home/hbhattar/afs/Hemanta/metals/pythonScripts/function")
#------------------------------------------------------------------------
#os.chdir("/home/hbhattar/afs/Hemanta/metals/pythonScripts/function")
import FDEAM as feam
#os.chdir("/home/hbhattar/afs/Hemanta/metals/pythonScripts/pythonfile")
#--------------------------------------------------------------------------




def main(argv):
    parser = argparse.ArgumentParser(
        description='Uses dump extractor to extract the information about the layer charge, field and position',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="Example: layerInfo -i ../KTuninig/src/Slab111Z18DSF.dump -f 100 -o Slab111Z18DSF.dat -n 1080")
    parser.add_argument("-i","--inputfile=", action="store", dest="fileIn", help="input dump file")

    parser.add_argument("-f","--frames=", action="store", type=int,
                        dest="frames", help="No of frames")

    parser.add_argument("-o","--datfile=", action="store", dest="datfile",help="use specified data file output")

    parser.add_argument("-n","--nMol", action="store", type=int,
                        dest="nMol", help="number of atoms")


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)
    args = parser.parse_args()

    if (not args.fileIn):
        parser.error("No input dump file was specified")

    if (not args.frames):
        parser.print_help()
        parser.error("No number of frames was specified")

    if (not args.nMol):
        parser.print_help()
        parser.error("No number of atom specified")

    if (not args.datfile):
        parser.print_help()
        parser.error("No output data file specified")

    file=args.fileIn
    frames=args.frames
    nMol=args.nMol
    rawData=feam.DumpExtractor(args.fileIn,frames,nMol,0)
    [vxe,vye,vze]=rawData["velocity"]
    [xe,ye,ze]=rawData["position"]
    [ce,we]=rawData["chargeQV"]
    [exe,eye,eze]=rawData["electricField"]
    [layere,ae]=feam.Layers(ze,nMol)
    begin=0
    eavze=[]
    eavxe=[]
    eavye=[]
    chave=[]
    zave=[]
    for counter in range(len(ae)):
        eavze.append(num.sum(num.sum(eze[begin:,layere[counter][0]],axis=1)/len(layere[counter][0]))/(frames-begin))
        chave.append(num.sum(num.sum(ce[begin:,layere[counter][0]],axis=1)/len(layere[counter][0]))/(frames-begin))
        eavxe.append(num.sum(num.sum(exe[begin:,layere[counter][0]],axis=1)/len(layere[counter][0]))/(frames-begin))
        eavye.append(num.sum(num.sum(eye[begin:,layere[counter][0]],axis=1)/len(layere[counter][0]))/(frames-begin))
        zave.append(num.sum(num.sum(ze[begin:,layere[counter][0]],axis=1)/len(layere[counter][0]))/(frames-begin))

    fileOut=open(args.datfile,'w')
    for counter in range(len(ae)):
        fileOut.write("%d\t%e\t%e\t%e\t%e\t%e\n"%(counter,zave[counter],chave[counter],eavxe[counter],eavye[counter],eavze[counter]))
    fileOut.close()    

if __name__ == "__main__":
    #if len(sys.argv) == 1:
        #parser.print_help()
        #usage() # need to change to call argeparse stuffs
        #sys.exit()
    main(sys.argv[1:])
