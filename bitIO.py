class BitWriter(object): 
    def __init__(self, f):
        self.accumulator = 0 
        self.bcount = 0 
        self.output = f 

    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
 
    def __del__(self):
        try:
            self.flush()
        except ValueError:  
            pass
 
    def close(self):
        self.flush()
        self.output.close()
        
    def writebit(self, bit):
        if self.bcount == 8:
            self.flush()
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount += 1
 
    def _writebits(self, bits, n):
        while n > 0:
            self.writebit(bits & 1 << n-1)
            n -= 1
 
    def writeint32bits(self, intvalue):
        self._writebits(intvalue, 32)

    def flush(self):
        if self.bcount: 
            self.output.write(bytearray([self.accumulator]))
            self.accumulator = 0
            self.bcount = 0
 
class BitReader(object): 
    def __init__(self, f):
        self.input = f 
        self.accumulator = 0 
        self.bcount = 0 
        self.read = 0 
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        self.input.close()
        
    def readsucces(self):
        return self.read
    
    def readbit(self):
        if not self.bcount: 
            a = self.input.read(1)
            if a: 
                self.accumulator = ord(a) 
            self.bcount = 8 
            self.read = len(a) 
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1 
        return rv
 
    def _readbits(self, n):
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v

    def readint32bits(self):
        return self._readbits(32)