import numpy as np
import sys
import re



def DumpExtractor(filename, frames, atomNumber, atomPlate):

    """
    infoDict=DumpExtractor(filename,frames,atomNumber,atomPlate)


    Function that extracts the information from the .dump file created by openmd


        Inputs:
      ===========


       filename:

                   Path of the dump file from which the information is to be extracted

        frame:

                    Total number of frames in the dump file

        atomNumber:

                    Totla number of atoms in the slab or crystal

        atomPlate:

                    Total number of atoms in the capacitor plates



        Outputs:
     =============

     infoDict:

             Dictonary containing position, velocity, chargeQV, electricField, plateEQV.
             Postion is a list of [x,y,z] and each x,y,z are array of x[frames][sites]
             velocity is a list of [vx,vy,vz] and each vx,vy,vz are array of vx[frames][sites]
             chargeQV is a lisf of [c,cv] and each c and cv are array of c[frame][sites]
             electric field is list of [ex,ey,ez] and each are array of ex[frame][sites]
             plateEQV is the list of [pex,pey,pez,pc,pcv] and each are array of pex[frames][sites]"""
    fileDump = open(filename)  # dump file for info extraction
    linesDump = fileDump.readlines()

    if linesDump[-1] != "</OpenMD>\n":
        print("Error: Incomplete file")
        sys.exit()
    processP = "Wait"
    processC = "Wait"

    # information storage matrix
    # posiiton and velocity storage
    x = np.zeros((frames, atomNumber))
    y = np.zeros((frames, atomNumber))
    z = np.zeros((frames, atomNumber))
    vx = np.zeros((frames, atomNumber))
    vy = np.zeros((frames, atomNumber))
    vz = np.zeros((frames, atomNumber))

    # charge and velocity storage matrix
    c = np.zeros((frames, atomNumber))
    cv = np.zeros((frames, atomNumber))
    ex = np.zeros((frames, atomNumber))
    ey = np.zeros((frames, atomNumber))
    ez = np.zeros((frames, atomNumber))
    pc = np.zeros((frames, atomPlate))
    pcv = np.zeros((frames, atomPlate))
    pex = np.zeros((frames, atomPlate))
    pey = np.zeros((frames, atomPlate))
    pez = np.zeros((frames, atomPlate))
    efieldConverter = 1.0 / 23.0609  # converts kcal mol^-1 to V/A
    # frame count initilization
    fCount = 0
    index = 0  # index for the atoms
    for line in linesDump:
        linesSplit = str.split(line)
        length = len(linesSplit)

        if length != 0 and linesSplit[0] == "<StuntDoubles>" and processP == "Wait":
            processP = "Start"
            continue

        elif length != 0 and linesSplit[0] == "</StuntDoubles>" and processP == "Start":
            processP = "Wait"
            index = 0
            continue

        elif length != 0 and linesSplit[0] == "<SiteData>" and processC == "Wait":
            processC = "Start"
            continue

        elif length != 0 and linesSplit[0] == "</SiteData>" and processC == "Start":
            fCount = fCount + 1
            index = 0
            processC = "Wait"
            continue

        elif fCount >= frames:
            break

        else:
            processP = processP
            processC = processC

        if processP == "Start":
            x[fCount][int(linesSplit[0])] = float(linesSplit[2])
            y[fCount][int(linesSplit[0])] = float(linesSplit[3])
            z[fCount][int(linesSplit[0])] = float(linesSplit[4])
            vx[fCount][int(linesSplit[0])] = float(linesSplit[5])
            vy[fCount][int(linesSplit[0])] = float(linesSplit[6])
            vz[fCount][int(linesSplit[0])] = float(linesSplit[7])

        if processC == "Start":
            if int(linesSplit[0]) < atomNumber:
                c[fCount][int(linesSplit[0])] = float(linesSplit[3])
                cv[fCount][int(linesSplit[0])] = float(linesSplit[4])
                ex[fCount][int(linesSplit[0])] = float(linesSplit[5]) * efieldConverter
                ey[fCount][int(linesSplit[0])] = float(linesSplit[6]) * efieldConverter
                ez[fCount][int(linesSplit[0])] = float(linesSplit[7]) * efieldConverter
            elif int(linesSplit[0]) == atomNumber and linesSplit[1] == "cwe":
                continue
                c[fCount][int(linesSplit[0])] = float(linesSplit[2])
                cv[fCount][int(linesSplit[0])] = float(linesSplit[3])
                ex[fCount][int(linesSplit[0])] = float(linesSplit[4]) * efieldConverter
                ey[fCount][int(linesSplit[0])] = float(linesSplit[5]) * efieldConverter
                ez[fCount][int(linesSplit[0])] = float(linesSplit[6]) * efieldConverter
            else:
                pc[fCount][int(linesSplit[1])] = float(linesSplit[3])
                pcv[fCount][int(linesSplit[1])] = float(linesSplit[4])
                pex[fCount][int(linesSplit[1])] = float(linesSplit[5])
                pey[fCount][int(linesSplit[1])] = float(linesSplit[6])
                pez[fCount][int(linesSplit[1])] = float(linesSplit[7])

    position = [x, y, z]
    velocity = [vx, vy, vz]
    chargeQV = [c, cv]
    electricField = [ex, ey, ez]
    platesEQV = [pex, pey, pez, pc, pcv]

    infoDict = {
        "position": position,
        "velocity": velocity,
        "chargeQV": chargeQV,
        "electricField": electricField,
        "platesEQV": platesEQV,
    }
    return infoDict


def DumpExtractorIncomplete(filename, frames, atomNumber, atomPlate):

    """
    infoDict=DumpExtractor(filename,frames,atomNumber,atomPlate)


    Function that extracts the information from the .dump file created by openmd


        Inputs:
      ===========


       filename:

                   Path of the dump file from which the information is to be extracted

        frame:

                    Total number of frames in the dump file

        atomNumber:

                    Totla number of atoms in the slab or crystal

        atomPlate:

                    Total number of atoms in the capacitor plates



        Outputs:
     =============

     infoDict:

             Dictonary containing position, velocity, chargeQV, electricField, plateEQV.
             Postion is a list of [x,y,z] and each x,y,z are array of x[frames][sites]
             velocity is a list of [vx,vy,vz] and each vx,vy,vz are array of vx[frames][sites]
             chargeQV is a lisf of [c,cv] and each c and cv are array of c[frame][sites]
             electric field is list of [ex,ey,ez] and each are array of ex[frame][sites]
             plateEQV is the list of [pex,pey,pez,pc,pcv] and each are array of pex[frames][sites]"""
    fileDump = open(filename)  # dump file for info extraction
    linesDump = fileDump.readlines()

    processP = "Wait"
    processC = "Wait"
    fileComplete = True
    try:

        if linesDump[-1] != "</OpenMD>\n":
            print("Error: Incomplete file")
            fileComplete = False
            # sys.exit();

        # information storage matrix
        # posiiton and velocity storage
        x = np.zeros((frames, atomNumber))
        y = np.zeros((frames, atomNumber))
        z = np.zeros((frames, atomNumber))
        vx = np.zeros((frames, atomNumber))
        vy = np.zeros((frames, atomNumber))
        vz = np.zeros((frames, atomNumber))

        # charge and velocity storage matrix
        c = np.zeros((frames, atomNumber))
        cv = np.zeros((frames, atomNumber))
        ex = np.zeros((frames, atomNumber))
        ey = np.zeros((frames, atomNumber))
        ez = np.zeros((frames, atomNumber))
        d = np.zeros((frames, atomNumber))
        pc = np.zeros((frames, atomPlate))
        pcv = np.zeros((frames, atomPlate))
        pex = np.zeros((frames, atomPlate))
        pey = np.zeros((frames, atomPlate))
        pez = np.zeros((frames, atomPlate))

        efieldConverter = 1.0 / 23.0609  # converts kcal mol^-1 to V/A

        # frame count initilization
        fCount = 0
        index = 0  # index for the atoms
        for line in linesDump:
            linesSplit = str.split(line)
            length = len(linesSplit)

            if length != 0 and linesSplit[0] == "<StuntDoubles>" and processP == "Wait":
                processP = "Start"
                continue

            elif (
                length != 0
                and linesSplit[0] == "</StuntDoubles>"
                and processP == "Start"
            ):
                processP = "Wait"
                index = 0
                continue

            elif length != 0 and linesSplit[0] == "<SiteData>" and processC == "Wait":
                processC = "Start"
                continue

            elif length != 0 and linesSplit[0] == "</SiteData>" and processC == "Start":
                fCount = fCount + 1
                index = 0
                processC = "Wait"
                continue

            elif fCount >= frames:
                break

            else:
                processP = processP
                processC = processC

            if processP == "Start":
                x[fCount][int(linesSplit[0])] = float(linesSplit[2])
                y[fCount][int(linesSplit[0])] = float(linesSplit[3])
                z[fCount][int(linesSplit[0])] = float(linesSplit[4])
                vx[fCount][int(linesSplit[0])] = float(linesSplit[5])
                vy[fCount][int(linesSplit[0])] = float(linesSplit[6])
                vz[fCount][int(linesSplit[0])] = float(linesSplit[7])

            if processC == "Start":
                if int(linesSplit[0]) < atomNumber:
                    c[fCount][int(linesSplit[0])] = float(linesSplit[3])
                    cv[fCount][int(linesSplit[0])] = float(linesSplit[4])
                    ex[fCount][int(linesSplit[0])] = (
                        float(linesSplit[5]) * efieldConverter
                    )
                    ey[fCount][int(linesSplit[0])] = (
                        float(linesSplit[6]) * efieldConverter
                    )
                    ez[fCount][int(linesSplit[0])] = (
                        float(linesSplit[7]) * efieldConverter
                    )
                    d[fCount][int(linesSplit[0])] = float(linesSplit[8])
                elif int(linesSplit[0]) == atomNumber and linesSplit[1] == "cwed":
                    continue
                    c[fCount][int(linesSplit[0])] = float(linesSplit[2])
                    cv[fCount][int(linesSplit[0])] = float(linesSplit[3])
                    ex[fCount][int(linesSplit[0])] = (
                        float(linesSplit[4]) * efieldConverter
                    )
                    ey[fCount][int(linesSplit[0])] = (
                        float(linesSplit[5]) * efieldConverter
                    )
                    ez[fCount][int(linesSplit[0])] = (
                        float(linesSplit[6]) * efieldConverter
                    )
                    d[fCount][int(linesSplit[0])] = float(linesSplit[8])
                else:
                    pc[fCount][int(linesSplit[1])] = float(linesSplit[3])
                    pcv[fCount][int(linesSplit[1])] = float(linesSplit[4])
                    pex[fCount][int(linesSplit[1])] = float(linesSplit[5])
                    pey[fCount][int(linesSplit[1])] = float(linesSplit[6])
        position = [x, y, z]
        velocity = [vx, vy, vz]
        chargeQV = [c, cv]
        electricField = [ex, ey, ez]
        density = [d]
        platesEQV = [pex, pey, pez, pc, pcv]

        infoDict = {
            "position": position,
            "velocity": velocity,
            "chargeQV": chargeQV,
            "electricField": electricField,
            "density": density,
            "platesEQV": platesEQV,
            "CFrame": fCount,
        }
        return infoDict
    except:
        position = [x, y, z]
        velocity = [vx, vy, vz]
        chargeQV = [c, cv]
        electricField = [ex, ey, ez]
        density = [d]
        platesEQV = [pex, pey, pez, pc, pcv]

        infoDict = {
            "position": position,
            "velocity": velocity,
            "chargeQV": chargeQV,
            "electricField": electricField,
            "density": density,
            "platesEQV": platesEQV,
            "CFrame": fCount - 1,
        }
        return infoDict


def ReportExtractor(reportFile,lineNo):
    file1=open(reportFile)
    lines1=file1.readlines()
    outLine=lines1[lineNo]
    #match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
    match_number = re.compile('-?[0-9]+\.?[0-9]*(?:[Ee][-+]?[0-9]+)?')
    outData = [float(x) for x in re.findall(match_number, outLine)]
    return outData
