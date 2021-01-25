#!/usr/bin/env python
# coding: utf-8

# In[37]:


class HeatMap(object):
   
    
    def __init__(self, folder):
        self.folder = folder
        self.freqThreshold = 300
        self.deltaZ = 3
        self.initial = 0
        self.fileOut = self.folder + "heatMap.jpg"
        
    def set_subsystem(self,subSys):
        self.subsystem = subSys
        
    def set_fileOut(self, fileOut):
        self.fileOut = self.folder + fileOut
        
    def set_system(self,*args):
        self.system = []
        for system in args:
            self.system.append(system)
            
    def set_numbers(self, *args):
        self.number = []
        for number in args:
            self.number.append(number)
    def set_inital(self, initial):
        self.initial = initial
        
    def set_deltaZ(self, deltaZ):
        self.deltaZ = deltaZ
        
    def set_freqThreshold(self, freqThreshold):
        self.freqThreshold = freqThreshold
        
    def getZVal(self, end,start):
        for index in range(start,end):
            yield self.initial + index * self.deltaZ
            
    def genFiles( self, number, system ):
        for index in range(1,number + 1):
            yield system +"_%d_%s.pspect"%(index, self.subsystem)
    
    def getDataFrame(self, list_names):
        import pandas as pd
        freqThreshold = self.freqThreshold
        folder = self.folder
        for file in list_names:
            df1 = pd.read_csv(folder+file,delimiter='\t',names=["f","I","smooth"])
            df1.I = df1.I/sum(df1.I)
            df1.smooth = df1.smooth/sum(df1.smooth)
            df1.fillna(0, inplace = True)
            df1 = df1[df1.f<freqThreshold]
            yield df1
            
    def getHeatMap(self, dfList):
        import pandas as pd
        columns = len(dfList)
        rows = len(dfList[0].iloc[:,0])
    
        from numpy import zeros
        heatMapMat = zeros(rows*columns).reshape(rows,columns)
        positionMat = [(x,y) for x in range(rows) for y in range(columns)]
        for matPos in positionMat:
            heatMapMat[matPos[0],matPos[1]] = dfList[matPos[1]].smooth[matPos[0]]
        return heatMapMat
    
    def HeatMapMatrix(self):
        self.mat = []
        for index in range(len(self.system)):
            fileList=list(self.genFiles(self.number[index],self.system[index]))
            dfList = list(self.getDataFrame(fileList))
            self.mat.append(self.getHeatMap(dfList))
            
    
        
    
    
    def heatMapPlot(self):
   
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
    
    #---------------------------------------
    #subplot adjust
        left  =0.1# the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.2  # the amount of width reserved for blank space between subplots,
               # expressed as a fraction of the average axis width
        hspace = 0.2  # the amount of height reserved for white space between subplots,
               # expressed as a fraction of the average axis height
        fig, (ax1, ax2) = plt.subplots(1, 2, sharey= True)
    #fig.subplots_adjust(left=left,right=right,bottom=bottom,top=top\
    #                  ,wspace=wspace,hspace=hspace)
    
        n1 = self.number[0]
        n2 = self.number[1]
        freqThreshold = self.freqThreshold
        deltax = int(900/sum(self.number))
        deltay = int(freqThreshold/20)
    
        
        fig.set_size_inches(6,6)
        zVal1=list(self.getZVal(n1, 0))
        zVal2=list(self.getZVal(n2,n1))
        axis1= n1 * deltax
        axis2= n2 * deltax
        mat1 = self.mat[0]
        mat2 = self.mat[1]
        
        
        im1 = ax1.imshow(mat1,interpolation='bilinear',extent=[0, axis1, 0, 1000],
               vmax=mat2.max(), vmin=mat2.min(),cmap="Blues")
        ax1.set_xticks(range(0,axis1,deltax))
        ax1.set_xticklabels(list(range(0,n1*3,3)))
        ax1.set_yticks(range(0,1000,50))
        ax1.set_yticklabels(range(freqThreshold,0,-deltay))


        im2 = ax2.imshow(mat2,interpolation='bilinear',extent=[0, axis2, 0, 1000],
               vmax=mat2.max(), vmin=mat2.min(),cmap="Blues")
        ax2.set_xticks(range(0,axis2,2*deltax))
        ax2.set_xticklabels(range(18,18+n2*3,3*2))
        ax2.set_aspect('auto')
        colorbar_ax=fig.add_axes([0.95,0.1,0.05,0.8])
        fig.colorbar(im2,cax=colorbar_ax)
        plt.subplots_adjust(wspace = 0, hspace = 0)
        plt.title(self.fileOut.split("/")[-1].split(".")[0])
        plt.savefig(self.fileOut, bbox_inches="tight")
        plt.show()
    
    
        
    
    
    


# In[38]:





# In[42]:









