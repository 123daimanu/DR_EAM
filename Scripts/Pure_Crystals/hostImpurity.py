import numpy as num
import sys
import re
import pandas as pan


def alloySolutionEntalphy(host,impurity):
    fileHost=open(host+".stat")
    fileImpurity=open(impurity+".stat")
    fileHostImpurity = open(host+impurity+".stat")




    fileImpurityOmd=open(impurity+".omd")
    linesImpurityOmd=fileImpurityOmd.readlines()
    nMolI=float(linesImpurityOmd[-4].split()[0])+1

    fileHostOmd=open(host+".omd")
    linesHostOmd=fileHostOmd.readlines()
    nMolH=float(linesHostOmd[-4].split()[0])+1


    HCohesive=(float(fileHost.readlines()[-1].split()[1]))*0.043364/nMolH
    ICohesive=(float(fileImpurity.readlines()[-1].split()[1]))*0.043364/nMolI

    HICohesive=(float(fileHostImpurity.readlines()[-1].split()[1]))*0.043364
    alloySolution=(HICohesive-(nMolH-1)*HCohesive-ICohesive)
    
    return alloySolution




def main():


    names = ["Cu","Ag","Au","Ni","Pd","Pt","Al","Pb","Fe","Mo","Ta",
            "W","Co","Ti","Zr"]
    dictOfNames={"Cu":0,"Ag":1,"Au":2,"Ni":3,"Pd":4, "Pt":5, "Al":6, "Pb":7, "Fe":8, "Mo":9, "Ta":10,"W":11,"Co":12,"Ti":13,"Zr":14}
    hostImp =[[hos,imp] for hos in names for imp in names]

    his=[] #[(host,impurity,energy)]
    for pair in hostImp:
        host=pair[0]
        impurity=pair[1]
        if (host!=impurity):
            alloySolution = alloySolutionEntalphy(host,impurity) 
            his.append([dictOfNames[host],dictOfNames[impurity],alloySolution])            
        else:
            his.append([dictOfNames[host],dictOfNames[impurity],9999])

    dataArray=num.zeros(len(names)*len(names)).reshape(len(names),len(names))
    for data in his:
        dataArray[data[1],data[0]]="{:+.3f}".format(data[2])

    dataFrame=pan.DataFrame(dataArray)
    dataFrame.to_csv("hostImpurity.csv",sep=",",header=names , index=names)

    




if __name__ == "__main__":
    main()
