from function import HeatMap 
def getAllPlots(subsystemAtom): 
    print("+++++++ PLOT GENERATING FOR %s and %s +++++++"%(subsystemAtom[0],subsystemAtom[1])) 
    subsystem, atom = subsystemAtom[0],subsystemAtom[1] 
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/" 
    fileOut = "%s_%s_Vcorr_Split_Noisy_Bilinear.eps"%(subsystem,atom) 
    tailSubsystem = "_Vcorr" 
    system2 = "%s_Dynamics_TimeAdjusted_%s_Atomic"%(subsystem,atom)
    system1 = "%s_Dynamics_TimeAdjusted_Au_Atomic"%(subsystem)
    n1=6
    n2=4
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n1,n2)
    heatMap.set_freqThreshold(200)
    heatMap.set_xlabel("Z")
    heatMap.set_ylabel("frequency ")
    heatMap.set_system(system1, system2)
    heatMap.set_subsystem(tailSubsystem)
    heatMap.set_deltaZ(3)
    heatMap.set_n1Start(3)
    heatMap.set_mapping("bilinear")
    heatMap.set_colormaxmin(2.25e-5,1.77e-2,1e-4,6.6e-3)
    #heatMap.set_showPlot()
    heatMap.set_fileOut(fileOut)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot2()


    
    return subsystem
    


def main():    
    subsystemList=["MNWN"]
    atomicList = ["CM"]
    totalSys = [[syst,atom] for syst in subsystemList for atom in atomicList]
    list(map(getAllPlots,totalSys))


if __name__ == "__main__":
    main()
