from function import HeatMap
def getAllPlots(subsystemAtom):
    print("+++++++ PLOT GENERATING FOR %s and %s +++++++"%(subsystemAtom[0],subsystemAtom[1]))
    subsystem, atom = subsystemAtom[0],subsystemAtom[1]
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    fileOut = "%s_%s.eps"%(subsystem,atom)
    tailSubsystem = "_Vcorr_smooth" 
    system2 = "%s_Dynamics_TimeAdjusted_%s_Atomic"%(subsystem,atom)
    system1 = "%s_Dynamics_TimeAdjusted_Au_Atomic"%(subsystem)
    n1=6
    n2=6
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n1,n2)
    heatMap.set_system(system1, system2)
    heatMap.set_subsystem(tailSubsystem)
    heatMap.set_mapping('bilinear')
#    heatMap.set_colormaxmin(0.0005,0.001,0.0005,0.001)
    heatMap.set_deltaZ(3)
    heatMap.set_fileOut(fileOut)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot2()


    
    return subsystem
    


def main():    
    subsystemList=["MNWN","MFWN","MNWN_TIP4P", "MFWN_TIP4P", "MNWF", "MFWF"]
    atomicList = ["H","O","CM"]
    totalSys = [[syst,atom] for syst in subsystemList for atom in atomicList]
    list(map(getAllPlots,totalSys))


if __name__ == "__main__":
    main()
