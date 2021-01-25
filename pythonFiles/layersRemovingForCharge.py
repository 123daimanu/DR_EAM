#import numpy as num


# Program makes cwe for the differnt atom positoin of the file that has the some layres removed



omdFile=open("/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ChargeDiffusion/Sphere/PtSphereDiffusion.omd")			#opens the initial .omd file that has layers removed
#charge=0 placing neutral charge
charge=float(0.)
lines=omdFile.readlines()
linesAppend=[]
process="Read"
for line in lines:
	lineApp=str.split(line);
	if len(lineApp)==0:
		continue;
	if(lineApp[0]=="<StuntDoubles>"):
		process="Write";
		continue;  
	if (lineApp[0]=="</StuntDoubles>"):
		break;
	if(process=="Write"):
		lineApp[1]="0"
		lineApp[2]="cwe"
		lineApp[3]=str(charge)
		lineApp[4]="0"
		lineApp[5]="0"
		lineApp[6]="0"
		lineApp[7]="0"
		
		last="\n"
		lineApp.append(last)
		sep="\t"
		linesAppend.append(sep.join(lineApp))

	
cweFileNew=open("/afs/crc.nd.edu/user/h/hbhattar/Hemanta/metals/ChargeDiffusion/Sphere/cwe_layers_reduce.dat","w")
cweFileNew.writelines("<SiteData>\n")
cweFileNew.writelines(linesAppend)
cweFileNew.writelines("</SiteData>\n")
cweFileNew.close()
