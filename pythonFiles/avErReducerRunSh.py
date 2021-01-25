__author__ = 'jmichalk'


import sys
import os.path
import re
import math
import numpy
'''Example: python inputfilename.stat  numberofreducedframe columnnumberwhoseaverageistaken file_name value_of_k'''

#------------------------------------------------modification form Joes code
newFrameNumber=int(sys.argv[2])
num=int(sys.argv[3])
fileOut=sys.argv[4]
valueOfk=sys.argv[5]

#------------------------------------------------------------------------

# A class to hold information about each frame
class Frame:
    """Frame class"""
    def __init__(self, bins):
        self.bins = bins


#endregion


#region file input
if len(sys.argv) == 1:
    filename = ""
else:
    try_filename = sys.argv[1]
    if "stat" in try_filename:
        filename = try_filename
        print "Filename: %s" % filename
    else:
        print "(" + try_filename + ") contained errors, please submit a valid edge ordering file."
        filename = ""

while(filename == ""):
    print "Please enter a filename to process: "
    try_filename = raw_input("Filename: ---> ")
    if "stat" in try_filename:
        filename = try_filename
    else:
        print "(" + try_filename + ") contained errors, please submit a valid eodat file."

file_exists = os.path.isfile(filename)
if (file_exists == False):
    print "File %s does not exist" % (filename)
    print "Quitting"
    exit(0)

#endregion

frames = []
bins = []
#region reading file
file_handle = open(filename, 'r')
#......................................... changed from Joescript
count=0
#........................................
for line in file_handle:
    if "#" in line:
        pass
    else:
        linelist = line.split()
       # frameIndex = int(linelist[0])
	#frames.append(frameIndex)

#-----------------------------------------------------------changes from Joes script
	count=count+1
	frames.append(count)
#-----------------------------------------------------------
	dipole = float(linelist[num])
        bins.append(dipole)


#endregion



#region Analyze/Shrink data
collapsedFrames = []

print "Current number of frames: %d" % (len(bins))
#-----------------------------------------------------------------------------------------------------------------------------
#newFrameNumber = float(raw_input("Please enter the desired number of frames (integer ratios are preferred, i.e. 990/10=99: "))

#-----------------------------------------------------------------------------------------------------------------------------
ratio  = len(bins)/newFrameNumber

print "Current frames: %d\t New Frames: %d\t Approximate Frame ratio: %f\n" % (len(bins), newFrameNumber, ratio)

newData=[];
for counter in range(len(bins)-1,len(bins)-ratio-1,-1):
	newData.append(bins[counter]);
	

newdataArray=numpy.array(newData);
newdataMean=numpy.mean(newdataArray);
newdataRMS=numpy.sqrt(numpy.mean((newdataArray-newdataMean)**2))


#-------------------------------------------------------------------------
print("Mean:=%s"%(newdataMean));
print("RMS=%s"%(newdataRMS));

#----------------------------------------------------------------write to afile---------------
f=open(fileOut,'a+')
f.write("\n%d\t\t\t%s\t\t\t%s"%(int(valueOfk),newdataMean,newdataRMS))
f.close()
