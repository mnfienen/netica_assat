import numpy as np

infile = 'xsect1.dat'
[x,y,elev]= np.loadtxt(infile,unpack=True)

ofp = open(infile + '.out','w')

for i,cx in enumerate(x):
    for j in np.arange(10):
        ofp.write('%10s %f %f %f %d\n' %('p' + str(i+1) + '_L' + str(j+1),cx,y[i],elev[i],j+1))