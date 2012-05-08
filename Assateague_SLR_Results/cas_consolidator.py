import numpy as np

def fillin_data(carr,cstr,indat):
    carr = np.vstack(carr,indat[cstr])
    return carr



infiles = ['SEAWAT2NETICA_SLR_00.cas','SEAWAT2NETICA_SLR_02.cas',
				'SEAWAT2NETICA_SLR_04.cas','SEAWAT2NETICA_SLR_06.cas']

ofp = open('All_SLR.cas','w')
ofp.write('islandwidth islandelev maxWT mean_rch max_WT_loc mean_DTW max_DTW\n')
    
islandwidth = np.empty(0)
islandelev = np.empty(0)
maxWT = np.empty(0)
mean_rch = np.empty(0)
max_WT_loc = np.empty(0)
mean_DTW = np.empty(0)
max_DTW = np.empty(0)

for cfile in infiles:
    indat = np.genfromtxt(cfile,names=True,dtype=None)
    islandwidth = np.hstack((islandwidth,indat['islandwidth']))
    islandelev = np.hstack((islandelev,indat['islandelev']))
    maxWT = np.hstack((maxWT,indat['maxWT']))
    mean_rch = np.hstack((mean_rch,indat['mean_rch']))
    max_WT_loc = np.hstack((max_WT_loc,indat['max_WT_loc']))
    mean_DTW = np.hstack((mean_DTW,indat['mean_DTW']))
    max_DTW = np.hstack((max_DTW,indat['max_DTW']))
    
for i in np.arange(len(islandelev)):
    ofp.write('%f ' %(islandwidth[i]))
    ofp.write('%f ' %(islandelev[i]))
    ofp.write('%f ' %(maxWT[i]))
    ofp.write('%f ' %(mean_rch[i]))
    ofp.write('%f ' %(max_WT_loc[i]))
    ofp.write('%f ' %(mean_DTW[i]))
    ofp.write('%f\n' %(max_DTW[i]))
ofp.close()
