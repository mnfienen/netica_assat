'''
Created on Jul 21, 2010

@author: langevin
'''

import numpy
import struct

def getvarfromline(line, index, type, varname='', filename=''):
    """Parse a value from a character string.
      line:     the character string
      index:    the index of the value within the string
      type:     the type of variable to return ('int', 'float', or 'str').
      varname:  the name of the variable to be read (for error message).
      filename: the name of the filename that line comes from (for error 
                message).
    
    """
    try:
        value = line.split()[index]
    except:
        msg = ('Error trying to parse a value from line:' + '\n' +
               line + '\n' +
               'at index: ' + str(index) + '\n' )
        if varname <> '':
            msg = msg + 'for input variable: ' + varname + '\n'
        if filename <> '':
            msg = msg + 'from file: ' + filename + '\n'
        print msg
    if type == 'int':
        value = int(value)
    if type == 'float':
        value = float(value)
    return value


def readarray(file, n):
    """Return a tuple containing n float values read from an ascii 
    file.  This will read a MODFLOW-style array as long as there is
    whitespace separating the values.
    
    """
    a=([])
    while (True):
        line=file.readline()
        for i in line.strip().split():
            a.append(float(i))
            if len(a) == n:
                break
        if len(a) == n:
            break
    return a

def readintarray(file, n):
    """Return a tuple containing n integer values read from an ascii 
    file.  This will read a MODFLOW-style array as long as there is
    whitespace separating the values.
    
    """
    a=([])
    while (True):
        line=file.readline()
        for i in line.strip().split():
            a.append(int(i))
            if len(a) == n:
                break
        if len(a) == n:
            break
    return a

def u2drel(nrow, ncol, infile, filedict=None):
    """Return a two dimensional real array.
    
    Only works for new word-style array headers.
    Not yet programmed to read binary data.
    
    If the array may be contained in an external file, then a file dictionary
    should be passed into this subroutine, where:
        filedict = file dictionary
        key = unit number
        filedict[key] = file name
        
    If a file dictionary is not passed in, then external unit numbers are assumed
    to point to this file (infile).
    
    """
    control = infile.readline()
    print control
    if 'CONSTANT' in control.upper():
        constant = float(control.strip().split()[1])
        a = numpy.ones(nrow * ncol)
        a = a * constant
    elif 'INTERNAL' in control.upper():
        t = readarray(infile, nrow * ncol)
        constant = float(control.strip().split()[1])
        a = numpy.array(t) * constant
    elif 'OPEN/CLOSE' in control.upper():
        filename = control.strip().split()[1]
        constant = float(control.strip().split()[2])
        ifl = open(filename,'r')
        t = readarray(infile, nrow * ncol)
        a = numpy.array(t) * constant
        close(ifl)
    elif 'EXTERNAL' in control.upper():
        nunit = int(control.strip().split()[1])
        constant = float(control.strip().split()[2])
        fmtin = control.strip().split()[3]
        if filedict == None:
            f = infile
        else:
            try:
                f = filedict[nunit]
            except:
                print 'Error finding EXTERNAL array.'
                return
        t = readarray(f, nrow * ncol)
        a = numpy.array(t) * constant
    else:
        #read old-style array header
        locat = int(control[0:10])
        constant = float(control[10:20])
        fmtin = control[20:40]
        if locat == 0:
            a = numpy.ones(nrow * ncol)
            a = a * constant
        elif locat > 0:
            if filedict == None:
                f = infile
            else:
                try:
                    f = filedict[locat]
                except:
                    print 'Error finding file associated with LOCAT.'
                    return
            t = readarray(f, nrow * ncol)
            a = numpy.array(t) * constant
        elif locat < 0:
            #not programmed yet for binary files
            pass
    a.shape=(nrow,ncol)
    return a


def u2dint(nrow, ncol, infile, filedict=None):
    """Return a two dimensional integer array.
    
    Only works for new word-style array headers.
    Not yet programmed to read binary data.
    
    If the array may be contained in an external file, then a file dictionary
    should be passed into this subroutine, where:
        filedict = file dictionary
        key = unit number
        filedict[key] = file name
        
    If a file dictionary is not passed in, then external unit numbers are assumed
    to point to this file (infile).
    
    """
    control = infile.readline()
    print control
    if 'CONSTANT' in control.upper():
        constant = int(control.strip().split()[1])
        a = numpy.ones(nrow * ncol)
        a = a * constant
    elif 'INTERNAL' in control.upper():
        t = readarray(infile, nrow * ncol)
        constant = int(control.strip().split()[1])
        a = numpy.array(t) * constant
    elif 'OPEN/CLOSE' in control.upper():
        filename = control.strip().split()[1]
        constant = int(control.strip().split()[2])
        ifl = open(filename,'r')
        t = readarray(infile, nrow * ncol)
        a = numpy.array(t) * constant
        close(ifl)
    elif 'EXTERNAL' in control.upper():
        nunit = int(control.strip().split()[1])
        constant = int(control.strip().split()[2])
        fmtin = control.strip().split()[3]
        if filedict == None:
            f = infile
        else:
            try:
                f = filedict[nunit]
            except:
                print 'Error finding EXTERNAL array.'
                return
        t = readarray(f, nrow * ncol)
        a = numpy.array(t) * constant
    else:
        #read old-style array header
        locat = int(control[0:10])
        constant = int(control[10:20])
        fmtin = control[20:40]
        if locat == 0:
            a = numpy.ones(nrow * ncol)
            a = a * constant
        elif locat > 0:
            if filedict == None:
                f = infile
            else:
                try:
                    f = filedict[locat]
                except:
                    print 'Error finding file associated with LOCAT.'
                    return
            t = readarray(f, nrow * ncol)
            a = numpy.array(t) * constant
        elif locat < 0:
            #not programmed yet for binary files
            pass
    a.shape=(nrow,ncol)
    return a


def u1drel(ncol, infile, filedict=None):
    """Return a one dimensional real array.
    
    Only works for new word-style array headers.
    Not yet programmed to read binary data.
    
    If the array may be contained in an external file, then a file dictionary
    should be passed into this subroutine, where:
        filedict = file dictionary
        key = unit number
        filedict[key] = file name
        
    If a file dictionary is not passed in, then external unit numbers are assumed
    to point to this file (infile).
    
    """
    control = infile.readline()
    print control
    if 'CONSTANT' in control.upper():
        constant = float(control.strip().split()[1])
        a = numpy.ones(ncol)
        a = a * constant
    elif 'INTERNAL' in control.upper():
        t = readarray(infile, ncol)
        constant = float(control.strip().split()[1])
        a = numpy.array(t) * constant
    elif 'OPEN/CLOSE' in control.upper():
        filename = control.strip().split()[1]
        constant = float(control.strip().split()[2])
        ifl = open(filename,'r')
        t = readarray(infile, ncol)
        a = numpy.array(t) * constant
        close(ifl)
    elif 'EXTERNAL' in control.upper():
        nunit = int(control.strip().split()[1])
        constant = float(control.strip().split()[2])
        fmtin = control.strip().split()[3]
        if filedict == None:
            f = infile
        else:
            try:
                f = filedict[nunit]
            except:
                print 'Error finding EXTERNAL array.'
                return
        t = readarray(f, ncol)
        a = numpy.array(t) * constant
    else:
        #read old-style array header
        locat = int(control[0:10])
        constant = float(control[10:20])
        fmtin = control[20:40]
        if locat == 0:
            a = numpy.ones(ncol)
            a = a * constant
        elif locat > 0:
            if filedict == None:
                f = infile
            else:
                try:
                    f = filedict[locat]
                except:
                    print 'Error finding file associated with LOCAT.'
                    return
            t = readarray(f, ncol)
            a = numpy.array(t) * constant
        elif locat < 0:
            #not programmed yet for binary files
            pass
    return a


def ijk_from_icrl(icrl,nlay,nrow,ncol):
    'Convert the modflow node number to row, column, and layer.'
    k=int( icrl / nrow / ncol )+1
    i=int( (icrl-(k-1)*nrow*ncol) / ncol )+1
    j=icrl - (k-1)*nrow*ncol - (i-1)*ncol
    return i,j,k

class binary():
    """Methods for reading and writing binary files.
    
    Only contains reading methods so far. File must already be open
        and positioned at desired read location.
    
    """
    
    def __init__(self, file, precision='single'):
        """Define byte structure for variable types
        
        Default precision type is single.  
        
        """
        self.file = file
        self.integer = numpy.int32
        self.integerbyte = 4
        self.character = numpy.uint8
        self.textbyte = 1
        if precision == 'single':
            self.real = numpy.float32
            self.realbyte = 4
            self.fmt = 'f'
        else:
            self.real = numpy.float64
            self.realbyte = 8
            self.fmt = 'd'
        self.byteposition = 0
        return

    def read_integer(self):
        """Read a single binary integer value."""
        intvalue = struct.unpack('i', self.file.read(1 * self.integerbyte))[0]
        self.byteposition = self.byteposition + 1 * self.integerbyte
        return intvalue

    def read_real(self):
        """Read a single binary real value."""
        realvalue = struct.unpack(self.fmt, self.file.read(1*self.realbyte))[0]
        self.byteposition = self.byteposition+1 * self.realbyte
        return realvalue

    def read_text(self):
        """Read a single binary text value."""
        #textvalue=struct.unpack('cccccccccccccccc', 
        #                        self.file.read(16*self.textbyte))
        textvalue = numpy.fromfile(file=self.file, dtype=self.character, 
                                 count=16).tostring()
        self.byteposition = self.byteposition+16 * self.textbyte
        return textvalue
    
    def read_3drealarray(self,nlay,nrow,ncol):
        """Read a three dimensional binary real array."""
        x = numpy.fromfile(file=self.file, dtype=self.real, 
                         count=nlay * nrow * ncol)
        x.shape = (nlay, nrow, ncol)
        return x

    def read_2drealarray(self,nrow,ncol):
        """Read a two dimensional binary real array."""
        x = numpy.fromfile(file=self.file, dtype=self.real, 
                         count=nrow * ncol)
        x.shape = (nrow, ncol)
        return x

    def read_1drealarray(self,ncol):
        """Read a one dimensional binary real array."""
        x = numpy.fromfile(file=self.file, dtype=self.real, 
                         count=ncol)
        x.shape = (ncol)
        return x

    def read_2dintegerarray(self,nrow,ncol):
        """Read a two dimensional binary integer array."""
        i = numpy.fromfile(file=self.file, dtype=self.integer, 
                         count=nrow * ncol)
        i.shape = (nrow, ncol)
        return i

class ascii():
    """Methods for reading and writing ascii files.
    
    Class not created yet.
    
    """
    
    def __init__(self,file):
        print 'need to implement'
        pass

    def read_integer(self):
        print 'need to implement'
        pass

    def read_real(self):
        print 'need to implement'
        pass

    def read_text(self):
        print 'need to implement'
        pass
    
    def read_3drealarray(self):
        print 'need to implement'
        pass

    def read_2drealarray(self):
        print 'need to implement'
        pass

    def read_2dintegerarray(self):
        print 'need to implement'
        pass
