from function import HeatMap
def getAllPlots(subsystemAtom):
    print("+++++++ PLOT GENERATING FOR %s +++++++"%subsystemAtom)
    subsystem = subsystemAtom
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    fileOut = "%s_Vcorr.eps"%(subsystem)
    tailSubsystem = "" 
    system2 = "%s_Dynamics_TimeAdjusted"%(subsystem)
    n2=3
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n2)
    heatMap.set_extension("hAngle")
    heatMap.set_initial(18)
    heatMap.set_subsystem("_smooth")
    heatMap.set_system(system2)
    heatMap.set_deltaZ(3)
    heatMap.set_colormaxmin(0.004,0.006)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(180)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot1()


    
    return subsystem
    


def main():    
    subsystemList=["MNWN","MFWN","MNWN_TIP4P", "MFWN_TIP4P", "MNWF", "MFWF"]
    list(map(getAllPlots,subsystemList))


if __name__ == "__main__":
    main()
