
# coding: utf-8

# Program that extracts the information about the position and velocity of atoms in each sites along with charge and charge velocity at those sites in each frames.
# 
# 
# path="" refers to the path of the dump file from which data is to be extracted
# 
# frames=------ number of frames during openmd execution
# 
# atomNumber=----------- total number of atomic sites during program execution

# In[1]:

# extract information from dump file.
import numpy as num
import matplotlib.pyplot as plt
from matplotlib import use
import pylab as lab
from scipy import constants
from matplotlib import rcParams
import os

from scipy.optimize import curve_fit

os.chdir("/home/hbhattar/afs/Hemanta/metals/pythonScripts/function")

import FDEAM as feam

os.chdir("/home/hbhattar/afs/Hemanta/metals/pythonScripts/")



#setting different parameteres
params = {
    'font.family':'serif',
   'axes.labelsize': 12,
   'font.size': 12,
   'legend.fontsize': 12,
   'xtick.labelsize': 12,
   'ytick.labelsize': 12,
   'text.usetex': False,
   'figure.figsize': [5,5],
    'figure.max_open_warning': 0
   }
rcParams.update(params)
get_ipython().magic('matplotlib inline')




# In[22]:

#Write the information about outer layers and the charge and z gradient wrt number of layers


KET=[[k,e,t] for k in range(10,27,2) for e in [0.1,0.2,0.3] for t in range(9,41,3)]
fileName=[]
for info in [[10,1,9]]:
    fileName.append("PtSlab111Z"+str(info[2])+"K_"+str(info[0])+"E_"+str(info[1])+".dump")
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}

frames=100
for info in KET:
    file="PtSlab111Z"+str(info[2])+"K_"+str(info[0])+"E_"+str(info[1])+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,100,nMol[str(info[2])],0)
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,atoms)
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue;
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    
    const=num.polyfit(zav[3:-3],chav[3:-3],1)
    dat=[]
    print("Writing::: K:%f  E:%  T:%f"%(info[0],info[1],info[2]))
    fileData=open("../KTuning/Results/ZSlopeResultK_"+str(info[0])+"E_"+str(info[1])+".dat","a+")
    fileData.write(str(info[2]))
    for var in zav[:3]:
        fileData.write("\t")
        fileData.write(str(var))
    for var in zav[-3:]:
        fileData.write("\t")
        fileData.write(str(var))
    for var in chav[:3]:
        fileData.write("\t")
        fileData.write(str(var))
    for var in chav[-3:]:
        fileData.write("\t")
        fileData.write(str(var))
    fileData.write("\t")
    fileData.write(str(const[0]))
    fileData.write("\n")
    fileData.close()
    


# In[ ]:

KET=[[k,e,t] for k in range(10,25) for e in [3] for t in [9,12,15,18,21,24,27,30,33,36,39]]
frames=100
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}

for info in KET:
    file="PtSlab111Z24"+"K_"+str(info[0])+"E_"+str(info[1])+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(info[2])],0)
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,2000)
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue;
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    
    const=num.polyfit(zav[3:-3],chav[3:-3],1)
    dat=[]
    print("Writing::: K:%f  E:%f"%(info[0],info[1]))
    fileData=open("../KTuning/Results/SlopeK_"+str(info[0])+".dat","a+")
    fileData.write(str(info[1]))
    fileData.write("\t")
    fileData.write(str(const[0]))
    fileData.write("\n")
    fileData.close()
    


# In[ ]:

KET=[[k,e] for k in range(10,39) for e in [1,3,4,5,6,7,8,9]]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100

for info in KET:
    file="PtSlab111Z24"+"K_"+str(info[0])+"E_"+str(info[1])+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(info[2])],0)
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,2000)
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    
    const=num.polyfit(zav[3:-3],chav[3:-3],1)
    dat=[]
    print("Writing::: K:%f  E:%f"%(info[0],info[1]))
    fileData=open("../KTuning/Results/SlopeE_"+str(info[1])+".dat","a+")
    fileData.write(str(info[0]))
    fileData.write("\t")
    fileData.write(str(const[0]))
    fileData.write("\n")
    fileData.close()
    


# In[4]:

#plot Z and calculate slopes dq/dz dq/dn dz/dn


efield=['0.3']
curvatures=[60]
thickness=[36]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100
KET=[[k,e,t] for k in curvatures for e in efield for t in thickness]


for info in KET:
    file="PtSlab111Z"+str(info[2])+'N_4'+"K_"+str(info[0])+"E_"+info[1]+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(info[2])],0)
        
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,nMol[str(info[2])])
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    const0=num.polyfit(zav[3:-3],chav[3:-3],1)
    const1=num.polyfit(range(len(chav[3:-3])),chav[3:-3],1)
    const2=num.polyfit(range(len(zav[3:-3])),zav[3:-3],1)
    print("=========K:%d=====E:%s=======T:%d======\n"%(info[0],info[1],info[2]))
    print("M_qz: %f\nM_q: %f\nM_z: %f\nM_q/M_z: %f\n\n"%(const0[0],const1[0],const2[0],const1[0]/const2[0]))
    lab.plot(zav,'o')
    lab.xlabel("Layer Index")
    lab.ylabel("Average")
    lab.show()
    


# In[2]:

efield=['0.02','0.03','0.04','0.05','0.06','0.07','0.08']
curvatures=[1,5,10]
thickness=[36]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100
KET=[[k,e,t] for k in curvatures for e in efield for t in thickness]
innerLayer=8
OutResultDen=[] #list of list i.e [[k,e,dipole],[...],[....]]
OutResultDPole=[]
A=28.805999*16.631151
for info in KET:
    file="PtSlab111Z"+str(info[2])+'N_4'+"K_"+str(info[0])+"E_"+info[1]+".dump"
    try:
        print("Reading: "+"../KTuning/Simulation/"+file)
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(info[2])],0)
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,nMol[str(info[2])])
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    eavz=num.array(eavz)*(1e-1)/23.0609    #convert to V/ang
    const0=num.polyfit(zav[8:-8],chav[8:-8],1)
    const1=num.polyfit(range(len(chav[8:-8])),chav[8:-8],1)
    const2=num.polyfit(range(len(zav[8:-8])),zav[8:-8],1)
    numberPerLayer=2*len(layer[8][0])
    dz=abs(zav[14]-zav[13])
    
    
    
    dipoleDen=const1[0]*len(layer[8][0])/(A*2)
    dipole=const0*dz*dz/4
    
    
    print("=========K:%d=====E:%f=======T:%d======\n"%(info[0],float(info[1])*1e-1,info[2]))
    print(dipoleDen*1.6e-19,dipole[0]*1.6e-19)
    
    OutResultDen.append([info[0],float(info[1])*1e-1,dipoleDen*1.6e-19])
    OutResultDPole.append([info[0],float(info[1])*1e-1,dipole[0]*1.6e-19])
    
    fig=plt.figure(figsize=(10,10),)
    
    ax1=fig.add_subplot(2,2,1)
    ax1.plot(range(1,len(a)+1),eavz)
    ax1.set_xlabel("Layer Index")
    ax1.set_ylabel("Ez")
    
    ax2=fig.add_subplot(2,2,2)
    ax2.plot(range(1,len(a)+1),chav)
    ax2.set_xlabel("Layer Index")
    ax2.set_ylabel("<q>")
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    
    
    ax3=fig.add_subplot(2,2,3)
    ax3.plot(eavz[8:-8])
    ax3.set_xlabel("Layer Index(inner[8:-8])")
    ax3.set_ylabel("Ez")
    
    ax4=fig.add_subplot(2,2,4)
    ax4.plot(chav[8:-8])
    ax4.set_xlabel("Layer Index(inner)[8:-8]")
    ax4.set_ylabel("<q>")
    ax4.yaxis.tick_right()
    ax4.yaxis.set_label_position("right")
    
    fig.suptitle('k:%f   E:%s'%(info[0],info[1]))
    plt.draw()
OutResultDen=num.array(OutResultDen)
OutResultDPole=num.array(OutResultDPole)

#print("densitywritting")
#num.savetxt("../KTuning/Results/KEDDensity.out",OutResultDen)
#num.savetxt("../KTuning/Results/KEDPole.out",OutResultDPole)
     
     
    


# In[7]:


OutResult3=num.loadtxt('../KTuning/Results/KEDDensity.out')




o3=OutResult3[3:]
lab.plot(o3[:-2,1],o3[:-2,2],'ob--')
lab.xlabel("E(V/Ang)")
lab.ylabel("Pz(C Ang^{-2})")
lab.show()




dat3=num.array(feam.CurvatureSlope(num.array(OutResult3[3:])))



lab.plot(dat3[:,0],dat3[:,1],'o')
lab.xlabel("k")
#lab.ylabel("alpha(A^3)")
lab.show()


# In[26]:

OutResult3=num.loadtxt('../KTuning/Results/KED.out')




o3=OutResult3[3:]
lab.plot(o3[:-2,1],o3[:-2,2],'ob--')
lab.xlabel("E(V/Ang)")
lab.ylabel("Pz(C Ang)")
lab.show()




dat3=num.array(feam.CurvatureSlope(num.array(OutResult3[3:])))
fitFx=lambda x,a,c:a/(x+c)
param=curve_fit(fitFx,dat3[:,0],dat3[:,1])
print(param)




lab.plot(dat3[:,0],dat3[:,1],'o')
lab.xlabel("k")
lab.ylabel("alpha(A^3)")
lab.plot(dat3[:,0],fitFx(dat3[:,0],param[0][0],param[0][1]),'o')
lab.show()

print(param[0][0]/6.1-param[0][1])


# In[45]:

efield=['0.02']
curvatures=[20]
thickness=[36]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100
KET=[[k,e,t] for k in curvatures for e in efield for t in thickness]


for info in KET:
    file="PtSlab111Z"+str(info[2])+"K_"+str(info[0])+"E_"+info[1]+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(info[2])],0)
        
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,nMol[str(info[2])])
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    eavz=num.array(eavz)*1e-1
    chav=num.array(chav)
    zav=num.array(zav)
    const0=num.polyfit(zav[3:-3],chav[3:-3],1)
    const1=num.polyfit(range(len(chav[3:-3])),chav[3:-3],1)
    const2=num.polyfit(range(len(zav[3:-3])),zav[3:-3],1)
    print("=========K:%d=====E:%s=======T:%d======\n"%(info[0],info[1],info[2]))
    print("M_qz: %f\nM_q: %f\nM_z: %f\nM_q/M_z: %f\n\n"%(const0[0],const1[0],const2[0],const1[0]/const2[0]))
    lab.plot(zav,'o')
    lab.xlabel("Layer Index")
    lab.ylabel("Average")
    lab.show()
num.savetxt("../KTuning/Results/dataN10K20E10.out",(eavz,chav,zav))
    


# In[65]:

data4=num.loadtxt('../KTuning/Results/dataN4K20E10.out')
data1=num.loadtxt('../KTuning/Results/dataN1K20E10.out')
data10=num.loadtxt('../KTuning/Results/dataN10K20E10.out')
data=num.loadtxt('../KTuning/Results/data.out')


# In[84]:

lab.plot(data10[1][:],'.-r')
lab.plot(data4[1][:],'-.b')
lab.plot(data1[1][:],'-.g')
#lab.plot(data[1][:],'-.k')

lab.xlabel("Layer")
#lab.xlim([-1,38])
#lab.ylim([0,0.05])


# In[233]:


#changing efield ,k and N
efield=['0.02','0.04']
curvatures=[20]
thickness=[36]
N=[4]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100
KEN=[[k,e,n] for k in curvatures for e in efield for n in N]


for info in KEN:
    file="PtSlab111Z"+str(thickness[0])+'N_'+str(info[2])+"K_"+str(info[0])+"E_"+info[1]+".dump"
    try:
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(thickness[0])],0)
        
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,nMol[str(thickness[0])])
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue
    
    eavz=[]
    eavx=[]
    eavy=[]
    chav=[]
    zav=[]
    begin=0
    for counter in range(len(a)):
        eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
        zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    eavz=num.array(eavz)*1e-1
    chav=num.array(chav)
    zav=num.array(zav)
    const0=num.polyfit(zav[3:-3],chav[3:-3],1)
    const1=num.polyfit(range(len(chav[3:-3])),chav[3:-3],1)
    const2=num.polyfit(range(len(zav[3:-3])),zav[3:-3],1)
    print("=========K:%d=====E:%s=======N:%d======\n"%(info[0],info[1],info[2]))
    print("M_qz: %f\nM_q: %f\nM_z: %f\nM_q/M_z: %f\n\n"%(const0[0],const1[0],const2[0],const1[0]/const2[0]))
    lab.plot(zav,'o')
    lab.xlabel("Layer Index")
    lab.ylabel("Average")
    lab.show()
    fileDataOut='../KTuning/Results/dataN'+str(info[2])+'K'+str(info[0])+'E'+info[1]+'.out'
    num.savetxt(fileDataOut,(eavz,chav,zav))


# In[16]:

# compare the data for diff N and diff E
efield=['0.02']
curvatures=[20]
thickness=[36]
N=[1,2,3,4,5,6,7,8,9,10]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
frames=100
KEN=[[k,e,n] for k in curvatures for e in efield for n in N]
#colors=feam.generate_color(36)
for info in KEN:
    fileDataOut='../KTuning/Results/dataN'+str(info[2])+'K'+str(info[0])+'E'+info[1]+'.out'
    data=num.loadtxt(fileDataOut)
    lab.plot(data[1][5:30],label=str(info[2]))
    lab.legend()



# In[14]:

2.901848048e-33/2.7000000000000003e-35


# In[56]:

lab.plot(2/eavz[8:-8],'o')



# In[8]:

rawData=feam.DumpExtractor("../KTuning/Simulation/PtSlab111Z36SmallTKConstN_2K_3E_0.dump",100,2592,0)
[vx,vy,vz]=rawData["velocity"]
[x,y,z]=rawData["position"]
[c,w]=rawData["chargeQV"]
[ex,ey,ez]=rawData["electricField"]
[layer,a]=feam.Layers(z,2592)


# In[10]:

lab.plot(c)
lab.show()


# ### Analysis for polarizablity of different layered system with constant K and constant field

# In[94]:

efield=['0.01']
curvatures=[24]
thickness=[9,12,15,18,21,24,27,30,33,36,39]
N=[1,2,3,4,5,6,7,8,9,10]
nMol={'9':648,'12':864,'15':1080,'18':1296,'21':1512,'24':1728,'27':1944,'30':2160,'33':2376,'36':2592,'39':2808}
Lx=28.805999
Ly=16.631151
Lz={'9':18.18,'12':24.95,'15':31.73,'18':38.51,'21':45.92,'24':52.08,'27':58.87,'30':65.65,'33':72.44,'36':79.23,'39':86.02}
frames=100
KEN=[[k,e,t] for k in curvatures for e in efield for t in thickness]
pz=[]
T=[]
for info in KEN:
    file="PtSlab111Z"+str(info[2])+"K_"+str(info[0])+"E_"+info[1]+".report"
    try:
        outData=feam.ReportExtractor("../KTuning/Simulation/"+file,13)
        pz.append(1e10*outData[0]/(Lz[str(info[2])]*Lx*Ly))
        T.append(info[2])
        rawData=feam.DumpExtractor("../KTuning/Simulation/"+file,frames,nMol[str(thickness[0])],0)
        [vx,vy,vz]=rawData["velocity"]
        [x,y,z]=rawData["position"]
        [c,w]=rawData["chargeQV"]
        [ex,ey,ez]=rawData["electricField"]
        [layer,a]=feam.Layers(z,nMol[str(thickness[0])])
        
    except:
        print("Error in reading "+"../KTuning/Simulation/"+file)
        continue


# In[95]:

feam.ReportExtractor('../KTuning/Simulation/PtSlab111Z36.report',11)


# In[96]:


fitFx=lambda x,a,c:a*x**2+c
param=curve_fit(fitFx,T,pz)
print(param)
lab.plot(T,pz,'o')
lab.plot(T,fitFx(num.array(thickness),param[0][0],param[0][1]))
lab.ylabel("Pz")


# In[97]:

param[0][1]


# In[99]:

cur=[4.86076688e-26,4.76413611e-26,4.65702755e-26,4.56554559e-26,4.46821079e-26,4.37919931e-26]
base=[-5.33310080e-24,-5.12569907e-24,-5.05080107e-24,-4.81750933e-24,-4.68516815e-24,-4.61546726e-24]
k=[14,16,18,20,22,24]
lab.plot(k,cur,'o')


# In[19]:

file="Slab111Z9"+"DSF.dump"
frames=100
rawData=feam.DumpExtractor("../KTuning/src/"+file,100,1080,0)
[vxd,vyd,vzd]=rawData["velocity"]
[xd,yd,zd]=rawData["position"]
[cd,wd]=rawData["chargeQV"]
[exd,eyd,ezd]=rawData["electricField"]
[layerd,ad]=feam.Layers(zd,1080)
begin=0

eavzd=[]
eavxd=[]
eavyd=[]
chavd=[]
zavd=[]
    
for counter in range(len(ad)):
    eavzd.append(num.sum(num.sum(ezd[begin:,layerd[counter][0]],axis=1)/len(layerd[counter][0]))/(frames-begin))
    chavd.append(num.sum(num.sum(cd[begin:,layerd[counter][0]],axis=1)/len(layerd[counter][0]))/(frames-begin))
    eavxd.append(num.sum(num.sum(exd[begin:,layerd[counter][0]],axis=1)/len(layerd[counter][0]))/(frames-begin))
    eavyd.append(num.sum(num.sum(eyd[begin:,layerd[counter][0]],axis=1)/len(layerd[counter][0]))/(frames-begin))
    zavd.append(num.sum(num.sum(zd[begin:,layerd[counter][0]],axis=1)/len(layerd[counter][0]))/(frames-begin))        


# In[3]:

file="Slab111Z18"+"Ewald.dump"
frames=100
rawData=feam.DumpExtractor("../KTuning/src/"+file,100,6480,0)
[vxe,vye,vze]=rawData["velocity"]
[xe,ye,ze]=rawData["position"]
[ce,we]=rawData["chargeQV"]
[exe,eye,eze]=rawData["electricField"]
[layere,ae]=feam.Layers(ze,6480)
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

    


# In[10]:

lab.plot(eavze[:],'o')
lab.xlim([-1,18])
lab.show()
print(eavze)
num.mean(eavze[3:-3]),num.std(eavze[3:-3])


# In[51]:

ae.size


# In[23]:

lab.plot(eavzd,label="d")
lab.plot(eavze,label="e")
lab.legend()
lab.show()


# In[24]:

lab.plot(chavd)
lab.plot(chave)
lab.show()


# In[25]:

rawData=feam.DumpExtractor("../KTuning/Simulation/PtSlab111Z9K_20E_0.01.dump",100,648,0)
[vx,vy,vz]=rawData["velocity"]
[x,y,z]=rawData["position"]
[c,w]=rawData["chargeQV"]
[ex,ey,ez]=rawData["electricField"]
[layer,a]=feam.Layers(z,648)
begin=0

eavz=[]
eavx=[]
eavy=[]
chav=[]
zav=[]
for counter in range(len(a)):
    eavz.append(num.sum(num.sum(ez[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    chav.append(num.sum(num.sum(c[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    eavx.append(num.sum(num.sum(ex[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    eavy.append(num.sum(num.sum(ey[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))
    zav.append(num.sum(num.sum(z[begin:,layer[counter][0]],axis=1)/len(layer[counter][0]))/(frames-begin))        

    


# In[34]:

frames=100
rawData=feam.DumpExtractor("../KTuning/src/Slab111Z9DSFSurfaceTerm.dump",100,1080,0)
[vxs,vys,vzs]=rawData["velocity"]
[xs,ys,zs]=rawData["position"]
[cs,ws]=rawData["chargeQV"]
[exs,eys,ezs]=rawData["electricField"]
[layerss,ass]=feam.Layers(zs,648)
begin=0

eavzs=[]
eavxs=[]
eavys=[]
chavs=[]
zavs=[]
for counter in range(len(ass)):
    eavzs.append(num.sum(num.sum(ezs[begin:,layerss[counter][0]],axis=1)/len(layerss[counter][0]))/(frames-begin))
    chavs.append(num.sum(num.sum(cs[begin:,layerss[counter][0]],axis=1)/len(layerss[counter][0]))/(frames-begin))
    eavxs.append(num.sum(num.sum(exs[begin:,layerss[counter][0]],axis=1)/len(layerss[counter][0]))/(frames-begin))
    eavys.append(num.sum(num.sum(eys[begin:,layerss[counter][0]],axis=1)/len(layerss[counter][0]))/(frames-begin))
    zavs.append(num.sum(num.sum(zs[begin:,layerss[counter][0]],axis=1)/len(layerss[counter][0]))/(frames-begin))        
 


# In[38]:

lab.plot(chavd,'o',label="DSF")
#lab.plot(chave,'--',label="Ewald")
lab.plot(chavs,'.--',label='DSF+Surface')
lab.xlabel("Layer Index")
#lab.ylabel("Efield (Z-Component)")
lab.legend(loc=4)
#lab.savefig("../KTuning/Efield.pdf")
lab.show()


# In[207]:

layere[counter][0]


# In[ ]:




# In[225]:

x=num.linspace(-100,100,100)


# In[232]:

lab.plot(x,x**2,'r')
lab.plot(x,x**2+.2*x**2+50*x,'g')


# In[ ]:



