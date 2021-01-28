import sys



def makeMolecule(molecule):
    lineString = """
    }
    molecule{
        name = "%s";
        atom[0]{
            type = "%s";
            position( 0.0, 0.0, 0.0);
        }
    
    }
    
    """%(molecule,molecule)

    return lineString

def makeComponent(molecule):
    lineString="""
    }
    component{
      type = "%s";
        nMol = 1;
        }


    
    """%(molecule)
    
    return lineString



file_in=sys.argv[1]
file_out=sys.argv[2]
impurity=sys.argv[3]
fileOmd=open(file_in)

fileOut=open(file_out,"w")
lines=fileOmd.readlines()

countBraces=0
molecule=True
component=True
lineNewFile=[]
nMol=lines[-4].split()[0]
for line in lines:
    words=line.split()
    
    if "}" in words:
        countBraces+=1

    if countBraces==2 and molecule==True:
       line=makeMolecule(impurity)
       molecule = False
    
    if countBraces==3 and component == True:
        line=makeComponent(impurity)
        component = False


    if "nMol" in words and countBraces==2:
        words[2]=nMol
        words.append(";")
        words.append("\n")
        line=' '.join(words)
    lineNewFile.append(line)
fileOut.writelines(lineNewFile)
fileOut.close()
