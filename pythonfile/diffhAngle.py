from function import HeatMap
def getAllPlots(subsystemAtom1,subsystemAtom2):
    print("+++++++ PLOT GENERATING FOR %s +++++++"%subsystemAtom1)
    subsystem1 = subsystemAtom1
    subsystem2 = subsystemAtom2
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    #for left and right system
    #fileOut = "%s_%s_HAngle.eps"%(subsystem,side)
    extensionName = "HHAngle"
    ylabelText = "HH"
    fileOut = "%s_%s_Diff.eps"%(subsystem1,extensionName)
    
    tailSubsystem = "" 
    system1 = "%s_Dynamics_TimeAdjusted"%(subsystem1)
    system2 = "%s_Dynamics_TimeAdjusted"%(subsystem2)
    n2=4
    n1=4
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n1,n2)
    heatMap.set_extension(extensionName)
    heatMap.set_initial(0)
    heatMap.set_subsystem("_Single")
    heatMap.set_system(system1,system2)
    heatMap.set_deltaZ(3)
    ref = 0
    dev = 2e-2
    heatMap.set_mapping("bilinear")
    heatMap.set_xlabel("Z")
    heatMap.set_ylabel("$S_1(\\theta_{%s})$"%(ylabelText))
    #heatMap.set_colormaxmin(4.3e-3,5.8e-3)
    heatMap.set_colormaxmin(ref-dev,ref+dev)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(1)
    heatMap.HeatMapMatrix()
    heatMap.diffMatMatrix()
    heatMap.heatMapDifferencePlot()

    


def main():    
    subsystemList1=["MNWN","MNWN_TIP4P", "MNWF"]
    subsystemList2=["MFWN", "MFWN_TIP4P", "MFWF"]
    list(map(getAllPlots,subsystemList1,subsystemList2))


if __name__ == "__main__":
    main()
