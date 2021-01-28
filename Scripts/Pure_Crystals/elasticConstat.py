import sys
import re


fileElastic=open(sys.argv[1],'r')
linesElastic=fileElastic.readlines()

for line in linesElastic:
    word=line.split()
    if "Bulk" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        bulk = [float(x) for x in re.findall(match_number,word[4])]
    if "Shear" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        shear = [float(x) for x in re.findall(match_number,word[4])]
    
    if "Young's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        youngs = [float(x) for x in re.findall(match_number,word[5])]
     
    if "Poisson's" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        poisson = [float(x) for x in re.findall(match_number,word[4])]

    if "Universal" in word:
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *[-+]?\ *[0-9]+)?')
        universal = [float(x) for x in re.findall(match_number,word[3])]

    
        

 
print("Bulk:%f \n Shear: %f \n Youngs: %f \n Poisson's: %f \n Universal: %f"%(bulk[0],shear[0],youngs[0],poisson[0],universal[0]))



