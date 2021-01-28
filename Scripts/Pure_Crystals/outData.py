import sys
import re


element=sys.argv[1]
file_out=sys.argv[2]
fileOmd=open(element+".omd")
#fileCohesive=open(element+".report")
#fileVacancy=open(element+"Vacancy.report")
#fileSurface=open(element+"Vaccum.report")
fileCohesive=open(element+".stat")
fileVacancy=open(element+"Vacancy.stat")
fileSurface=open(element+"Vaccum.stat")
fileElastic = open(element+"Elastic.dat")
fileOut=open(file_out,"a+")

linesOmd=fileOmd.readlines()
nMol=float(linesOmd[-4].split()[0])+1

match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
for line in linesOmd:
    word=line.split()
    if "Hmat:" in word:
        Lx=[float(x) for x in re.findall(match_number,word[2])]
        Ly=[float(y) for y in re.findall(match_number,word[8])]
        Lz=[float(z) for z in re.findall(match_number,word[14])]
        break

Area=Lx[0]*Ly[0]

#Cohesive = [float(x) for x in re.findall(match_number,fileCohesive.readlines()[4])][0]
#Vac = [float(x) for x in re.findall(match_number,fileVacancy.readlines()[4])][0]
#Surface = [float(x) for x in re.findall(match_number,fileSurface.readlines()[4])][0]



Cohesive=float(fileCohesive.readlines()[-1].split()[1])
Vac=float(fileVacancy.readlines()[-1].split()[1])    
Surface=float(fileSurface.readlines()[-1].split()[1])

c=abs(Cohesive/nMol)*0.043  # ev/atom
s=abs((Cohesive-Surface)/(2*Area))*1e16*6.9478e-14     #erg/cm^2
v=(Vac-((nMol-1)/nMol)*Cohesive)*0.043    #ev


linesElastic=fileElastic.readlines()

for line in linesElastic:
    word=line.split()
    if "Bulk" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        bulk = [float(x) for x in re.findall(match_number,word[2])]
    if "Shear" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        shear = [float(x) for x in re.findall(match_number,word[2])]
    
    if "Young's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        youngs = [float(x) for x in re.findall(match_number,word[3])]
     
    if "Poisson's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        poisson = [float(x) for x in re.findall(match_number,word[2])]

    if "Universal" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        universal = [float(x) for x in re.findall(match_number,word[3])]

    
 







#cohesive|Vacancy|Surface|Bulk|Youngs|Elatic_anisotropy|Poissons_ratio
fileOut.write("%s\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\t\t%f\n"%(element,c,v,s,bulk[0],shear[0],youngs[0],poisson[0],universal[0]))
fileOut.close()



