'''
read_HDS.py
a m!ke@usgs joint
contact: mnfienen@usgs.gov
Code to read in a windoze formatted HDS file with binary head output from
MODFLOW

12/20/2009
'''

import numpy as np
from scipy.io.numpyio import fread




######
# Set up a class for the data to live in
######
class hds:
    def __init__(self,nlay,nrow,ncol,kstp):
        self.ktimestep  = kstp
        self.heads      = np.zeros((nrow,ncol,nlay))

def read_head_MODFLOW(infile,nlay,nrow,ncol,ss,nan_flag):
	ifp = open(infile,'rb')
	# holders for the data reading in
	kstp    = []
	kper    = []
	pertim  = []
	totim   = []
	heads   = []
	newTime = True
	i=-1
	while 1:
		kstp_tmp = fread(ifp,1,'i')
		if not kstp_tmp:
			break
		else:
			kstp.append(kstp_tmp[0])
			if newTime == True:
				heads.append(hds(nlay,nrow,ncol,kstp[-1]))
				newTime = False
				i +=1
			kper.append(fread(ifp,1,'i')[0])
			pertim.append(fread(ifp,1,'f')[0])
			totim.append(fread(ifp,1,'f')[0])
			junkus = fread(ifp,16,'c')
			pos = fread(ifp,3,'i')
			headin = fread(ifp,pos[0]*pos[1],'f').reshape(nrow,ncol)
			if nan_flag:
				headin[headin==999] = np.nan
			heads[i].heads[:,:,pos[2]-1]=headin
			if pos[2]==nlay:
				newTime = True
				# here we break out after only one pass if seeking only one
				# stress period (ss means steady-state).  probably not really necessary....
				if ss == True:
					break
	return kstp,kper,heads, pertim
	   	
