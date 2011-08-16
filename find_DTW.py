import numpy as np
import pylab as plt
infile_heads = 'assateague_heads.smp'
infile_elevs = 'xsect1.dat.out'

points = np.genfromtxt(infile_elevs,usecols=(0,),dtype=str)
elevs = np.genfromtxt(infile_elevs,usecols=(3,))
heads = np.loadtxt(infile_heads,usecols=(3,))
dtw = elevs-heads

ofp = open('dtw.dat','w')
for i in np.arange(70):
    ofp.write('%s %f\n' %(points[i],dtw[i]))
ofp.close()

