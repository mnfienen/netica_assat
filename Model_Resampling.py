import numpy as np
import matplotlib.pyplot as plt
from headfile import HeadFile



class mod_res:
    
    def plotfield(self,arr2plot,filename):
        fig = plt.figure()
        plt.imshow(arr2plot,interpolation = 'nearest')
        plt.colorbar()
        plt.savefig(filename + '.pdf')
        
    
    def __init__(self, inroot,ISLAND_MID_WIDTH,ISLAND_DISRUPTOR):
        self.inroot = inroot
        self.ISLAND_MIN_WIDTH = ISLAND_MID_WIDTH
        self.ISLAND_DISRUPTOR = ISLAND_DISRUPTOR
        
    def read_dis(self):
        #read the number or rows, number of columns, and top of model
        DX = []
        DY = []
    
        indat = open(self.inroot + '.dis','r').readlines()
        
        # remove the comment lines from the top of the file
        contflag = True
        while contflag:
            if '#' in indat[0]:
                junkus = indat.pop(0)
            else:
                contflag = False
                
        # get the control (uber) parameters
        tmp = indat.pop(0).strip().split()
        self.NLAY = int(tmp.pop(0))
        self.NROW = int(tmp.pop(0))
        self.NCOL = int(tmp.pop(0))
                
        i = 0
        for line in indat:
            if "TOP of Model" in line:
                break
            else:
                i+=1
        del(indat[0:i+1])

        self.modtop = []
        for line in indat:
            if "BOTTOM of Lay" not in line:
                self.modtop.extend(line.strip().split())
            else:
                break
        # read to the bottom of layer 1    
        self.modtop = np.array(self.modtop).astype(float)
        # reshape to model dimensions
        self.modtop = self.modtop.reshape(self.NROW,self.NCOL)

            
    def read_IBOUND(self):
        indat = open('IB1.inf','r').readlines()
        IB = []
        for line in indat:
            IB.extend(line.strip().split())
        IB = np.array(IB).astype(float)
        self.ibound = IB.reshape(self.NROW,self.NCOL)

    def read_heads(self):
        hd = HeadFile(self.inroot + '.hds',platform = "Windows")
        hd.get_time(hd.totim)        
        self.heads = hd.head[0,:,:]
        self.heads[self.heads==999.]=np.nan
        del hd
        
    def read_recharge(self):
        indat = open(self.inroot + '.rch','r').readlines()
        
        i = 0
        for line in indat:
            if "RECHARGE" in line:
                break
            else:
                i+=1
        del(indat[0:i+1])

        self.rch = []
        for line in indat:
            self.rch.extend(line.strip().split())
        # read to the bottom of layer 1    
        self.rch = np.array(self.rch).astype(float)
        # reshape to model dimensions
        self.rch = self.rch.reshape(self.NROW,self.NCOL)
            
    def sweep_rows(self,strow,endrow):
        # set two indices to be the east and west ends of the island
        self.eastend=[]
        self.westend=[]
        for i in np.arange(strow-1,endrow):
            # pull the ibound model row cross section
            ibt = self.ibound[i]
            # find all the constant head cells
            neginds = np.nonzero(ibt < 0)[0]
            # get the diff to look for gaps
            dneginds = np.diff(neginds)
            
            # find all non constant head cells
            posinds = np.nonzero(ibt >= 0)[0]
            dposinds = np.diff(posinds)
            print i
            if (len(neginds) < 2):
                # if no constant head cells, set an exception flag  
                self.eastend.append(-999)
                self.westend.append(-999)
            else:
                # else set east end as first gap greater than ISLAND_MIN_WIDTH
                # and west as next gap greater than ISLAND_DISRUPTOR
                # ### DANGER! being clever here!!! ### #
                minwid = np.nonzero(dneginds >= self.ISLAND_MIN_WIDTH)[0]
                firstgap = np.nonzero(dposinds >= self.ISLAND_DISRUPTOR)[0]
                if (max(ibt) > 0):
                    self.eastend.append(neginds[minwid[-1]+1])
                    self.westend.append(posinds[firstgap[-2]]+dposinds[firstgap[-2]]-1)
                else:
                    self.eastend.append(-999)
                    self.westend.append(-999)                    
        self.westend = np.array(self.westend).astype(int)
        self.eastend = np.array(self.eastend).astype(int)
        ofp = open('testout.dat','w')
        for i, cw in enumerate(self.westend):
            ofp.write('%10d %10d\n' %(cw,self.eastend[i]))
        ofp.close()    
    def plotall(self):
        self.plotfield(self.heads,'HEADS')
        self.plotfield(self.ibound,'IBOUND')        
        self.plotfield(self.modtop,'modtop')
        self.plotfield(self.rch,'RECHARGE')
    
        
    def make_calcs(self,strow,endrow):
        self.island_width = []
        self.meanelev = []
        self.maxWT = []
        self.meanrch = []
        self.maxWTloc = []
        ofp = open('SEAWAT2NETICA.dat','w')
        ofp.write('%10s %16s %16s %16s %16s %16s %12s %12s %12\n' %('model_row',
                                                      'width',
                                                      'mean_elev',
                                                      'maxWT',
                                                      'mean_rch',
                                                      'max_WT_loc',
                                                      'west_index',
                                                      'east_index',
                                                      'max_WT_col')) 
           
        for i in np.arange(strow-1,endrow):
            if self.westend[i] < 0:
                self.island_width.append(-999)
                self.meanelev.append(-999)
                self.maxWT.append(-999)
                self.meanrch.append(-999)
                self.maxWTloc.append(-999)
            else:
                self.island_width.append((self.eastend[i] - self.westend[i] + 1)*50.0)
                self.meanelev.append(np.mean(self.modtop[i,self.westend[i]+1:self.eastend[i]]))
                tmpWT = self.heads[i,self.westend[i]+1:self.eastend[i]]
                self.maxWT.append(np.max(tmpWT))
                self.meanrch.append(np.mean(self.heads[i,self.westend[i]+1:self.eastend[i]]))
                maxWTind = np.nonzero(tmpWT==np.max(tmpWT))[0]
                self.maxWTloc.append((len(tmpWT)-maxWTind+1)*50)
                ofp.write('%10d %16.4f %16.4f %16.4f %16.4f %16.4f %12d %12d\n' %(i,
                                                                        self.island_width[i],
                                                                        self.meanelev[i],
                                                                        self.maxWT[i],
                                                                        self.meanrch[i],
                                                                        self.maxWTloc[i],
                                                                        self.westend[i],
                                                                        self.eastend[i])) 
        ofp.close()
        
            
    def noflow2nan(self):
        # simply make all no-flow cells equal to np.nan for cleaner plotting
        self.heads[self.ibound==0] = np.nan
        self.modtop[self.ibound==0] = np.nan
        self.rch[self.ibound==0] = np.nan
        self.ibound[self.ibound==0] = np.nan
        
##############################################
#################  M A I N  ################## 
##############################################
plotflag = False

# initialize --> 
ISLAND_MIN_WIDTH=2 # ### --> minimum number of contiguous island cells to make an island
ISLAND_DISTRUPTOR=3 # ## --> number of cells in a gap tha defines island 

mod1 = mod_res('gv12',ISLAND_MIN_WIDTH,ISLAND_DISTRUPTOR)
# read the top elevation and dimensionality
mod1.read_dis()
# read in IBOUND
mod1.read_IBOUND()
# read in the heads file
mod1.read_heads()
# read in the recharge
mod1.read_recharge()
# sweep through the rows
strow = 1
endrow = 1240
mod1.sweep_rows(strow,endrow)

# finally report the calculations
mod1.make_calcs(strow,endrow)

if plotflag:
    # nan the noflows --> but only for plotting
    mod1.noflow2nan()
    mod1.plotall()