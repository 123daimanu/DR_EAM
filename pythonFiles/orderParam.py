from function import HeatMap
def getAllPlots(subsystemAtom):
    print("+++++++ PLOT GENERATING FOR %s +++++++"%subsystemAtom)
    subsystem = subsystemAtom[0]
    side = subsystemAtom[1]
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    #fileOut = "%s_%s_OrderProb.eps"%(subsystem,side)
    fileOut = "%s_merged_OrderProb.eps"%(subsystem)
    tailSubsystem = "" 
    system2 = "%s_Dynamics_TimeAdjusted"%(subsystem)
    n2=4
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n2)
    heatMap.set_extension("OrderProb")
    heatMap.set_initial(0)

    #heatMap.set_subsystem("_%s_smooth"%(side))
    heatMap.set_subsystem("_Single")
    heatMap.set_system(system2)
    heatMap.set_deltaZ(3)
    ref = 0.005
    dev = 0.007
    heatMap.set_xlabel("Z")
    heatMap.set_ylabel("$S_1(\\theta_{D})$")
    #heatMap.set_colormaxmin(0.0,ref + dev)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(1)
    heatMap.HeatMapMatrix()
    heatMap.heatMapPlot1()


    
    return subsystem


def getDifferencePlots(sys1,sys2,side):
    print("+++++++ DIFFERENCE PLOT GENERATING FOR %s +++++++"%(sys1 + "--" + sys2))
    folder = "/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ThermalConductivity/EqulibratedSystem/"
    fileOut = "%s_%s_%s_OrderProb.eps"%(sys1, sys2, side)
    tailSubsystem = "" 
    system1 = "%s_Dynamics_TimeAdjusted"%(sys1)
    system2 = "%s_Dynamics_TimeAdjusted"%(sys2)
    n2=5
    heatMap = HeatMap.HeatMap(folder)
    heatMap.set_numbers(n2, n2)
    heatMap.set_extension("OrderProb")
    heatMap.set_initial(18)
    
    heatMap.set_subsystem("_%s_smooth"%(side))
    heatMap.set_system(system1, system2)
    heatMap.set_deltaZ(3)
    heatMap.set_colormaxmin(-0.0001,0.0001)
    heatMap.set_fileOut(fileOut)
    heatMap.set_freqThreshold(180)
    heatMap.HeatMapMatrix()
    heatMap.diffMatMatrix()
    heatMap.heatMapDifferencePlot()

    


def main():    
    subsystemList=["MNWN","MFWN","MNWN_TIP4P", "MFWN_TIP4P", "MNWF", "MFWF"]
    side = ["L", "R"]
    subsystemList = [ [syst, lr] for syst in subsystemList for lr in side ]
    list(map(getAllPlots,subsystemList))
'''
    system1 = ["MNWN","MNWN_TIP4P", "MNWF"]
    system2 = ["MFWN","MFWN_TIP4P", "MFWF"]

    side1 = ["L"] * 4
    side2 = ["R"] * 4
    list(map(getDifferencePlots,system1,system2,side1))
    list(map(getDifferencePlots,system1,system2,side2))
'''
if __name__ == "__main__":
    main()
