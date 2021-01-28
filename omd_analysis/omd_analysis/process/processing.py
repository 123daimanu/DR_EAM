"""
contains function that does data processing of the extracted data


"""

from scipy.optimize import curve_fit





def Layers(ZPosition,atomNumber):
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
    a=np.sort(list(set(ZPosition[0,0:atomNumber-1])))
    layer=[]
    for var in a:
        layer.append(np.where(ZPosition[0]==var))
    
    return [layer,a]



def LayerDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    """Function that determines average dipoles of layers excluding 4 surface layers
    dipole=LayerDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool)
    
    
    Input:
   ========
           dumpFile: Dump file to be analysed
           
           frames: No of frames in dumpfile
           
           atomNumber: No of atom number in dump file
           
           atomPlate: No of atoms in plate
           
           UsedFrame: The begin of frame that is used for averaging
           
           K: Value of K in simulation
           
           E: Value of Efield in simulation
           
           plotBool: true or false to output graph
           
           
   Output:
  =========
          
          float dipole; Average dipole of layers
    
    """
    
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
            averageChargeLayers.append(np.sum(charge[0][UsedFrame:,layer[counter][0]])/totalData)
            aveZpos.append(np.sum(pos[2][UsedFrame:,layer[counter][0]])/totalData)
        
        
        
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
        dipole=np.sum(diff[4:-4])/float(len(diff)-9)
        #dipole=np.sum(diff[4:-4])/float(len(diff)-9)
        
        return dipole
    
        
    except:
        print("Corrupt File")
        return 999999
    
    
    



def LayerFitDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool):
    """"
    
    Function that calculates Layers dipole using linear fit to charge and z position to ensure charge neutrality in bulk
    
    [dipole,dipolefitted]=LayerFitDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame,K,E,plotBool)
    
    
     Input:
   ========
           dumpFile: Dump file to be analysed
           
           frames: No of frames in dumpfile
           
           atomNumber: No of atom number in dump file
           
           atomPlate: No of atoms in plate
           
           UsedFrame: The begin of frame that is used for averaging
           
           K: Value of K in simulation
           
           E: Value of Efield in simulation
           
           plotBool: true or false to output graph
           
           
   Output:
  =========
          
          list [dipole,dipolefitted]; dipole is raw dipole of layers, dipolefitted is dipole after doing linear fit of charge with z
    
    """
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
        
        n=np.arange(1,len(a)+1-8)
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
        
        
        dipolefitted=np.sum(averageChargeFitted*averageZPosFitted)/num.size(averageChargeFitted)
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
        dipole=np.sum(diff[5:-4])/float(len(diff)-9)
        
        #dipole=np.sum(diff[4:-4])/float(len(diff)-9)
        print(dipole,dipolefitted)
        return [dipole,dipolefitted]
    
        
    except:
        print("Corrupt File")
        return 999999



def SlabDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame):
    
    """"
    
    Function that calculates dipole of bulk using p_z=\sum_{i}q_i z_i
    
    dipole=SlabDipole(dumpFile,frames,atomNumber,atomPlate,UsedFrame)
    
    
     Input:
   ========
           dumpFile: Dump file to be analysed
           
           frames: No of frames in dumpfile
           
           atomNumber: No of atom number in dump file
           
           atomPlate: No of atoms in plate
           
           UsedFrame: The begin of frame that is used for averaging
           
     
                  
   Output:
  =========
          
          float dipole; dipole is the total bulk dipole of system
    
    """
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        charge=dump["chargeQV"]
        z=pos[2][UsedFrame,:]
        c=charge[0][UsedFrame,:]
        dipole=np.sum(num.multiply(z,c))
        return dipole
    
    except:
        print("Corrupt File")
        return 999999
    



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
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y', 'k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
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
    
    



def LayerPos(dumpFile,frames,UsedFrame,atomNumber,atomPlate,K,E,plotBool):
    try:
        dump=DumpExtractor(dumpFile,frames,atomNumber,atomPlate)
        pos=dump["position"]
        layersInfo=Layers(pos[2],atomNumber)
        layer=layersInfo[0]
        a=layersInfo[1]
        averagePos=[]
        
        
        
        if plotBool==True:
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y','k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
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
            colors=['b','b--', 'g--','g','r--','r','c--','c','m--','m','y--','y', 'k--','k','b-.','g-.','r-.','c-.','m-.','y-.','k-.']
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
    

    
def DipoleStatFile(statFile):
    try:
        data=pan.DataFrame(pan.read_csv(statFile,sep="\t",header=1))
        p=np.sum(data.iloc[:,[9]][-10:])/10
        return p[0]
    except:
        print("Error in ::",statFile)
        return 99999
        
        
        
def SlopePE(alpha,atomNumber,units):
    """"
    Converts the alpha to units of C m^2 V^-1
    """
    if units=="AU":
        return alpha*1.648773e-41*atomNumber
    elif units=="A^3":
        return alpha*1.648773e-41*atomNumber/0.14818474
    else:
        print("Error in units. Units must be \"AU\"or \"A^3\" ")

        
        
        
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
        
        n=np.arange(1,len(a)+1-8)
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

    
    
def CurvatureSlope(InputArray):
    """
    [KvrsSlope]=CurvatureSlope(InputArray)
    
    Returns the array where of each row is [k,slope(related to alpha)]
    
    
    Input:
   ========
   List: List of List [curvature,efield,layerdipole]
   Output:
  =========
  [KvrSlope]: List of list [k(curvature),slope(related to alpha)] in units of Ang^3
    
    """
    
    outPut=[]
    setofCurvature=list(set(InputArray[:,0]))
    for var in setofCurvature:
        arrayK=InputArray[InputArray[:,0]==var]
        try:
            const1=np.polyfit(arrayK[:,1],arrayK[:,2],1)
            lab.plot(arrayK[:,1],arrayK[:,2])
            slope=const1[0]/1.1125e-20
            outPut.append([var,slope])
        except:
            continue;
    return outPut

