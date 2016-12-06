from math import log
from math import ceil

class Stats(object):

    #Base Stats. Directly Modifiable.
    PHS = 1+1j
    RES = 1+1j
    INS = 1+1j
    INT = 1+1j
    PER = 1+1j
    EXS = 1+1j

    #Class Stat. Directly Modifiable.
    CLS = [1+1j,'Default', 'DEF']

    #Offset Modifier Vector. Gives a value for how much a Complex Base Stat can
    #grow before negative effects are invoked. Directly Modifiable.
    #Format: [PHS.realOffset,PHS.imagOffset,...CLS.realOffset, CLS.imagOffset]
    offset = [0] * 14

    #Derived Stats. Calculated from Base.
    ST = 0
    SP = 0
    FL = 0
    WT = 0
    SM = 0
    ID = 0
    VT = 0
    IM = 0
    IS = 0
    NS = 0
    AP = 0
    DS = 0
    CR = 0
    CI = 0

    #Derived Stats Vector. What's abctually used in calculation for ease of code
    dStats = [0] * 14

    #Base Stats Vector. See above.
    bStats = [0] * 14

##    def __calcDebuffs__(self):
##
##        old = self.dStats.copy()
##        new = [-old[i]/2 for i in rand(len(old))]
##
##        for i in range(len(old)):
##
##            magnitude = int(old[i])
##            count = 0
##
##            for j in range((-magnitude + i) % len(old),(magnitude + i) % len(old):
##
##                if 
##
##                new[i] += len(old)**-1 * 

            
        

        

    def __calcStats__(self):
        '''Calculates derived stats.'''

        self.bStats = [self.PHS,self.RES,self.INS,self.INT,self.PER,self.EXS,
                  self.CLS[0]]
        

        #This aborted of list comprehension calculates the derived stats...

        for i in range(len(self.dStats)):

            bSt = [float(self.bStats[int(i/2)].real),
                   float(self.bStats[int(i/2)].imag)]

            #log of stat currently being calculated, and it's opposing piece.
            lbStat = log(bSt[i%2], 7)
            loStat = log(bSt[(i+1)%2], 7)

            #Determine real-imag degredation...
            anaceptVal = max(loStat - self.offset[i], 0)

            self.dStats[i] = lbStat - anaceptVal

        #Finally, determine growth debuffs.
        #self.__calcDebuffs__()    


        self.ST,self.SP,self.FL,self.WT,self.SM,self.ID,self.VT,self.IM, \
        self.IS,self.NS,self.AP,self.DS,self.CR,self.CI = self.dStats        
        

    def __init__(self,cls):

        self.CLS = [self.CLS[0],cls[0],cls[1]]

        self.PHS += 33
        self.RES += 44444j
        self.INS += 332552
        self.INT += 4j + 22249
        self.PER += 11232
        self.EXS += 2

        self.__calcStats__()

    def setPHS(self,phs):

        self.PHS += complex(phs)
        

        
a = Stats(['Alpha Tester','ALP'])
a.setPHS(7)
print(a.ST)
a.setPHS(7+7j)
print(a.ST)
