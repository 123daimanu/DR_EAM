"""Generates the heat map for different data containing different order parameters"""



from pylab import *
class HeatMap(object):
   
    
    def __init__(self, folder):
        self.folder = folder
        self.freqThreshold = 300
        self.deltaZ = 3
        self.initial = 0
        self.fileOut = self.folder + "heatMap.jpg"
        self.showPlot = False
        self.subsystem =""
        self.extension = "pspect"
        self.colormaxminBool = False
        self.colormaxmin = [0 , 0]
        self.deduct = 0
        self.deductFlag = False
        self.YAxisPoints = 20
        self.YInitial = 0
        self.xlabel = "X"
        self.ylabel = "Y"
        self.ns1=1
        self.ns2=1    
        self.mapping = "none"
        
    def set_mapping(self,mapping):
        self.mapping = mapping

    def set_n1Start(self,ns1):
        self.ns1= ns1

    def set_n2Start(self,ns2):
        self.ns2= ns2
    def set_YAxisPoints(self,YAxisPoints):
        self.YAxisPoints = YAxisPoints
    def set_YInitial(self,YInitial):
        self.YInitial = YInitial
    def set_subsystem(self,subSys):
        self.subsystem = subSys
        
    def set_colormaxmin(self, *arg):
        import sys
        self.colormaxminBool = True
        if (len(list(arg)) != 2) and (len(list(arg)) !=4) :
            print("Set max and min")
            sys.exit()

        self.colormaxmin = list(arg)
        
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
    def set_initial(self, initial):
        self.initial = initial
        
    def set_deltaZ(self, deltaZ):
        self.deltaZ = deltaZ
        
    def set_freqThreshold(self, freqThreshold):
        self.freqThreshold = freqThreshold

    def set_showPlot(self):
        self.showPlot = True

    def set_extension(self, extension):
    	self.extension = extension

    def set_xlabel(self, xlabel):
        self.xlabel = xlabel


    def set_ylabel(self, ylabel):
        self.ylabel = ylabel	
    
    def set_deduction(self, deduction):
        self.deduct = deduction
        self.deductFlag = True
    
    def getZVal(self,inital, end,start,step=1):
        for index in range(start,end,step):
            yield initial+index * self.deltaZ
            
    def genFiles( self, number_start,number_end, system ):
        for index in range(number_start,number_end + 1):
            filename = system +"_%d%s.%s"%(index, self.subsystem,self.extension)
            yield filename
    
    def getDataFrame(self, list_names):
        import pandas as pd
        freqThreshold = self.freqThreshold
        folder = self.folder
        for fileName in list_names:
            df1 = pd.read_csv(folder+fileName,delimiter='\t',names=["f","I"])
            #df1.I = df1.I/sum(df1.I)
            
            if self.deductFlag :
                df1.f = self.deduct - df1.f
                
            df1.sort_values("f", axis = 0, ascending =True, inplace = True)
            df1.fillna(0, inplace = True)
            df1 = df1[df1.f<freqThreshold]
            self.freqList = list(df1.f)
            
            yield df1
            
    def getHeatMap(self, dfList):
        import pandas as pd
        columns = len(dfList)
        rows = len(dfList[0].iloc[:,0])
    
        from numpy import zeros
        heatMapMat = zeros(rows*columns).reshape(rows,columns)
        #positionMat = [(x,y) for x in range(1,rows) for y in range(columns)]
        positionMat = [(x,y) for x in range(rows) for y in range(columns)]
        for matPos in positionMat:
            heatMapMat[matPos[0],matPos[1]] = dfList[matPos[1]].I[matPos[0]]
        return heatMapMat
    
    def HeatMapMatrix(self):
        self.mat = []
        startNumber = [self.ns1, self.ns2]
        for index in range(len(self.system)):
            fileList=list(self.genFiles(startNumber[index],self.number[index],self.system[index]))
            dfList = list(self.getDataFrame(fileList))
            self.mat.append(self.getHeatMap(dfList))
            
    
        
    def diffMatMatrix(self):
        mat1, mat2 = self.mat[0], self.mat[1]
        self.diffMat = [mat1 - mat2]
        
    
    def heatMapPlot(self):
   
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        from matplotlib import rc, rcParams
        rc('text', usetex=True)
        rc('axes',linewidth=1.5)
        rc('font',weight=2)
        rcParams['text.latex.preamble']=[r'\usepackage{sfmath}\boldmath']
    #---------------------------------------
    #subplot adjust
        left  =0.1# the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.1  # the amount of width reserved for blank space between subplots,
               # expressed as a fraction of the average axis width
        hspace = 0.2  # the amount of height reserved for white space between subplots,
               # expressed as a fraction of the average axis height
    
        n1 = self.number[0]
        n2 = self.number[1]
        n1s = self.ns1
        n2s = self.ns2
        freqThreshold = self.freqThreshold
        freqList  = self.freqList
        deltay = int(freqThreshold/20)
        metalInital=0
        
        #zVal1=list(self.getZVal(0,n1s,n1))
        #zVal2=list(self.getZVal(self.initial,n2s,n2))
        #print(zVal1,zVal2)
        mat1 = self.mat[0]
        mat2 = self.mat[1]
        

        if(self.colormaxminBool):
            vmax = self.colormaxmin[1]
            vmin = self.colormaxmin[0]
        else:
            vmax = mat2.max()
            vmin = mat2.min()
        
        xdim = 800
        deltax1 = int(xdim/(n1-n1s+1))
        deltax2 = int(xdim/(n2-n2s+1))
        #axis1= (n1-n1s+2) * deltax1
        #axis2= (n2-n2s+2) * deltax2
        axis1 = xdim
        axis2 = xdim
        

        fig, (ax1, ax2) = plt.subplots(1, 2, sharey= True)
        fig.set_size_inches(10,10)
        
        im1 = ax1.imshow(mat1,aspect="auto",interpolation=self.mapping,extent=[0, axis1, 0, 1000],
               vmax=vmax, vmin=vmin, cmap= "Blues")
        

        xtick1 = [x for x in range(0,axis1+deltax1,deltax1)]
        xtick1Label = [r'\textbf{%s}'%str(-3*(xtick))for xtick in range(n1-n1s+1,0,-1)]
        xtick1Label.append("") 
        

        xtick2=[x for x in range(0,axis2+deltax2,deltax2)]
        xtick2Label=[r'\textbf{%s}'%str(xtick*3)for xtick in range(0,n2+1,1)]

        ax1.set_xticks(xtick1)
        ax1.set_xticklabels(xtick1Label,fontsize=12)
       
        ax1.set_yticks(range(0,1000,50))
        ax1.set_yticklabels([r'\textbf{%s}'%str(ytick) for ytick in range(freqThreshold,0,-deltay)], fontsize=12)
        ax1.set_ylabel(r'\textbf{%s}'%self.ylabel, fontsize = 12)

        im2 = ax2.imshow(mat2,aspect="auto",interpolation=self.mapping,extent=[0, axis2, 0, 1000],
               vmax=vmax, vmin=vmin,cmap="Blues")
        

        ax2.set_xticks(xtick2)
        ax2.set_xticklabels(xtick2Label, fontsize=12)
        
        ax2.set_aspect('auto')
        plt.title(r'\textbf{%s}'%self.xlabel, y=-0.1, x=-0.1, fontsize=12)
        from numpy import linspace
        colorticks = linspace(vmin,vmax,10,endpoint=True)
        colorbar_ax=fig.add_axes([0.915,0.11,0.04,0.77])
        #fig.colorbar(im2,cax=colorbar_ax)
        cb = plt.colorbar(im2,cax=colorbar_ax,ticks=colorticks)
        ctick = ["{:1.1e}".format(i) for i in colorticks]
        cb.ax.set_yticklabels([r'\textbf{%s}'%str(xtick) for xtick in ctick], fontsize=12)
        plt.subplots_adjust(wspace = 0, hspace = 0)
       # plt.title(self.fileOut.split("/")[-1].split(".")[0])
        plt.savefig(self.fileOut, bbox_inches="tight")
        
        if self.showPlot:
            plt.show()
    
    
    def heatMapPlot2(self):
   
    
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        from matplotlib import rc, rcParams
        rc('text', usetex=True)
        rc('axes',linewidth=1.5)
        rc('font',weight=2)
        rcParams['text.latex.preamble']=[r'\usepackage{sfmath}\boldmath']
    #---------------------------------------
    #subplot adjust
        left  =0.1# the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.1  # the amount of width reserved for blank space between subplots,
               # expressed as a fraction of the average axis width
        hspace = 0.2  # the amount of height reserved for white space between subplots,
               # expressed as a fraction of the average axis height
    
        n1 = self.number[0]
        n2 = self.number[1]
        n1s = self.ns1
        n2s = self.ns2
        freqThreshold = self.freqThreshold
        freqList  = self.freqList
        deltay = int(freqThreshold/20)
        metalInital=0
        
        #zVal1=list(self.getZVal(0,n1s,n1))
        #zVal2=list(self.getZVal(self.initial,n2s,n2))
        #print(zVal1,zVal2)
        mat1 = self.mat[0]
        mat2 = self.mat[1]
        print("%e,%e"%(mat1.min(),mat1.max()))        

        print("%e,%e"%(mat2.min(),mat2.max()))        

        if(self.colormaxminBool):
            vmax1 = self.colormaxmin[1]
            vmin1 = self.colormaxmin[0]
            vmax2 = self.colormaxmin[3]
            vmin2 = self.colormaxmin[2]
        else:
            vmax2 = mat2.max()
            vmin2 = mat2.min()
            vmax1 = mat1.max()
            vmin1 = mat1.min()
       # vmax2 = mat2.max()
       # vmin2 = mat2.min()
       # vmax1 = mat1.max()
       # vmin1 = mat1.min()
        
        xdim = 800
        deltax1 = int(xdim/(n1-n1s+1))
        deltax2 = int(xdim/(n2-n2s+1))
        axis1 = xdim
        axis2 = xdim
        

        fig, (ax1, ax2) = plt.subplots(1, 2, sharey =True)
        fig.set_size_inches(12,12)
        
        im1 = ax1.imshow(mat1,aspect="auto",interpolation=self.mapping,extent=[0, axis1, 0, 1000],
               vmax=vmax1, vmin=vmin1, cmap= "Reds")
        

        xtick1 = [x for x in range(0,axis1+deltax1,deltax1)]
        xtick1Label = [r'\textbf{%s}'%str(-3*(xtick))for xtick in range(n1-n1s+1,0,-1)]
        xtick1Label.append("") 
        

        xtick2=[x for x in range(0,axis2+deltax2,deltax2)]
        xtick2Label=[r'\textbf{%s}'%str(xtick*3)for xtick in range(0,n2+1,1)]

        ax1.set_xticks(xtick1)
        ax1.set_xticklabels(xtick1Label,fontsize=14)
       
        ax1.set_yticks(range(0,1000,50))
        ax1.set_yticklabels([r'\textbf{%s}'%str(ytick) for ytick in range(freqThreshold,0,-deltay)], fontsize=14)
        ax1.set_ylabel(r'\textbf{%s}'%self.ylabel, fontsize = 14)

        im2 = ax2.imshow(mat2,aspect="auto",interpolation=self.mapping,extent=[0, axis2, 0, 1000],
               vmax=vmax2, vmin=vmin2,cmap="Blues")
        

        ax2.set_xticks(xtick2)
        ax2.set_xticklabels(xtick2Label, fontsize=14)
        
        ax2.set_aspect('auto')
        plt.title(r'\textbf{%s}'%self.xlabel, y=-0.1, x=-0.1, fontsize=14)


        from numpy import linspace

        colorticks1 = linspace(vmin1,vmax1,10,endpoint=True)
        colorbar_ax1=fig.add_axes([0.025,0.11,0.04,0.770])
        cb1 = plt.colorbar(im1,cax=colorbar_ax1,ticks=colorticks1)
        ctick1 = ["{:1.1e}".format(i) for i in colorticks1]
        cb1.ax.yaxis.set_label_position("left")
        cb1.ax.yaxis.tick_left()
        cb1.ax.set_yticklabels([r'\textbf{%s}'%str(xtick) for xtick in ctick1], fontsize=14)



        colorticks2 = linspace(vmin2,vmax2,10,endpoint=True)
        colorbar_ax2=fig.add_axes([0.915,0.11,0.04,0.770])
        cb2 = plt.colorbar(im2,cax=colorbar_ax2,ticks=colorticks2)
        ctick2 = ["{:1.1e}".format(i) for i in colorticks2]
        cb2.ax.set_yticklabels([r'\textbf{%s}'%str(xtick) for xtick in ctick2], fontsize=14)



        plt.subplots_adjust(wspace = 0, hspace = 0)
       # plt.title(self.fileOut.split("/")[-1].split(".")[0])
        plt.savefig(self.fileOut, bbox_inches="tight")
        
        if self.showPlot:
            plt.show()
        return 0
    


    def heatMapPlot1(self):
   
    
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        from matplotlib.ticker import FormatStrFormatter
        from matplotlib import rc, rcParams
        rc('text', usetex=True)
        rc('axes',linewidth=1.5)
        rc('font',weight=2)
        rcParams['text.latex.preamble']=[r'\usepackage{sfmath}\boldmath']
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
        fig, ax1 = plt.subplots(1, 1)
    #fig.subplots_adjust(left=left,right=right,bottom=bottom,top=top\
    #                  ,wspace=wspace,hspace=hspace)
    
        n1 = self.number[0]
        dfList = self.freqList
        freqThreshold = self.freqThreshold
        xdim = 800
        n1=self.number[0]
        n1s= self.ns1
        deltaY = int(1000/self.YAxisPoints)
        
        deltax1 = int(xdim/(n1-n1s+1))
        axis1 = xdim
    
        
        fig.set_size_inches(6,6)

        mat2 = self.mat[0]

        if(self.colormaxminBool):
            vmax = self.colormaxmin[1]
            vmin = self.colormaxmin[0]
        else:
            vmax = mat2.max()
            vmin = mat2.min()
        
        
        im1 = ax1.imshow(mat2,interpolation=self.mapping,extent=[0, axis1, 0, 1000],
               vmax= vmax, vmin= vmin, cmap = 'Blues')
        

        xtick2=[x for x in range(0,axis1+deltax1,deltax1)]
        xtick2Label=[r'\textbf{%s}'%str(xtick*3)for xtick in range(0,n1+1,1)]
        ax1.set_xticks(xtick2)
        #ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax1.set_xticklabels(xtick2Label,fontsize=12)
        
        
        increment = int(len(dfList)/self.YAxisPoints)
        yTicks = list(range(0,1000,deltaY))
        yy = [var for var in yTicks]
        ll=["%2.1f"%(dfList[pos]) for pos in range(0, len(dfList), increment)]
        ax1.set_yticks(yTicks)
        ax1.set_yticklabels([r'\textbf{%2.1f}'%(dfList[pos]) for pos in range(0, len(dfList), increment)],fontsize=12)

        ax1.set_xlabel(r'\textbf{%s}'%self.xlabel, fontsize=13)
        ax1.set_ylabel(r'\textbf{%s}'%self.ylabel, fontsize=13)
        from numpy import linspace
        colorticks = linspace(vmin,vmax,10,endpoint=True)
        colorbar_ax=fig.add_axes([0.915,0.11,0.04,0.770])
        #fig.colorbar(im2,cax=colorbar_ax)
        cb = plt.colorbar(im1,cax=colorbar_ax,ticks=colorticks)
        ctick = ["{:1.1e}".format(i) for i in colorticks]
        cb.ax.set_yticklabels([r'\textbf{%s}'%str(xtick) for xtick in ctick],fontsize=12)
        plt.subplots_adjust(wspace = 0, hspace = 0)
       # plt.title(self.fileOut.split("/")[-1].split(".")[0])
        plt.savefig(self.fileOut, bbox_inches="tight")

        
        
        if self.showPlot:
            plt.show()
        
    
 

    def heatMapDifferencePlot(self):
   
        import numpy as np
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        from matplotlib.ticker import FormatStrFormatter
        from matplotlib import rc, rcParams
        rc('text', usetex=True)
        rc('axes',linewidth=1.5)
        rc('font',weight=2)
        rcParams['text.latex.preamble']=[r'\usepackage{sfmath}\boldmath']
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
        fig, ax1 = plt.subplots(1, 1)
    #fig.subplots_adjust(left=left,right=right,bottom=bottom,top=top\
    #                  ,wspace=wspace,hspace=hspace)
    
        n1 = self.number[0]
        dfList = self.freqList
        freqThreshold = self.freqThreshold
        xdim = 800
        n1=self.number[0]
        n1s= self.ns1
        deltaY = int(1000/self.YAxisPoints)
        
        deltax1 = int(xdim/(n1-n1s+1))
        axis1 = xdim
    
        
        fig.set_size_inches(6,6)

        mat2 = self.diffMat[0]
        

        if(self.colormaxminBool):
            vmax = self.colormaxmin[1]
            vmin = self.colormaxmin[0]
        else:
            vmax = mat2.max()
            vmin = mat2.min()
        
        
        im1 = ax1.imshow(mat2,interpolation=self.mapping,extent=[0, axis1, 0, 1000],
               vmax= vmax, vmin= vmin, cmap = 'coolwarm')
        

        xtick2=[x for x in range(0,axis1+deltax1,deltax1)]
        xtick2Label=[r'\textbf{%s}'%str(xtick*3)for xtick in range(0,n1+1,1)]
        ax1.set_xticks(xtick2)
        #ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax1.set_xticklabels(xtick2Label,fontsize=12)
        
        
        increment = int(len(dfList)/self.YAxisPoints)
        yTicks = list(range(0,1000,deltaY))
        yy = [var for var in yTicks]
        ll=["%2.1f"%(dfList[pos]) for pos in range(0, len(dfList), increment)]
        ax1.set_yticks(yTicks)
        ax1.set_yticklabels([r'\textbf{%2.1f}'%(dfList[pos]) for pos in range(0, len(dfList), increment)],fontsize=12)

        ax1.set_xlabel(r'\textbf{%s}'%self.xlabel, fontsize=13)
        ax1.set_ylabel(r'\textbf{%s}'%self.ylabel, fontsize=13)
        from numpy import linspace
        colorticks = linspace(vmin,vmax,10,endpoint=True)
        colorbar_ax=fig.add_axes([0.915,0.11,0.04,0.770])
        #fig.colorbar(im2,cax=colorbar_ax)
        cb = plt.colorbar(im1,cax=colorbar_ax,ticks=colorticks)
        ctick = ["{:1.1e}".format(i) for i in colorticks]
        cb.ax.set_yticklabels([r'\textbf{%s}'%str(xtick) for xtick in ctick],fontsize=12)
        plt.subplots_adjust(wspace = 0, hspace = 0)
       # plt.title(self.fileOut.split("/")[-1].split(".")[0])
        plt.savefig(self.fileOut, bbox_inches="tight")

        
        
        if self.showPlot:
            plt.show()
        
    
 



# In[38]:





# In[42]:









