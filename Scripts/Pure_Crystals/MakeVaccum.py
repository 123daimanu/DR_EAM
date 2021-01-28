import sys

file_in=sys.argv[1]
file_out=sys.argv[2]
fileOmd=open(file_in)

fileOut=open(file_out,"w")
lines=fileOmd.readlines()
lineNewFile=[]
change=True
for line in lines:
    words=line.split()

    if "Hmat:" in words:
        words[-2]=str(float(words[-2])*5)
        words.append('\n')
        line=' '.join(words)



    lineNewFile.append(line)
fileOut.writelines(lineNewFile)
fileOut.close()
