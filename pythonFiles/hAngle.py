from function import HeatMap
def getAllPlots(subsystemAtom):
    print("+++++++ PLOT GENERATING FOR %s +++++++"%subsystemAtom)
    subsystem = subsystemAtom
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    #for left and right system
    #fileOut = "%s_%s_HAngle.eps"%(subsystem,side)
    extensionName = "HAngle"
    ylabelText = "OH"
    fileOut = "%s_%s.eps"%(subsystem,extensionName)
    
    tailSubsystem = "" 
    system2 = "%s_Dynamics_TimeAdjusted"%(subsystem)
    n2=4
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n2)
    heatMap.set_extension(extensionName)
    heatMap.set_initial(0)
    heatMap.set_subsystem("_Single")
    heatMap.set_system(system2)
    heatMap.set_mapping("bilinear")
    heatMap.set_deltaZ(3)
    ref = 0.005
    dev = 0.001
    heatMap.set_xlabel("Z")
    heatMap.set_ylabel("$S_1(\\theta_{%s})$"%(ylabelText))
    heatMap.set_colormaxmin(0.5,0.65)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(1)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot1()


    
    return subsystem
    


def main():    
    subsystemList=["MNWN","MFWN","MNWN_TIP4P", "MFWN_TIP4P", "MNWF", "MFWF"]
    subsystemList = [ syst for syst in subsystemList ]
    list(map(getAllPlots,subsystemList))


if __name__ == "__main__":
    main()
