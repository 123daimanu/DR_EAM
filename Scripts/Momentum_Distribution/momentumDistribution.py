import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import re
from argparse import RawDescriptionHelpFormatter
import argparse
import textwrap
from scipy.optimize import curve_fit


kb = 8.31451e-7 # boltzman constant in amu Ang^2 /fs^2/K

class MomentumDistribution:
    def __init__(self, file_name, mass):
        self.file = file_name
        self.mass = mass
        
        (filepath, filename) = os.path.split(file_name)
        (outfilePrefix, ext)  = os.path.splitext(filename)
        
        self.outfile = outfilePrefix + ".Temperature"
        self.outplot = outfilePrefix + "_plot.pdf"
        self.filepath = filepath
    
    def getDistribution(self):
        try:
            inFile = open(self.file, 'r')
        except FileNotFoundError:
            print("FileNotFoundError: %s not found"%self.file)
            sys.exit()
        self.metadata = []
        self.momentum = []
        self.count = []
        readfile = True
        line = inFile.readline()
        while readfile:
            if '#' in line:
                self.metadata.append(line)
            else:
                split_line = line.split()
                if split_line:
                    self.momentum.append(float(split_line[0]))
                    self.count.append(float(split_line[1]))
                else:
                    readfile = False
            line = inFile.readline()
        self.metadata.pop()
    
    

    def getFit(self):
        Gauss = lambda x, a, b: a * np.exp(-b * (x)**2)
        coeff,cov = curve_fit(Gauss, np.array(self.momentum), np.array(self.count))
        self.a, self.b= coeff
        self.cov = cov

    def calcTemp(self):
        self.temp = 1.0/(2.0 * self.mass * kb * self.b)

    def plotDistribution(self):
                   
        mom_max = max(self.momentum)
        mom_min = min(self.momentum)
        Gauss = lambda x, a, b: a * np.exp(-b * (x)**2)
        x = np.linspace(mom_min, mom_max, 1000)
        plt.plot(x, Gauss(x, self.a, self.b), 'b', label = "Best_fit")
        plt.plot(self.momentum, self.count, 'or', label = "Data points")
        plt.xlabel("Momentum(amu A/fs)")
        plt.ylabel("count")
        plt.title("Temp: %.3f"%self.temp)
        plt.legend()
        
        plt.savefig 
        plotfile = self.filepath + "/" + self.outplot
        plt.savefig(plotfile)
        plt.show()


    def write(self):
        outfile = open(self.filepath + "/" + self.outfile,'w+')
        outfile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        outfile.write("+ The distribution is fitted with gaussian function:      +\n")
        outfile.write("+                                                         +\n")
        outfile.write("+        p(x) = a0 * exp(-a1*x^2)                         +\n")
        outfile.write("+                                                         +\n")
        outfile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
        outfile.write("     Temperature: %.3f                                       \n"%self.temp)
        outfile.write("     Generalized mass: %.3f\n\n"%self.mass)
        outfile.write("     Parameters: a0 = %.3f\n"%self.a)
        outfile.write("                 a1 = %.3f\n\n"%self.b)
        outfile.write("     Covariance Matrix:\n\n")
        outfile.write("\t\t\t%.3f\t%.3f\n\t\t\t%.3f\t%.3f\n\n"%(self.cov[0][0], self.cov[0][1],\
                                                                self.cov[1][0], self.cov[1][1]))
        outfile.close()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+ The distribution is fitted with gaussian function:      +")
        print("+                                                         +")
        print("+        p(x) = a0 * exp(-a1*x^2)                         +")
        print("+                                                         +")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        print("     Temperature: %.3f                                       "%self.temp)
        print("     Generalized mass: %.3f\n"%self.mass)
        print("     Parameters: a0 = %.3f"%self.a)
        print("                 a1 = %.3f\n"%self.b)
        print("     Covariance Matrix:\n\n")
        print("\t\t\t%.3f\t%.3f\n\t\t\t%.3f\t%.3f\n\n"%(self.cov[0][0], self.cov[0][1],\
                                                                self.cov[1][0], self.cov[1][1]))
        

def usage():
    print (__doc__)

def main(argv):
    parser = argparse.ArgumentParser(
        description='Fit the momentum distribution to find temperature',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""
                    Example: python2.7 momentumDistribtuion -i Au.px -m 119.19
                """)
   
 
    parser.add_argument("-m","--mass=", action="store",
                        dest="mass",type=float, help="Generalized mass")
    parser.add_argument("-i","--input=", action="store",
                        dest="inFile", help="Input the momentum distribution file")

    parser.add_argument("-p","--plot=", action="store_true", dest="plotFlag", default = False, help="Flag to plot the distribution and best fit")
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(2)

    args=parser.parse_args()


    if (not args.inFile):
        parser.error("No input file specified")
    
    inFile = args.inFile

    if (not args.mass):
        parser.error("Expected value of generalized mass")
    mass = args.mass

    momentum_dist = MomentumDistribution(inFile, mass)
    momentum_dist.getDistribution()
    momentum_dist.getFit()
    momentum_dist.calcTemp()
    momentum_dist.write()

    if(args.plotFlag):
        momentum_dist.plotDistribution()
        

 
    


if __name__ == "__main__":
    main(sys.argv[1:])


                            
