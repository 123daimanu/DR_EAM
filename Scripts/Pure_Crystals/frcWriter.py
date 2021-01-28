from sys import argv
from scipy.optimize import curve_fit

from numpy import linspace,array,inf
from pylab import plot, ylim, xlim, savefig, show, xlabel, ylabel, title

openFile=open("metalsFQ1.frc","w")








openFile.write(
"""
// This is the forcefield file for the Embedded Atom Method (EAM)
// parameterized in:
//
//      X. W. Zhou, R. A. Johnson, and H. N. G. Wadley,
//      Phys. Rev. B, 69, 144113 (2004).
//
// Note that as of OpenMD version 2.5, precomputed funcfl or setfl DYNAMO files
// are not required - the splines for the electron density,
// functional, and pair potentials are computed upon initialization.
begin Options
      Name                  EAMZhou2004
      // energies in metallic force fields are usually in eV. Convert to kcal/mol:
      MetallicEnergyUnitScaling     23.0605423
      // All of the other interactions (NonBonded, Fluctuating Charge)
      // will also follow this eV convention
      EnergyUnitScaling     23.0605423
      // measure charges in electrons:
      //ChargeUnitScaling     1.0
      // measure distances in angstroms:
      DistanceUnitScaling   1.0
      EAMMixingMethod   Johnson
end Options


begin BaseAtomTypes
Cu       63.550
Ag      107.87
Au      196.97
Ni       58.710
Pd      106.40
Pt      195.09
Al       26.981538
Pb      207.2
Fe       55.845
Mo       95.94
Ta      180.94788
W       183.84
Mg       24.3050
Co       58.933195
Ti       47.867
Zr       91.224
end BaseAtomTypes

begin EAMAtomTypes
// Equlibrium distances (re) are in angstroms, density parameters (fe,rhoe) are
// in eV/angstrom. Most others (alpha, beta, kappa, lambda, eta) are
// dimensionless. Spline parameters for the energy functional (Fn0, Fn1, Fn2,
// Fn3, F0, F1, F2, F3, Fe) are in eV.
//
// Type     lat re       fe       rhoe      rhos      alpha    beta     A        B        kappa    lambda    Fn0       Fn1      Fn1       Fn3      F0    F1 F2       F3        eta      Fe        rhol rhoh
Cu Zhou2004 FCC 2.556162 1.554485 21.175871 21.175395 8.12762  4.334731 0.39662  0.548085 0.308782 0.756515 -2.170269 -0.263788 1.088878 -0.817603 -2.19 0  0.56183  -2.100595 0.31049  -2.186568 0.85 1.15
Ag Zhou2004 FCC 2.891814 1.106232 14.6041   14.604144 9.13201  4.870405 0.277758 0.419611 0.33971  0.750758 -1.729364 -0.255882 0.91205  -0.561432 -1.75 0  0.744561 -1.15065  0.783924 -1.748423 0.85 1.15
Au Zhou2004 FCC 2.885034 1.529021 19.991632 19.991509 9.516052 5.075228 0.229762 0.356666 0.35657  0.748798 -2.937772 -0.500288 1.601954 -0.83553  -2.98 0  1.706587 -1.134778 1.021095 -2.978815 0.85 1.15
Ni Zhou2004 FCC 2.488746 2.007018 27.562015 27.562031 8.383453 4.471175 0.429046 0.633531 0.443599 0.820658 -2.693513 -0.076445 0.241442 -2.375626 -2.7  0  0.26539  -0.152856 0.44547  -2.7      0.85 1.15
Pd Zhou2004 FCC 2.750897 1.595417 21.335246 21.940073 8.697397 4.638612 0.406763 0.59888  0.397263 0.754799 -2.321006 -0.473983 1.615343 -0.231681 -2.36 0  1.481742 -1.675615 1.13     -2.352753 0.85 1.15
//
// Note that the Pt rhol value below is not mentioned in the original paper,
// but is required for continuity of the functional.
//
Pt Zhou2004 FCC 2.771916 2.336509 33.367564 35.205357 7.105782 3.78975  0.556398 0.696037 0.385255 0.77051  -1.455568 -2.149952 0.528491  1.222875 -4.17 0  3.010561 -2.420128 1.45     -4.145597 0.25 1.15
Al Zhou2004 FCC 2.863924 1.403115 20.418205 23.19574  6.613165 3.527021 0.314873 0.365551 0.379846 0.759692 -2.807602 -0.301435 1.258562 -1.247604 -2.83 0  0.622245 -2.488244 0.785902 -2.824528 0.85 1.15
Pb Zhou2004 FCC 3.499723 0.647872  8.450154  8.450063 9.121799 5.212457 0.161219 0.236884 0.250805 0.764955 -1.42237  -0.210107 0.682886 -0.529378 -1.44 0  0.702726 -0.538766 0.93538  -1.439436 0.85 1.15
Fe Zhou2004 BCC 2.481987 1.885957 20.041463 20.041463 9.81827  5.236411 0.392811 0.646243 0.170306 0.340613 -2.534992 -0.059605 0.193065 -2.282322 -2.54 0  0.200269 -0.14877  0.39175  -2.539945 0.85 1.15
Mo Zhou2004 BCC 2.7281   2.72371  29.354065 29.354065 8.393531 4.47655  0.708787 1.120373 0.13764  0.27528  -3.692913 -0.178812 0.38045  -3.13365  -3.71 0  0.875874  0.776222 0.790879 -3.712093 0.85 1.15
Ta Zhou2004 BCC 2.860082 3.086341 33.787168 33.787168 8.489528 4.527748 0.611679 1.032101 0.176977 0.353954 -5.103845 -0.405524 1.112997 -3.585325 -5.14 0  1.640098  0.221375 0.848843 -5.141526 0.85 1.15
W  Zhou2004 BCC 2.74084  3.48734  37.234847 37.234847 8.900114 4.746728 0.882435 1.394592 0.139209 0.278417 -4.946281 -0.148818 0.365057 -4.432406 -4.96 0  0.661935  0.348147 0.582714 -4.961306 0.85 1.15
Mg Zhou2004 HCP 3.196291 0.544323  7.1326    7.1326  10.228708 5.455311 0.137518 0.22593  0.5      1        -0.896473 -0.044291 0.162232 -0.68995  -0.9  0  0.122838 -0.22601  0.431425 -0.899702 0.85 1.15
Co Zhou2004 HCP 2.505979 1.975299 27.206789 27.206789 8.679625 4.629134 0.421378 0.640107 0.5      1        -2.541799 -0.219415 0.733381 -1.589003 -2.56 0  0.705845 -0.68714  0.694608 -2.559307 0.85 1.15
Ti Zhou2004 HCP 2.933872 1.8632   25.565138 25.565138 8.775431 4.68023  0.373601 0.570968 0.5      1        -3.203773 -0.198262 0.683779 -2.321732 -3.22 0  0.608587 -0.75071  0.558572 -3.219176 0.85 1.15
Zr Zhou2004 HCP 3.199978 2.230909 30.879991 30.879991 8.55919  4.564902 0.424667 0.640054 0.5      1        -4.485793 -0.293129 0.990148 -3.202516 -4.51 0  0.928602 -0.98187  0.597133 -4.509025 0.85 1.15
end EAMAtomTypes




begin AtomTypes
//name baseatomtype
Pt_FQ  Pt
Cu_FQ   Cu
Ag_FQ   Ag
Au_FQ   Au
Pd_FQ   Pd
Pb_FQ   Pb
Al_FQ   Al
Fe_FQ   Fe
Mo_FQ   Mo
Ta_FQ   Ta
W_FQ    W
Mg_FQ   Mg
Co_FQ   Co
Ti_FQ   Ti
Zr_FQ   Zr
Ni_FQ Ni
end AtomTypes

begin FluctuatingChargeAtomTypes
// Fictitious ChargeMass has units of (fs / e)^2 kcal / mol  (note the ps->fs difference between
// this code and the Rick, Stuart, and Berne paper
//Name  chargeMass (fs^2 kcal/e^2 mol) EAM  nValence coupling  q0 u0 k0 q1 u1 k1 q2 u2 k2
//all the parameters are converted in to eV

"""
)

names = ["Cu_FQ",
        "Ag_FQ",
        "Au_FQ",
        "Ni_FQ",
        "Pd_FQ",
        "Pt_FQ",
        "Al_FQ",
        "Pb_FQ",
        "Fe_FQ",
        "Mo_FQ",
        "Ta_FQ",
        "W_FQ",
        "Mg_FQ",
        "Co_FQ",
        "Ti_FQ",
        "Zr_FQ"]
ktho = [7.63,
7.58,
7.92,
8.08,
7.59,
6.15,
5.54,
6.70,
9.49,
7.38,
7.12,
7.79,
7.68,
8.31,
7.18,
6.42
]
        
kemp = [7.87,
        8.10,
        9.38,
        7.78,
        9.13,
        12.34,
        11.01,
        12.50,
        9.88,
        5.62,
        7.51,
        6.33,
        8.31,
        6.86,
        7.15,
        5.85]

kmean = [7.752095957,
        7.83834703,
        8.646583171,
        7.929804495,
        8.356597494,
        9.243615159,
        8.275440295,
        9.603383917,
        9.687695934,
        6.502373392,
        7.319018117,
        7.063069826,
        7.99760472,
        7.58601708,
        7.165019152,
        6.136937706
        ]




eAffinityIoni={}
oxStates={}


#   https://doi.org/10.1063/1.1679514
#   https://www.webelements.com/
#   detailed refernce can be found in above link
#   All the units of the energies are in kJ/mol
#   To convert kJ/mol to eV the conversion factor is 0.01
#   The oxidation states should be scaled by 0.4
#   http://www.compoundchem.com/wp-content/uploads/2015/11/The-Periodic-Table-Of-Oxidation-States-2016.png
#   http://www.compoundchem.com/2015/11/17/oxidation-states/
#   http://periodictable.com/Elements/029/data.html
#   For magnesium, there are only three oxidation states i.e 0,1,2. But the self energy has 4 fit parameters. So, we take the ionization
#   energy of magnesium for oxidation state 3 from the link given above.
eAffinityIoni1 = {"Cu_FQ":[118.4,0,745.48,1957.92,3555,5536],
        "Ag_FQ":[125.6,0,731.00,2072.93,3358,4728],
        "Au_FQ":[222.8,0,890.13,1949.3,2890],
        "Ni_FQ":[112,0,737.14,1753.03,3395.0,5299],
        "Pd_FQ":[0,804.38,1875,3177,4438,5886,6114],
        "Pt_FQ":[205.3,0,864.40,1791,2800,4150,5400,7240],
        "Al_FQ":[42.5,0,577.54,1816.68,2744.78],
        "Pb_FQ":[35.1,0,715.60,1450.42,3081.17,4084.47],
        "Fe_FQ":[15.7,0,762.47,1562.98,2957.4,5298,7236,9551],
        "Mo_FQ":[71.9,0,684.32,1559,2618,3891,5250,6641],
        "Ta_FQ":[31.00,0,728.42,1560,2230,3380,4657.5],
        "W_FQ":[78.6,0,758.76,1580,2510,3690,4979,6249],
        "Mg_FQ":[0,737.75,1450.68,7732.68,10542.51],
        "Co_FQ":[63.7,0,760.40,1648.39,3232.3,4947,7671],
        "Ti_FQ":[7.6,0,658.81,1309.84,2652.55,41.74],
        "Zr_FQ":[0,640.10,1267,2236,3320.87]}


oxidationStates1 = {"Cu_FQ":[-1,0,1,2,3,4],
        "Ag_FQ":[-1,0,1,2,3,4],
        "Au_FQ":[-1,0,1,2,3],
        "Ni_FQ":[-1,0,1,2,3,4],
        "Pd_FQ":[0,1,2,3,4,5,6],
        "Pt_FQ":[-1,0,1,2,3,4,5,6],
        "Al_FQ":[-1,0,1,2,3],
        "Pb_FQ":[-1,0,1,2,3,4],
        "Fe_FQ":[-1,0,1,2,3,4,5,6],
        "Mo_FQ":[-1,0,1,2,3,4,5,6],
        "Ta_FQ":[-1,0,1,2,3,4,5],
        "W_FQ":[-1,0,1,2,3,4,5,6],
        "Mg_FQ":[0,1,2,3,4],
        "Co_FQ":[-1,0,1,2,3,4,5],
        "Ti_FQ":[-1,0,1,2,3,4],
        "Zr_FQ":[0,1,2,3,4]}
eAffinityIoni2 = {"Cu_FQ":[-119.235,0,745.48,1957.92,3555,5536],
        "Ag_FQ":[-125.6,0,731.00,2072.93,3358,4728],
        "Au_FQ":[-222.747,0,890.13,1949.3,2890],
        "Ni_FQ":[-111.65,0,737.14,1753.03,3395.0,5299],
        "Pd_FQ":[-54.067,0,804.38,1875,3177,4438],
        "Pt_FQ":[-205.041,0,864.40,1791,2800,4150],
        "Al_FQ":[-41.762,0,577.54,1816.68,2744.78],
        "Pb_FQ":[-34.4204,0,715.60,1450.42,3081.17,4084.47],
        "Fe_FQ":[-14.785,0,762.47,1562.98,2957.4,5298],
        "Mo_FQ":[-72.10,0,684.32,1559,2618,3891],
        "Ta_FQ":[-31.00,0,728.42,1560,2230,3380],
        "W_FQ":[-78.76,0,758.76,1580,2510,3690],
        "Mg_FQ":[0,737.75,1450.68,7732.68,10542.51],
        "Co_FQ":[-63.898,0,760.40,1648.39,3232.3,4947,7671],
        "Ti_FQ":[-8,0,658.81,1309.84,2652.55],
        "Zr_FQ":[-41.1,0,640.10,1267,2236,3320.87]}
 


# 'Au_FQ': [-222.747, 0, 890.13, 2839.43, 5729.43],
# 'Mg_FQ': [40, 0, 737.75, 2188.4300000000003, 9921.11, 20463.620000000003], 
eAffinityIoni={'Ag_FQ': [-125.6, 0, 731.0, 2803.93, 6161.93, 10889.93],
         'Al_FQ': [-41.762, 0, 577.54, 2394.2200000000003, 5139.0,16716.5],
          'Au_FQ': [-222.747, 0, 890.13, 2839.43,5729.43,10069.43],
           'Co_FQ': [-63.898, 0, 760.4, 2408.79, 5641.09, 10588.09, 18259.09],
            'Cu_FQ': [-119.235, 0, 745.48, 2703.4, 6258.4, 11794.4],
             'Fe_FQ': [-14.785, 0, 762.47, 2325.45, 5282.85, 10580.85],
             'Mg_FQ': [149.55, 0, 737.75, 2188.4300000000003, 9921.11], 
             #'Mg_FQ': [40, 0, 737.75, 2188.4300000000003, 9921.11], 
             #'Mg_FQ': [0, 737.75, 2188.4300000000003, 9921.11],
             'Mo_FQ': [-72.1, 0, 684.32, 2243.32, 4861.32, 8752.32],
                'Ni_FQ': [-111.65, 0, 737.14, 2490.17, 5885.17, 11184.17],
                 'Pb_FQ': [-34.4204, 0, 715.6, 2166.02, 5247.1900000000005, 9331.66,15971.66],
                  'Pd_FQ': [-54.067, 0, 804.38, 2679.38, 5856.38, 10294.380000000001],
                   'Pt_FQ': [-205.041, 0, 864.4, 2655.4, 5455.4, 9605.4],
                    'Ta_FQ': [-31.0, 0, 728.42, 2288.42, 4518.42, 7898.42],
                     'Ti_FQ': [-7.6, 0, 658.81, 1968.6499999999999, 4621.2,8795.85],
                      'W_FQ': [-78.76, 0, 758.76, 2338.76, 4848.76, 8538.76],
                       'Zr_FQ': [-41.1, 0, 640.1, 1907.1, 4143.1, 7463.97,15215.97]}


oxidationStates = {"Cu_FQ":[-1,0,1,2,3,4],
        "Ag_FQ":[-1,0,1,2,3,4],
        "Au_FQ":[-1,0,1,2,3,4],
        "Ni_FQ":[-1,0,1,2,3,4],
        "Pd_FQ":[-1,0,1,2,3,4],
        "Pt_FQ":[-1,0,1,2,3,4],
        "Al_FQ":[-1,0,1,2,3,4],
        "Pb_FQ":[-1,0,1,2,3,4,5],
        "Fe_FQ":[-1,0,1,2,3,4],
        "Mo_FQ":[-1,0,1,2,3,4],
        "Ta_FQ":[-1,0,1,2,3,4],
        "W_FQ":[-1,0,1,2,3,4],
        "Mg_FQ":[-1,0,1,2,3],
        #"Mg_FQ":[0,1,2,3],
        "Co_FQ":[-1,0,1,2,3,4,5],
        "Ti_FQ":[-1,0,1,2,3,4],
        "Zr_FQ":[-1,0,1,2,3,4,5]}# for Zr try adding -1 oxidation states


Nv= {   "Cu_FQ":0.57 ,
        "Ag_FQ":0.48 ,
        "Au_FQ":0.59 ,
        "Ni_FQ":0.45 ,
        "Pd_FQ":0.48 ,
        "Pt_FQ":1.64 ,
        "Al_FQ":1.22 ,
        "Pb_FQ":1.83 ,
        "Fe_FQ":1.20 ,
        "Mo_FQ":0.31 ,
        "Ta_FQ":0.49 ,
         "W_FQ":0.34 ,
        "Mg_FQ":0.67 ,
        "Co_FQ":0.33 ,
        "Ti_FQ":0.46 ,
        "Zr_FQ":0.45 }
eneg={"Cu_FQ":11.6,
        "Ag_FQ":11.76,
        "Au_FQ":15.84,
        "Ni_FQ":11.63,
        "Pd_FQ":13.6,
        "Pt_FQ":14.10,
        "Al_FQ":9.62,
        "Pb_FQ":14.44,
        "Fe_FQ":11.10,
        "Mo_FQ":13.30,
        "Ta_FQ":8.9,
        "W_FQ":14.64,
        "Mg_FQ":7.62,
        "Co_FQ":11.43,
        "Ti_FQ":9.16,
        "Zr_FQ":7.75}

enegNew={"Cu_FQ":10.75,
        "Ag_FQ":10.9,
        "Au_FQ":13.89,
        "Ni_FQ":10.8,
        "Pd_FQ":12.22,
        "Pt_FQ":12.61,
        "Al_FQ":9.33,
        "Pb_FQ":12.86,
        "Fe_FQ":10.41,
        "Mo_FQ":12.3,
        "Ta_FQ":8.8,
        "W_FQ":13.01,
        "Mg_FQ":7.86,
        "Co_FQ":10.66,
        "Ti_FQ":8.99,
        "Zr_FQ":7.96}



for var in range(len(names)):
    print(names[var])
    b=ktho[var]
    a=enegNew[names[var]]
    q=array(oxidationStates[names[var]])*0.4
    ene=array(eAffinityIoni[names[var]])*0.0103643
    print(q.size)
    print(ene.size)
    f= lambda x,c,d,e,ff:a*x+b*x**2+c*x**3+d*x**4+e*x**5+ff*x**6
    #f= lambda x,c,d : a*x+b*x**2+c*x**3+d*x**4
 
    param=curve_fit(f,q,ene)
    c,d,e,ff=param[0]

    print(a,b,param[0])
    x=linspace(-20,20,1000)
    plot(q,ene,".")
    plot(x,f(x,c,d,e,ff))
    xlabel("Oxidation States")
    ylabel("Energy")
    title(names[var][:-3])
    ylim([-10,200])
    xlim([-1.5,2.5])
    savefig("%s.pdf"%(names[var]))
    show()
    openFile.write("%s 	400.0 EAMPoly   %f 1 %f 2 %f 3 %f 4 %f 5 %f 6 %f\n"%(names[var],Nv[names[var]],a,b,c,d,e,ff))
openFile.write("end FluctuatingChargeAtomTypes")
openFile.close()
