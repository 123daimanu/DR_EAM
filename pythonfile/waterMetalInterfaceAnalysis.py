#!/usr/bin/env python
# coding: utf-8

# In[39]:


# extract information from dump file.
import numpy as num
import matplotlib.pyplot as plt
import pylab as lab
from scipy import constants
import scipy as sci
import pandas as pan
import os
from collections import OrderedDict
from scipy.optimize import curve_fit
import sys


system_ =sys.argv[1]

path = "/home/hbhattar/afs/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
#system_ = "MNWN_Dynamics.dump"
system = (path + system_)[:-5]


# In[45]:


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
            fCount=fCount+1
            index=0
            continue;

        elif(fCount>=frames):
            break;

        else:
            processP=processP;



        if (processP=="Start"):
            x[fCount][int(linesSplit[0])]=float(linesSplit[2])
            y[fCount][int(linesSplit[0])]=float(linesSplit[3])
            z[fCount][int(linesSplit[0])]=float(linesSplit[4])
            vx[fCount][int(linesSplit[0])]=float(linesSplit[5])
            vy[fCount][int(linesSplit[0])]=float(linesSplit[6])
            vz[fCount][int(linesSplit[0])]=float(linesSplit[7])



    position=[x,y,z]
    velocity=[vx,vy,vz]
    


    infoDict={"position":position,"velocity":velocity}
    return infoDict


# In[ ]:





# ## for MNWN

# In[35]:



info = DumpExtractor(system+".dump",1000,4925)


# In[36]:


x,y,z=info["position"]


# In[37]:




import matplotlib.pyplot as plt


# In[44]:


z_av_metal = []
for frame in range(0,1000):
    z_surf = z[frame,:1799][z[frame,:1799]>15.5]
    z_av_metal.append(num.mean(z_surf))
    
fig,ax= plt.subplots(nrows=1,ncols=1)
plt.plot(z[:,:1799])
#plt.ylim([-20,-15.5])
plt.savefig('%s1.pdf'%(system))
plt.close(fig)




fig,ax= plt.subplots(nrows=1,ncols=1)
plt.plot(z_av_metal)
plt.savefig('%s2.pdf'%(system))
plt.close(fig)

# In[12]:


#plt.plot(z[:20,1800:],'.')
#plt.ylim([19,21])
#plt.show()


# In[13]:


#plt.plot(z[5,1800:][z[5,1800:]>0],'.')
#plt.ylim([19,21])


# In[41]:

fig,ax= plt.subplots(nrows=1,ncols=1)
for frame in range(0,10):
    ax.plot(num.sort(z[frame,1800:][num.logical_and(z[frame,1800:]>19, z[frame,1800:]<21)])[:200],'.')
    ax.set_ylim([19,21])
plt.savefig('%s3.pdf'%(system))
plt.close(fig)



    
z_av_water = []
for frame in range(0,1000):
    z_surf = z[frame,1800:][num.logical_and(z[frame,1800:]>19, z[frame,1800:]<21)]
    z_av_water.append(num.mean(z_surf))
    


# In[42]:

plt.plot(z_av_water,z_av_metal,".")
plt.savefig('%s4.pdf'%(system))
plt.close(fig)


# In[43]:


d = num.array(z_av_water) - num.array(z_av_metal)



fig,ax= plt.subplots(nrows=1,ncols=1)
plt.plot(d)
plt.savefig('%s5.pdf'%(system))
plt.close(fig)

bins = num.linspace(19,25,1000)


surf_atoms_hist = num.zeros(bins.size-1)
for frame in range(1000):
    surf_atoms = num.sort(z[frame,1800:][z[frame,1800:]>0])[:400]
    hist , bins = num.histogram(surf_atoms, bins,)
    surf_atoms_hist = hist + surf_atoms_hist
    


z_av_water = []
for frame in range(0,1000):
    z_surf = z[frame,1800:][num.logical_and(z[frame,1800:]>19, z[frame,1800:]<21)]
    z_av_water.append(num.mean(z_surf))

    
    
    
from scipy.optimize import curve_fit
    
def doubleGauss(x,x1,x2,a1,a2,A1,A2,A):
    return A + A1 * num.exp(-a1*(x-x1)**2) + A2 * num.exp(-a2*(x-x2)**2)

const, var = curve_fit(doubleGauss, bins[:-1],surf_atoms_hist,[19.5,22.5,1,1,1600,600,0])
x1,x2,a1,a2,A1,A2,A = const


fig,ax= plt.subplots(nrows=1,ncols=1)
plt.plot(bins[:-1],surf_atoms_hist)
plt.plot(bins[:-1,],doubleGauss(bins[:-1],x1,x2,a1,a2,A1,A2,A),'r')
plt.savefig("%s6.pdf"%(system))
plt.close(fig)

fig,ax= plt.subplots(nrows=1,ncols=1)
plt.plot(bins[:-1],surf_atoms_hist)
plt.savefig("%s7.pdf"%(system))
plt.close(fig)


f=open("%s.dat"%(system),'w')
f.write(str(num.mean(d)))
f.write("\n x1 = %f\tx2 = %f"%(x1,x2))
f.write("\n metal_av = %f"%(num.mean(z_av_metal)))
f.close()
print(num.mean(d))


# In[27]:


#for frame in range(0,1000):
#    plt.plot(z[frame,1800:],'.')
#    plt.hlines(y=-74,xmin=0,xmax=3300)
#    plt.hlines(y=74,xmin=0,xmax=3300)
#    plt.xlim([0,3300])


# ## for MFWN

# In[ ]:




