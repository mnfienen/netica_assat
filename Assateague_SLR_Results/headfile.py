'''
Created on Sep 23, 2010

@author: langevin
'''

import numpy
import struct
from reader import binary


class HeadFile:
    """HeadFile class for working with a MODFLOW head file.
    
    Presently written for Intel-created binary files only.
    
    """
    
    def __init__(self,name,form='binary', order='lrc', precision='single', platform='windows'):
        """Initialize the MODFLOW head file.
        
        Open the file and assign the appropriate reader type.  
        
        """
        self.name = name
        self.form = form
        self.order = order
        self.platform = platform
        #Open the file and assign the appropriate file reading class.
        if form == 'binary':
            self.file = open(self.name,'rb')
            self.reader = binary(self.file, precision=precision)
        else:
            self.file = open(self.name,'rb')
            self.reader = ascii(self.file)
        #Create an index of the records in a binary head file
        if form == 'binary':
            self.headerbyte=(5 * self.reader.integerbyte + #kstp,kper,ncol,nrow,ilay
                             2 * self.reader.realbyte    + #pertim,totim
                             16 * self.reader.textbyte)    #text
            if self.platform.lower() == 'linux':
                self.headerbyte += 2 * self.reader.integerbyte
            self.build_index()
           #mnf debug self.print_index()
        #allocate space for 3D head array

        if order == 'lrc':
            self.head=numpy.empty((self.nlay,self.nrow,self.ncol))
        else:
            self.head=numpy.empty((self.nrow,self.ncol,self.nlay))

    def read_header(self):
        """ Read the header from a MODFLOW binary file.
        
        Uses the binary or ascii reader classes assigned to self.reader.
    
        """
        verbose=True
        try:
            if self.platform.lower() == 'linux':
                junkus = self.reader.read_integer()
                if(verbose): print 'junkus ' + str(junkus)
            self.kstp = self.reader.read_integer()
            if(verbose): print 'kstp ' + str(self.kstp)
            
        except:
            if(verbose): print 'Error reading header value for kstp.'
            return False
        try:
            self.kper = self.reader.read_integer()
            if(verbose): print 'kper ' + str(self.kper)
        except:
            if(verbose): print 'Error reading header value for kper.'
            return False
        try:
            self.pertim = self.reader.read_real()
            if(verbose): print 'pertim ' + str(self.pertim)
        except:
            if(verbose): print 'Error reading header value for pertim.'
            return False
        try:
            self.totim  = self.reader.read_real()
            if(verbose): print 'totim ' + str(self.totim)
        except:
            if(verbose): print 'Error reading header value for totim.'
            return False
        try:
            self.text   = self.reader.read_text()
            if(verbose): print 'text ' + str(self.text)
        except:
            if(verbose): print 'Error reading header value for text.'
            return False
        try:
            self.ncol   = self.reader.read_integer()
            if(verbose): print 'ncol ' + str(self.ncol)
            
        except:
            if(verbose): print 'Error reading header value for ncol.'
            return False
        try:
            self.nrow   = self.reader.read_integer()
            if(verbose): print 'nrow ' + str(self.nrow)
        except:
            if(verbose): print 'Error reading header value for nrow.'
            return False
        try:
            self.ilay   = self.reader.read_integer()
            if(verbose): print 'ilay ' + str(self.ilay)

            if self.platform.lower() == 'linux':
                junkus = self.reader.read_integer()
                if(verbose): print 'junkus ' + str(junkus)
        except:
            if(verbose): print 'Error reading header value for ilay.'
            return False
        return True

    def print_header(self):
        """ Print the header information to the screen.
        
        Simple method to print the header information stored in the 
        Headfile Class.
    
        """
        print 'kstp  : '+str(self.kstp)
        print 'kper  : '+str(self.kper)
        print 'pertim: '+str(self.pertim)
        print 'totim : '+str(self.totim)
        print 'text  : '+self.text
        print 'ncol  : '+str(self.ncol)
        print 'nrow  : '+str(self.nrow)
        print 'ilay  : '+str(self.ilay)
        return

    def build_index(self):
        """ Create an index of head records in the binary file.
        
        Read through a binary head file and index the records.  This function
        creates the following class entries:  
        
            HeadFile.kstpkperdict is a dictionary.
                key = kstpkper is str(kstp)+' '+str(kper)
                D[key] = byteposition of kstpkper in the binary file
                e.g. Headfile.kstpkperdict = {'1 1' : 0 , '1 2' : 4564L}

            HeadFile.totimdict is a dictionary.
                key = totim
                D[key] = byteposition of totim in the binary file
                e.g. Headfile.totimdict = {1.0 : 0 , 2.0 : 4564L}
                
            nlay is the maximum value of ilay encountered in the file.
            
            time is a tuple of times encountered in the file.
    
        """
        print 'Building index of records in ' + self.name + '...'
        self.kstpkperdict = {}
        self.totimdict = {}
        self.time = ([])
        recnum = 0
        self.nlay = 0
        while(True):
            #store present position
            position = self.file.tell()
            #get header information
            success = self.read_header()

            #skip through a 2D real array number of bytes
            nbytes = self.reader.realbyte*self.ncol*self.nrow
            if self.platform.lower() == 'linux':
                nbytes += 2 * self.reader.integerbyte
            self.file.seek(nbytes, 1)
            if not success: 
                break
            if self.ilay == 1:
                recnum = recnum+1
                kstpkper = str(self.kstp) + ' ' + str(self.kper)
                self.kstpkperdict[kstpkper] = position
                self.totimdict[self.totim] = position
                self.time.append(self.totim)
            if self.nlay < self.ilay:
                self.nlay = self.ilay
        #reposition to beginning of file
        self.file.seek(0,0)
        return
        
    def print_index(self):
        print 'Summary of records in: ',self.name
        record = 1
        for t in self.time:
            print 'Record: ',record, 'is for time: ',t
            record += 1
        return
        
    def __iter__(self):
        return self

    def next(self):
        for k in range(self.nlay):
            success = self.read_header()
            if not success:
                raise StopIteration
                return self
            if self.order == 'lrc':
                self.head[self.ilay - 1, :, :] = (
                    self.reader.read_2drealarray(self.nrow,self.ncol))
            else:
                self.head[:, :, self.ilay - 1] = (
                    self.reader.read_2drealarray(self.nrow,self.ncol))
                
        line = 'Successful head read [totim:' + str(self.totim) + '].' 
        print line
        return self
    
    def get_kstpkper(self,kstp,kper):
        """Jump ahead to the specified time step and stress period
        and read the 3D head array.
        """
        position = self.kstpkperdict[str(kstp) + ' ' + str(kper)]
        self.file.seek(0,0)
        if(kstp > 0 or kper > 0):
            self.file.seek(position, 0)
        self.next()
        return
        
    def get_time(self,time):
        """Jump ahead to the specified time
        and read the 3D head array.
        """
        try:
            record=self.time.index(time)
        except:
            print 'Error.  Time not found in file.'
            return
        position = self.totimdict[time]
        self.file.seek(position, 0)
        self.next()
        return            


