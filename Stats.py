from math import log,ceil

class Stats(object):

    #Let's allow human-memorable setters and getters.
    nameMap = {'PHS':0,'RES':1,'INS':2,'INT':3,'PER':4,'EXS':5,'CLS':6,
               'ST':0,'SP':1,'VT':2,'IM':3,'FL':4,'WT':5,'SM':6,'ID':7,
               'IS':8,'NS':9,'AP':10,'DS':11,'CR':12,'CI':13}

    #Base Stats Vector. See above.
    bStats = [1+1j] * 7

    #Class name and Abbrevs?
    CLS = ['UNDEFINED','ERR']

    #Postcalc Base Stats.
    bStatsFinal = []

    #Derived Stats Vector. What's abctually used in calculation for ease of code
    dStats = [0] * len(bStats) * 2


    #Debuffs Vector. Needs to be separate so calculating debuff removal doesn't
    #alter the stats under consideration.
    dSDB = [0] * len(bStats) * 2

    #Short and long-term non-innate buff vectors. Use short term for status fx
    #long term for item bonuses and/or weird permanent effects.
    #Format: [[buff,buffStatKey],...]. Ex: Buff ID + 1 = [1,7], or [1,'ID']
    
    stBuffs = []
    ltBuffs = []

    #Offset Modifier Vector. Gives a value for how much a Complex Base Stat can
    #grow before negative effects are invoked. Directly Modifiable.
    #Format: [PHS.realOffset,PHS.imagOffset,...CLS.realOffset, CLS.imagOffset]
    offset = [0] * len(bStats) * 2



    def __buildSegments__(self):

        return []


    def __dbRemove__(self):

        norms = self.dStats
        norms = [[0 - val/2, 0 + val/2] for val in norms]

        positions = [[self.offset[i] + int(i/2), self.offset[i] + int(i/2)]
                     for i in range(14)]
        
        norms = [(norms[i] + positions[i]) % 7 for i in range(14)]

        

        #Stores all overlaps in format [[mainRange],[mainRange]...]
        #[mainrange] = [rangeStart,rangeEnd,principleOne,principleTwo]
        overlapIndex = []

        #start and end points for the ranges
        sePoints = []

        for i in range(len(self.dStats)):
            break

            
        
    def __calcBaseFinal__(self):

        bStats = self.bStats
        offset = self.offset

        #Reset bStatsFinal vec
        self.bStatsFinal = [0] * len(bStats)

        for i in range(len(bStats)):

            if (bStats[i].real  > 1) and (bStats[i].imag > 1):

                lRe = log(bStats[i].real,7)
                lIm = log(bStats[i].imag,7)
                baseDiffs = complex(max(lRe-lIm,0),max(lIm-lRe,0))
                effectiveOffsets = complex(min(offset[i*2+1],lIm),
                                           min(offset[i*2],lRe))
                
                nStat = baseDiffs + effectiveOffsets

                print(bStats[i],lRe,lIm,baseDiffs,effectiveOffsets,offset,nStat)
                
                self.bStatsFinal[i] += complex(7**nStat.real,7**nStat.imag)

            else: self.bStatsFinal[i] += bStats[i]
    

    def __calcDerivStats__(self):
        '''Calculates derived stats.'''

        #Build base deriv stats
        self.dStats = [log(self.bStatsFinal[int(i/2)].real,7) if i % 2 == 0 else
                       log(self.bStatsFinal[int(i/2)].imag,7) for i in range(len(
                           self.dStats))]

        #Build debuff vec
        self.dSDB = [(-log(self.bStatsFinal[int(i/2)].real,7) if i % 2 == 0 else
                      -log(self.bStatsFinal[int(i/2)].imag,7))/2
                     for i in range(len(self.dStats))]

    def __init__(self,cls):

        self.CLS = cls

        self.bStats = [33+1j, 1+44444j, 1j+332552, 2j + 22249, 1j+11232, 1j+2, 1j+7**7]

        self.__calcBaseFinal__()

        self.__calcDerivStats__()

        #self.__caclFinalBuffs__()

    def classUp(self,newclass):

        '''Class promotion method.
           newclass = [clasName,statAbrev,modifiers]'''
        #modifiers is either a scalar, or a len(self.offsets) vector.

        #Overall procedure: scale offsets by how much stronger or weaker new
        #class is. Then calculate a naive dStats vector, scale *that*, and
        #reconstruct the bStats

        self.CLS = newclass[:2]

        #if the new class only has a scalar modifier relative to the old...
        #and really, this should absolutely never be the case.
        mods = [newclass[3]] * len(self.offsets) if type(newclass[3])\
               is int else newclass[3]
        
        self.offsets = [self.offsets[i]/mods[i] for i in
                        range(len(self.offsets))]

        tempDStats = [self.bStats[int(i/2)].real if i % 2 == 0 else
                      self.bStats[int(i/2)].imag for i in range(len(self.dStats
                                                                    ))]
        tempDStats = [log(tempDStats[i],7)/mods[i] for i in
                      range(len(tempDStats))]

        self.bStats = [round(7**tempDStats[i*2]) + round(7**tempDStats[i*2 + 1])
                       * 1j for i in range(len(self.bStats))]

        

        

        
        

        
a = Stats(['Alpha Tester','ALP'])
