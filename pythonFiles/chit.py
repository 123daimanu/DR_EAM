import numpy as num

def chi(n,alpha,V):
    alpha1=4*num.pi*n/float(V)*alpha
    den=3*alpha1
    nu=3-alpha1
    return den/nu


n=num.array([3600,4800,6000,7200])
v=num.array([51200.7370,69271.5885,87343.3981,105413.2781])
alpha=4.5047

for var in range(num.size(n)):
   print chi(n[var],alpha,v[var])

