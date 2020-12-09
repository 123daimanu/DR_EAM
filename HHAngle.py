from function import HeatMap
def getAllPlots(subsystemAtom):
    print("+++++++ PLOT GENERATING FOR %s +++++++"%subsystemAtom)
    subsystem = subsystemAtom[0]
    side = subsystemAtom[1]
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    #fileOut = "%s_%s_HHAngle.eps"%(subsystem,side)
    fileOut = "%s_merged_HHAngle.eps"%(subsystem)
    tailSubsystem = "" 
    system2 = "%s_Dynamics_TimeAdjusted"%(subsystem)
    n2=4
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n2)
    heatMap.set_extension("HHAngle")
    heatMap.set_initial(0)
    #heatMap.set_subsystem("_%s_merged_smooth"%(side))
    heatMap.set_subsystem("_Single_merged_smooth")
    heatMap.set_system(system2)
    heatMap.set_deltaZ(3)
    ref = 0.005
    dev = 0.001
    heatMap.set_xlabel("Z")
    heatMap.set_ylabel("$S_1(\\theta_{HH})$")
    heatMap.set_colormaxmin(ref - dev,ref + dev)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(1)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot1()


    
    return subsystem
    


def main():    
    subsystemList=["MNWN","MFWN","MNWN_TIP4P", "MFWN_TIP4P", "MNWF", "MFWF"]
    side = ["L", "R"]
    subsystemList = [ [syst, lr] for syst in subsystemList for lr in side ]
    list(map(getAllPlots,subsystemList))


if __name__ == "__main__":
    main()
