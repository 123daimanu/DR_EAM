



import numpy as num
import matplotlib.pyplot as plt
import pylab as lab
from scipy import constants
import scipy as sci
import pandas as pan
import os
from collections import OrderedDict
from scipy.optimize import curve_fit



get_ipython().magic('matplotlib inline')
    
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
   
def DumpExtractor(filename,frames,atomNumber,atomPlate):
    
    fileDump=open(filename)  #dump file for info extraction
    linesDump=fileDump.readlines()

    processP="Wait"
    processC="Wait"


    #information storage matrix 
    #posiiton and velocity storage
    x=num.zeros((frames,atomNumber+1))
    y=num.zeros((frames,atomNumber+1))
    z=num.zeros((frames,atomNumber+1))
    vx=num.zeros((frames,atomNumber+1))
    vy=num.zeros((frames,atomNumber+1))
    vz=num.zeros((frames,atomNumber+1))


    #charge and velocity storage matrix
    c=num.zeros((frames,atomNumber+1))
    cv=num.zeros((frames,atomNumber+1))
    ex=num.zeros((frames,atomNumber+1))
    ey=num.zeros((frames,atomNumber+1))
    ez=num.zeros((frames,atomNumber+1))
    pc=num.zeros((frames,atomPlate))
    pcv=num.zeros((frames,atomPlate))
    pex=num.zeros((frames,atomPlate))
    pey=num.zeros((frames,atomPlate))
    pez=num.zeros((frames,atomPlate))

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
        
        if(processC=="Start"):
            if int(linesSplit[0])<atomNumber:
                c[fCount][int(linesSplit[0])]=float(linesSplit[3])
                cv[fCount][int(linesSplit[0])]=float(linesSplit[4])
                ex[fCount][int(linesSplit[0])]=float(linesSplit[5])
                ey[fCount][int(linesSplit[0])]=float(linesSplit[6])
                ez[fCount][int(linesSplit[0])]=float(linesSplit[7])
            elif (int(linesSplit[0])==atomNumber and linesSplit[1]=="cwe"):
                continue
                c[fCount][int(linesSplit[0])]=float(linesSplit[2])
                cv[fCount][int(linesSplit[0])]=float(linesSplit[3])
                ex[fCount][int(linesSplit[0])]=float(linesSplit[4])
                ey[fCount][int(linesSplit[0])]=float(linesSplit[5])
                ez[fCount][int(linesSplit[0])]=float(linesSplit[6])
            else:
                pc[fCount][int(linesSplit[1])]=float(linesSplit[3])
                pcv[fCount][int(linesSplit[1])]=float(linesSplit[4])
                pex[fCount][int(linesSplit[1])]=float(linesSplit[5])
                pey[fCount][int(linesSplit[1])]=float(linesSplit[6])
                pez[fCount][int(linesSplit[1])]=float(linesSplit[7])
        
    position=[x,y,z]
    velocity=[vx,vy,vz]
    chargeQV=[c,cv]
    electricField=[ex,ey,ez]
    platesEQV=[pex,pey,pez,pc,pcv]
    
    infoDict={"position":position,"velocity":velocity,"chargeQV":chargeQV,"electricField":electricField,"platesEQV":platesEQV}
    return infoDict


# In[33]:

"""Function that determines different layers in a crystal

[layer,a]= Layers(ZPosition,atomNumber)
 
  Input:
 ========
 
         ZPosition: Z Coordinates of lattice for layer determination
         
         atomNumber: total Number of atoms in crystal
         
         
  Output:
 =========
         list [layer,a]; layer has index for atoms in each layers and "a" has the z-coordinates for each layers
         
         
"""
def Layers(ZPosition,atomNumber):
    a=num.sort(list(set(ZPosition[0,0:atomNumber-1])))
    layer=[]
    for var in a:
        layer.append(num.where(ZPosition[0]==var))
    
    return [layer,a]


# In[34]:

def LayerDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        print("dump")
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        aveZpos=[]
    
    
        for counter in range(len(a)):
            totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
            averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            aveZpos.append(num.sum(pos[2][UsedFrame:,layer[counter][0]])/totalData)
        
        
        
        diff=[]
        precharge=0
        prez=0
        for counter in range(len(a)):
            diff.append((averageChargeLayers[counter]-precharge)*(aveZpos[counter]-prez))
            precharge=averageChargeLayers[counter]
            prez=aveZpos[counter]
    
         
        if plotBool==True:
            lab.plot(range(1,len(a)),diff[1:],'o-')
            lab.xlabel("Layers")
            lab.ylabel("LayerDipole")
            lab.title("E = "+str(E)+" || K = "+str(K))
            lab.grid()
            lab.show()
        dipole=num.sum(diff[4:-4])/float(len(diff)-9)
        #dipole=num.sum(diff[4:-4])/float(len(diff)-9)
        
        return dipole
    
        
    except:
        print("Corrupt File")
        return 999999
    
    
    


# In[35]:

def LayerFitDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        aveZpos=[]
    
    
        for counter in range(len(a)):
            totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
            averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            aveZpos.append(num.sum(pos[2][UsedFrame:,layer[counter][0]])/totalData)
        
        n=num.arange(1,len(a)+1-8)
        if len(a)%2==0:
            n=n-num.ceil((len(a)+1-8)/2)  # shfting 1 2 3 4 5 6 to -3 -2 -1 1 2 3
            n[n>=0]=n[n>=0]+1
        else:
            n=n-num.ceil((len(a)-8)/2)
            
        
            
        fitFx=lambda x,a:a*x
        paramCharge=curve_fit(fitFx,n,averageChargeLayers[4:-4])
        paramZPos=curve_fit(fitFx,n,aveZpos[4:-4])
        
        averageChargeFitted=fitFx(n,paramCharge[0])
        averageZPosFitted=fitFx(n,paramZPos[0])
        
        
        #lab.plot(aveZpos[4:-4],averageChargeLayers[4:-4],"or")
        #lab.plot(averageZPosFitted,averageChargeFitted,"og")
        
        
        dipolefitted=num.sum(averageChargeFitted*averageZPosFitted)/num.size(averageChargeFitted)
        diff=[]
        precharge=0
        prez=0
        for counter in range(len(a)-8):
            diff.append((averageChargeFitted[counter]-precharge)*(averageZPosFitted[counter]-prez))
            precharge=averageChargeFitted[counter]
            prez=averageZPosFitted[counter]
    
         
        if plotBool==True:
            lab.plot(range(1,len(a)),diff[1:],'o-')
            lab.xlabel("Layers")
            lab.ylabel("LayerDipole")
            lab.title("E = "+str(E)+" || K = "+str(K))
            lab.grid()
            lab.show()
        dipole=num.sum(diff[5:-4])/float(len(diff)-9)
        
        #dipole=num.sum(diff[4:-4])/float(len(diff)-9)
        print(dipole,dipolefitted)
        return [dipole,dipolefitted]
    
        
    except:
        print("Corrupt File")
        return 999999


# In[36]:

def SlabDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        charge=dump["chargeQV"]
        z=pos[2][UsedFrame,:]
        c=charge[0][UsedFrame,:]
        dipole=num.sum(num.multiply(z,c))
        return dipole
    
    except:
        print("Corrupt File")
        return 999999
    


# In[37]:

def ChargeVZPos(dumpFile,frames,UsedFrame,atomNumber,atomPlate,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        averagePos=[]
        
        
        if plotBool==True:
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y'                , 'k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            for counter in range(len(a)):

                totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
                averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
                averagePos.append(num.sum(pos[2][:,layer[counter][0]])/totalData) 
                
            
            lab.plot(averagePos,averageChargeLayers,"o")
            #handles, labels = ax.get_legend_handles_labels()
            #lgd=lab.legend(bbox_to_anchor=(1.5,1),loc="upper right")
            lab.xlabel("Average Z Position")
            lab.ylabel("AverageCharge")
            lab.title("K = "+str(K)+"|| E="+str(E))
            lab.grid()
            lab.show()
            
    except:
        print("Corrupt file.")
    
    


# In[38]:

def LayerPos(dumpFile,frames,UsedFrame,atomNumber,atomPlate,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averagePos=[]
        
        
        
        if plotBool==True:
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y'                , 'k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            
            for counter in range(len(a)):
                totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
                averagePos.append(num.sum(pos[2][:,layer[counter][0]])/totalData)
            #f=lambda x:a*x+b
            #params = curve_fit(f,range(len(a)),averagePos)
            print(0)
            
            lab.plot(range(len(a)),averagePos,"o")
            #handles, labels = ax.get_legend_handles_labels()
            #lgd=lab.legend(bbox_to_anchor=(1.5,1),loc="upper right")
            lab.ylabel("Average Z Position")
            lab.xlabel("LayerNumber")
            lab.title("K = "+str(K)+"|| E="+str(E))
            lab.xlim([-1,len(a)])
            lab.show()
            #return params[0]
            
    except:
        print("Corrupt file.")
    


# In[39]:

from scipy.optimize import curve_fit
def LayerCharge(dumpFile,frames,UsedFrame,atomNumber,atomPlate,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        
        
        
        if plotBool==True:
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y'                , 'k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            
            for counter in range(len(a)):
                totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
                averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            f=lambda x,a,b:a*x+b
            
            params = curve_fit(f, range(len(a)), avergaeChargeLayers)
            
            lab.plot(range(len(a)),averageChargeLayers,"o")
            lab.ylabel("Average Charge")
            lab.xlabel("LayerNumber")
            lab.title("K = "+str(K)+"|| E="+str(E))
            lab.xlim([-1,len(a)])
            lab.xticks(range(len(a)))
            lab.grid()
            lab.show()
            return params[0]
            
    except:
        print("Corrupt file.")
    
   


# In[ ]:

def DipoleStatFile(statFile):
    try:
        data=pan.DataFrame(pan.read_csv(statFile,sep="\t",header=1))
        p=num.sum(data.iloc[:,[9]][-10:])/10
        return p[0]
    except:
        print("Error in ::",statFile)
        return 99999
        
        
        
def SlopePE(alpha,atomNumber,units):
    if units=="AMU":
        return alpha*0.14818474*1.1126e-30*atomNumber
    elif units=="A^3":
        return alpha*1.1126e-30*atomNumber
    else:
        print("Error in units. Units must be \"AMU\"or \"A^3\" ")
 


# In[10]:

def SlopeQZ(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        aveZpos=[]
    
    
        for counter in range(len(a)):
            totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
            averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            aveZpos.append(num.sum(pos[2][UsedFrame:,layer[counter][0]])/totalData)
        
        n=num.arange(1,len(a)+1-8)
        if len(a)%2==0:
            n=n-num.ceil((len(a)+1-8)/2)  # shfting 1 2 3 4 5 6 to -3 -2 -1 1 2 3
            n[n>=0]=n[n>=0]+1
        else:
            n=n-num.ceil((len(a)-8)/2)
            
        
            
        fitFx=lambda x,a:a*x
        paramCharge=curve_fit(fitFx,n,averageChargeLayers[4:-4])
        paramZPos=curve_fit(fitFx,n,aveZpos[4:-4])
        
        averageChargeFitted=fitFx(n,paramCharge[0])
        averageZPosFitted=fitFx(n,paramZPos[0])
        
        
        return paramCharge[0]/paramZPos[0]
    
        
    except:
        print("Corrupt File")
        return 999999


# In[40]:

# values of k
k=[200,300,400,500]
E=[0.5,1,1.5,2,2.5,3]
frameUsed=50
atomNumber=768
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/24Layers111ZhouPt/"
plot=False


ke=[[kfile,Efile] for kfile in k for Efile in E]
dipoleMoment=[]
valuesK=[]
valuesE=[]
for fileTag in ke:
    
    #filename=("24LayersK_"+str(fileTag[0])+"E_"+str(fileTag[1])+".dump")
    #dipoleMoment.append(LayerFitDipole(pathFolder+filename,frames,atomNumber,atomPlate,frameUsed,fileTag[0],\
    #                                   fileTag[1]/float(10),plot)[1])
    
    
    filename=("24LayersK_"+str(fileTag[0])+"E_"+str(fileTag[1])+".stat")
    dipoleMoment.append(DipoleStatFile(pathFolder+filename))
    
    
    
    valuesK.append(fileTag[0])
    valuesE.append(fileTag[1]/float(10))

dipoleDict=OrderedDict([("E",valuesE),("K",valuesK),("Dipole",dipoleMoment)])
dipoleFrame=pan.DataFrame(dipoleDict)


# In[41]:

#dipoleFrame["DipoleCm"]=dipoleFrame["Dipole"]*1.6e-19*1e-10   #using dump

dipoleFrame["DipoleCm"]=dipoleFrame["Dipole"]/atomNumber   #using stat file

dipoleFrame


# In[679]:

dipoleFrame[dipoleFrame.E==0]


# In[42]:

from scipy import stats
newFrame=dipoleFrame[num.logical_and(dipoleFrame.Dipole!=99999,dipoleFrame.E<=0.3)]
slope=[]
intercept=[]
error=[]

actualforPt=[3.627,7.254,10.88,14.508,18.135,21.762]
for kval in k:
    entries=newFrame.K==kval
    s,i,p_val,r_val,std_err=stats.linregress(newFrame[entries].E,newFrame[entries].DipoleCm)
    slope.append(s)
    intercept.append(i)
    error.append(std_err)
    lab.plot(newFrame[entries].E,newFrame[entries].DipoleCm,'bo')
    lab.plot(newFrame[entries].E,num.array(actualforPt)*1e-30,"ro--")
    ee=num.linspace(0,max(newFrame.E),1000)
    lab.plot(ee,s*ee+i,"r")
    lab.title("K="+str(kval))
    lab.xlabel("E(V/A)")
    lab.ylabel("Pz(Cm)")
    lab.show()
    print(num.sum(num.array(actualforPt)*1e-30-newFrame[entries].DipoleCm))
    


# In[14]:

dataSloInt=OrderedDict([("K",k),("slope",slope),("intercept",intercept),("error",error)])


# In[15]:

dataFrameSIE=pan.DataFrame(dataSloInt)
print(dataFrameSIE)
print(dipoleFrame[dipoleFrame.E==0])


# In[12]:

#dataFrameSIE["Slope800"]=slope
#dataFrameSIE["intercept800"]=intercept
#dataFrameSIE["error800"]=error


# In[17]:

from scipy.interpolate import interp1d
lab.plot(dataFrameSIE.slope,dataFrameSIE.K,"o")
#lab.plot(dataFrameSIE.K,dataFrameSIE.Slope800,'^')
fitFx=interp1d(dataFrameSIE.slope,dataFrameSIE.K,kind="cubic")
#fitFx800=interp1d(dataFrameSIE.K,dataFrameSIE.Slope800,kind="cubic")
kk=num.linspace(min(dataFrameSIE.slope),max(dataFrameSIE.slope),1000)
lab.plot(kk,fitFx(kk),"r",label="600")
#lab.plot(kk,fitFx800(kk),"g",label='800')
lab.xlabel("slope")
lab.legend()
lab.ylabel("K")
lab.show()


# In[75]:

alphaAMU=44
alphaA3=2.58
#print("%f : K when alpha is in amu"%fitFx(alphaAMU*0.14818474*1.1126e-30))


# In[ ]:

Zhou2001_111_12Layers=326.85758949587773
Zhou2001_111_15Layers=327.8989168180896

Zhou2004_111_12Layers=330.1797905290682
Zhou2004_111_15Layers=333.9439100747316

Zhou2001_100_12Layers=265.8676218249607



Zhou2004_111_12Layers_fitFx=352
Zhou2004_111_12Layers_fitFxNscaled=347



# In[ ]:

from scipy.interpolate import interp1d
lab.plot(dataFrameSIE.K,dataFrameSIE.slope,"o")

fitFx1=interp1d(dataFrameSIE.K,dataFrameSIE.slope,kind="cubic")

kk=num.linspace(min(dataFrameSIE.K),max(dataFrameSIE.K),1000)
lab.plot(kk,fitFx1(kk),"r")
#lab.plot(kk,fitFx800(kk),"g",label='800')
lab.xlabel("K")
lab.legend()
lab.ylabel("slope")
lab.show()


# In[18]:



x = dataFrameSIE.K
y = dataFrameSIE.slope
yerr=dataFrameSIE.error

def fit_func(x, a,b):
    return a*x+b

params = curve_fit(fit_func, x, y)

[a,b] = params[0]

kk=num.linspace(min(dataFrameSIE.K)-100,max(dataFrameSIE.K)+200,1000)

lab.plot(dataFrameSIE.K,dataFrameSIE.slope,"ro")
lab.errorbar(x, y,yerr, fmt='r.')
lab.xlim([min(x)-200,max(x)+200])
lab.plot(kk,fit_func(kk,a,b))


# In[19]:

alphaA3=6.512
slope=alphaA3*1.1126e-30
def kval(slope,a,b):
    return (a/(slope-b))
print(kval(slope,a,b))


# In[ ]:

sum(abs(y-fit_func(x,a,b)))


# In[ ]:

b


# In[ ]:

slope


# In[ ]:

b


# In[472]:

# values of k
k=[200,300,400,500,600,700,800,900,1000]
E=[.5]
frameUsed=50
atomNumber=768#1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/24Layers111ZhouPt/"
plot=True


ke=[[kfile,Efile] for kfile in k for Efile in E]

for fileTag in ke:
    
    filename=("24LayersK_"+str(fileTag[0])+"E_"+str(fileTag[1])+".dump")
    ChargeVZPos(pathFolder+filename,frames,frameUsed,atomNumber,atomPlate,fileTag[0],fileTag[1]/float(10),plot)
    


# In[427]:

# values of k
k=[200,250,300,350,400,450,500,550]
E=[0.5,1,1.5,2,2.5,3]
frameUsed=50
atomNumber=1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/15Layers111Zhou2004/"
plot=True


ke=[[kfile,Efile] for kfile in k for Efile in E]

for fileTag in ke:
    
    filename=("PtSlab111Zhou2004Layers15K_"+str(fileTag[0])+"E_"+str(fileTag[1])+".dump")
    LayerCharge(pathFolder+filename,frames,frameUsed,atomNumber,atomPlate,fileTag[0],fileTag[1]/float(10),plot)
    


# In[42]:

alphaAMU*0.14818474*1.1126e-30


# In[66]:

b=num.arange(10)


# In[241]:

# values of k
k=[200,300,400,500,600,700,800,900,1000]
E=[.5]
frameUsed=50
atomNumber=768#1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/24Layers111ZhouPt/"
plot=True


ke=[[kfile,Efile] for kfile in k for Efile in E]

for fileTag in ke:
    
    filename=("24LayersK_"+str(fileTag[0])+"E_"+str(fileTag[1])+".dump")
    LayerPos(pathFolder+filename,frames,frameUsed,atomNumber,atomPlate,fileTag[0],fileTag[1]/float(10),plot)
    


# In[507]:

def LayerFitDipoleTest(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        print("dump")
        pos=dump["position"]
        charge=dump["chargeQV"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averageChargeLayers=[]
        aveZpos=[]
    
    
        for counter in range(len(a)):
            totalData=float(len(layer[counter][0]))*(frames-UsedFrame)
            averageChargeLayers.append(num.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            aveZpos.append(num.sum(pos[2][UsedFrame:,layer[counter][0]])/totalData)
        
        n=num.arange(1,len(a)+1-8)
        if len(a)%2==0:
            n=n-num.ceil((len(a)+1-8)/2)  # shfting 1 2 3 4 5 6 to -3 -2 -1 1 2 3
            n[n>=0]=n[n>=0]+1
        else:
            n=n-num.ceil((len(a)-8)/2)
            
        print(n)
            
        fitFx=lambda x,a:a*x
        paramCharge=curve_fit(fitFx,n,averageChargeLayers[4:-4])
        paramZPos=curve_fit(fitFx,n,aveZpos[4:-4])
        
        averageChargeFitted=fitFx(n,paramCharge[0])
        averageZPosFitted=fitFx(n,paramZPos[0])
        
        lab.plot(aveZpos[4:-4],averageChargeLayers[4:-4],"or")
        lab.plot(averageZPosFitted,averageChargeFitted,"og")
        print(num.sum(averageChargeFitted))
        
        dipolefitted=num.sum(averageChargeFitted*averageZPosFitted)
        diff=[]
        precharge=0
        prez=0
        for counter in range(len(a)-8):
            diff.append((averageChargeFitted[counter]-precharge)*(averageZPosFitted[counter]-prez))
            precharge=averageChargeFitted[counter]
            prez=averageZPosFitted[counter]
    
         
        if plotBool==True:
            lab.plot(range(1,len(a)),diff[1:],'o-')
            lab.xlabel("Layers")
            lab.ylabel("LayerDipole")
            lab.title("E = "+str(E)+" || K = "+str(K))
            lab.grid()
            lab.show()
        dipole=num.sum(diff[4:-4])/float(len(diff)-9)
        print(dipole,dipolefitted)
        #dipole=num.sum(diff[4:-4])/float(len(diff)-9)
        
        return dipole,dipolefitted
    
        
    except:
        print("Corrupt File")
        
        
# values of k
k=[200]
E=[.5]
frameUsed=50
atomNumber=768#1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/24Layers111ZhouPt/"
plot=False


ke=[[kfile,Efile] for kfile in k for Efile in E]
for fileTag in ke:
    
    filename=("24LayersK_"+str(fileTag[0])+"E_"+str(fileTag[1])+".dump")
    LayerFitDipoleTest(pathFolder+filename,frames,atomNumber,atomPlate,frameUsed,fileTag[0],fileTag[1]/float(10),plot)
    


# In[208]:

frameUsed=50
atomNumber=768#1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/24Layers111ZhouPt/24LayersK_200E_3.dump"
plot=True


    
    

dump1=DumpExtractor(pathFolder,frames,atomNumber,atomPlate)
x=dump1["position"][0]
y=dump1["position"][1]
z=dump1["position"][2]
c=dump1["chargeQV"][1]
#c=c/abs(c)
layer,a=Layers(z,atomNumber)

xx=x[99,layer[8][0]]
yy=y[99,layer[8][0]]
colors=c[99,layer[8][0]]


xx1=x[99,layer[7][0]]
yy1=y[99,layer[7][0]]
colors1=c[99,layer[7][0]]

xx2=x[99,layer[6][0]]
yy2=y[99,layer[6][0]]
colors2=c[99,layer[6][0]]

fig1=plt.figure(figsize=(8,8))
ax1=fig1.add_subplot(1,1,1)
plt.scatter(xx, yy, c=colors, s=600, cmap='bwr',linewidth=2,edgecolor="blue")
plt.scatter(xx1, yy1, c=colors1, s=600, cmap='bwr',linewidth=2,edgecolor="red")
plt.scatter(xx2, yy2, c=colors2, s=600, cmap='bwr',linewidth=2,edgecolor='green')

plt.colorbar()

plt.xlim([-11,11])
plt.ylim([-6,6])
plt.axes().set_aspect('equal', 'datalim')
plt.show()


# In[383]:

x=num.linspace(0,3.14,10)
y=x**2


# In[384]:

def fitfx(x,a,b,c,d):
    return a*num.sin(x)+b*num.cos(x)+c*num.sin(2*x)+d*num.cos(2*x)

param=curve_fit(fitfx,x,y)
param


# In[385]:

[a,b,c,d]=param[0]


# In[386]:

lab.plot(x,y,"o")
lab.plot(x,x**2)
lab.plot(x,fitfx(x,a,b,c,d),'--')


# In[387]:

num.random.normal(0,1,100)


# In[544]:

p=lambda E,alpha:alpha*E


# In[548]:

E=num.array([0.5,1,1.5,2,2.5,3])
alpha=7.254295035856001e-30


# In[549]:

p(E,alpha)


# In[408]:

n=num.arange(1,6+1)


# In[409]:

n


# In[410]:

n=n-num.ceil((6+1)/2)
n


# In[411]:

n[n>=0]=n[n>=0]+1


# In[412]:

n


# In[490]:

n


# In[491]:

n[2:-2]


# In[461]:

num.arange(10)


# In[466]:

for i in range(0,10):
    print(i)


# In[646]:

def DipoleStatFileTest(statFile):
    try:
        data=pan.DataFrame(pan.read_csv(statFile,sep="\t",header=1))
        p=num.sum(data.iloc[:,[9]][-10:])/10
        print(data.iloc[:,[9]][-10:])
        print(p)
        return p[0]
    except:
        print("Error in ::",statFile)
        return 99999
        

k=[200]
E=[0.5]
frameUsed=99
atomNumber=768#1080 #864
atomPlate=0
frames=100
pathFolder="../Susceptiblity_K_determine/12Layers111Zhou2004Pt/"
plot=False


ke=[[kfile,Efile] for kfile in k for Efile in E]
dipoleMoment=[]
valuesK=[]
valuesE=[]
for fileTag in ke:
    
    
    
    
    filename=("PtSlab111Zhou2004Layers12K_"+str(fileTag[0])+"E_"+str(fileTag[1])+".stat")
    dipoleMoment.append(DipoleStatFileTest(pathFolder+filename))
    
    
    
    valuesK.append(fileTag[0])
    valuesE.append(fileTag[1]/float(10))

dipoleDict=OrderedDict([("E",valuesE),("K",valuesK),("Dipole",dipoleMoment)])
dipoleFrame=pan.DataFrame(dipoleDict)


# In[647]:

dipoleFrame


# In[576]:

dipoleFrame


# In[ ]:



