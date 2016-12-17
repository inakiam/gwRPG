from math import log,ceil

class Stats(object):

    #Let's allow human-memorable setters and getters.
    nameMap = {'PHS':0,'RES':1,'INS':2,'INT':3,'PER':4,'EXS':5,'CLV':6,
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

    #Rebuff Vec + ALmighty Vec. Latter determines
    buffs = [0] * len(bStats) * 2
    almighty = [False] * len(bStats) * 2

    #Short and long-term non-innate buff vectors. Use short term for status fx
    #long term for item bonuses and/or weird permanent effects.
    #Format: [[buff,buffStatKey],...]. Ex: Buff ID + 1 = [1,7], or [1,'ID']
    
    stBuffs = []
    ltBuffs = []

    #Offset Modifier Vector. Gives a value for how much a Complex Base Stat can
    #grow before negative effects are invoked. Directly Modifiable.
    #Format: [PHS.realOffset,PHS.imagOffset,...CLS.realOffset, CLS.imagOffset]
    offset = [0] * len(bStats) * 2

    offset[7] = 4

    #TEST VALS REMOVE LATER
    bStats = [33+1j, 1+44444j, 1j+332552, 2j + 22249, 1j+11232, 1j+2, 1j+7**7]

    def __genSegs__(self):

        ds = self.dStats
        mod = len(ds) / 2

        segs = [[(-ds[i] / 2 + int(i/2)) %  mod, (ds[i] / 2 + int(i/2)) % mod]
                for i in range(len(ds))]
        segs = [segs[i] if ds[i] % 7 != 0 else (True if int(ds[i]) == 7
                                                else False)
                for i in range(len(segs))]
        return segs

    def __testSeg__(self,index,order,segs,curSeg):
        '''Recursive determiner.'''

        


    def __calcInnateBuffs__(self):

        segs = __genSegs__()

        for i in range(len(segs)):

            order = 0

            if segs[i]

            for item in segs:

                if type(item) is complex:

                    #Don't count self or opposing stat!
                    if item != segs[i] and item != segs[i-1 if i%2 == 1 else i+1]:

                        #run the segtest, which is in another function because
                        #recursion
                        __testSeg__(i,order,segs,item)
                        

                elif item: #if its bool/true

                    order += 1
                    self.buffs[i] += 1/(len(self.dStats) * self.dStats[i]

            if order >= 7:
                

                self.almighty[i] = True

        buffs = [item if item <= 3.5 else 3.5 for item in buffs

        

            
        
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
        self.dSDB = [(-log(self.bStatsFinal[int(i/2)].imag,7) if i % 2 == 0 else
                      -log(self.bStatsFinal[int(i/2)].real,7))/2
                     for i in range(len(self.dStats))]

    def __init__(self,cls=['Undefined,ERR']):

        if self.CLS[1] == 'ERR': self.CLS = cls

        self.__calcBaseFinal__()

        self.__calcDerivStats__()

        #self.__calcInnateBuffs__()

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


    def setSTBuff(self,buff):

        self.stBuffs += buff

    def setLTBuff(self,buff):

        self.ltBuffs += buff

    def remSTBuff(self,buff):
        self.stBuffs.remove(buff)

    def remLTBuff(self,buff):
        self.ltBuffs.remove(buff)

    def statUp(self,stat,incr):

        ''''stat is a numerical index corresponding to bStats or a string
            corresponding to a key in nameMap. incr is a real, imaginary, or
            complex int.'''

        if type(stat) is str: stat = nameMap[stat]

        self.bStats[stat] += incr

    def reportStat(self,base,index):

        if type(index) is str: index = self.nameMap[index]

        return self.bStats[index] if base else self.dStats[index]

    def reportBuff(self,base,index):

        if type(index) is str: index = nameMap[index]

        longterm = 0
        shortterm = 0

        for i in ltBuffs: longterm += i[0] if i[1] == index else 0
        for i in stBuffs: shortterm += i[0] if i[1] == index else 0

            

        return [self.dSDB[index],longterm,shorterm]

    def textReport(self):
        '''Write current into to stdout? Is that what we call what print does?'''
        nm = self.nameMap
        b = self.bStats
        d = self.dStats
        db = self.dSDB
        bf = self.bStatsFinal
        
        leKeys = ['PHS','RES','INS','INT','PER','EXS','CLV']
               
        seKeys = ['ST','SP','VT','IM','FL','WT','SM','ID',
               'IS','NS','AP','DS','CR','CI']

        bsR = [val + ": " + str(b[nm[val]]) + '\n' for val in leKeys]
        fbsR = [val + ": " + str(bf[nm[val]]) + '\n' for val in leKeys]
        dsR = [val + ": " + str(d[nm[val]]) + '\n' for val in seKeys]
        dbR = [val + ": " + str(db[nm[val]]) + '\n' for val in seKeys]
        
        print("-Base Stats-\n\n" + ''.join(bsR) + "\n-Final Base Stats-\n\n" +
              ''.join(fbsR) + "\n-Derived Stats-\n\n" + ''.join(dsR) +
              "\n-dStat Debuffs\n\n" + ''.join(dbR))

        
a = Stats(['Alpha Tester','ALP'])
a.textReport()
b = a.__genSegs__()
