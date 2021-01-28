import sys

file_in=sys.argv[1]
file_out=sys.argv[2]
fileOmd=open(file_in)

fileOut=open(file_out,"w")
lines=fileOmd.readlines()


lineNewFile=[]
nMol=lines[-4].split()[0]
lines[-4]=""
for line in lines:
    words=line.split()

    if "nMol" in words:
        words[2]=nMol
        words.append(";\n")
        line=' '.join(words)
    if "</StuntDoubles>" in words:
        lineNewFile.pop()
    lineNewFile.append(line)
fileOut.writelines(lineNewFile)
fileOut.close()
