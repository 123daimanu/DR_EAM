import sys

file_in=sys.argv[1]
file_out=sys.argv[2]
fileOmd=open(file_in)

lines=fileOmd.readlines()
lineNewFile=[]
change=True
for line in lines:
    words=line.split()

    if "useMinimizer" in words:
        words[-1]="True;"
        words.append('\n')
        line=' '.join(words)

    if "\\\ensemble" in words:
        words[0] = "//ensemble"
        line = ' '.join(words)
        words.append('\n')
        line=' '.join(words)


    lineNewFile.append(line)

fileOmd.close()
fileOut=open(file_out,"w")
fileOut.writelines(lineNewFile)
fileOut.close()
