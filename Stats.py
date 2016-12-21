from math import log,ceil

class Stats(object):

    #Class name and Abbrevs?
    CLS = ['UNDEFINED','ERR']
    #^^Migrate to actual class class; stats only really needs a multvec for
    #upgrades

    #Let's allow human-memorable setters and getters.
    nameMap = {'PHS':0,'RES':1,'INS':2,'INT':3,'PER':4,'EXS':5,'CLV':6,
               'ST':0,'SP':1,'VT':2,'IM':3,'FL':4,'WT':5,'SM':6,'ID':7,
               'IS':8,'NS':9,'AP':10,'DS':11,'CR':12,'CI':13}

    #Base Stats Vector. Settable. Max val of each part: 7**7.
    bStats = [1+1j] * 7

    #Postcalc Base Stats. This stores stats after nullification.
    bStatsFinal = []

    #Offset Modifier Vector. Gives a value for how much a Complex Base Stat can
    #grow before negative effects are invoked. Directly Modifiable.
    #Format: [PHS.realOffset,PHS.imagOffset,...CLS.realOffset, CLS.imagOffset]
    offset = [0] * len(bStats) * 2

    
    #Derived Stats Vector. Calculated from bStatsFinal.
    dStats = [0] * len(bStats) * 2

    #Holds postbuff dStats for reduced computation.
    dStatsFinal = []


    #Debuffs Vector. Needs to be separate so calculating debuff removal doesn't
    #alter the stats under consideration. Calculated from bStats
    dSDB = [0] * len(bStats) * 2

    #Rebuff Vec. Determines how much of cross-stat debuff is negated by overlaps
    #Calculated from dStats.
    buffs = [0] * len(bStats) * 2

    #Almighty Vec. Used to determine if the buff gets multiplied by
    #2, or not. True = it does. Set to True when overlap of 7 unrelated stats.
    almighty = [False] * len(bStats) * 2


    #Short and long-term non-innate buff vectors. Settable.
    #Use short term for status fx, long term for item bonuses and/or
    #weird permanent effects.
    #Format: [[buff,buffStatKey],...]. Ex: Buff ID + 1 = [1,7], or [1,'ID']
    stBuffs = []
    ltBuffs = []

    
    #TEST VALS REMOVE LATER
    offset[7] = 4
    #bStats = [33+1j, 1+44444j, 1j+332552, 2j + 22249, 1j+11232, 1j+2, 1j+7**7]
    bStats = [7**6 + 1j] * 7

##    def __genSegs__(self):
##        '''Generate line segments from dStats.'''
##
##        ds = self.dStats
##        mod = len(ds) / 2
##
##        segs = [[(-ds[i] / 2 + int(i/2)) %  mod, (ds[i] / 2 + int(i/2)) % mod]
##                for i in range(len(ds))]
##        segs = [segs[i] if ds[i] % 7 != 0 else (True if int(ds[i]) == 7
##                                                else False)
##                for i in range(len(segs))]
##        return segs
##
##    def __calcBuffs__(self):
##
##        lBs = len(self.bStats) - 1
##
##        for i in self.dStats:
##
##            dsI = self.dStats.index(i)
##
##            #where the item is centered
##            pos = int(dsI/2)
##
##            #what it's edge is...
##            edge = i/2
##
##            #stats in dStats that aren't i or its counterpart
##            testStats = self.dStats[:pos*2] + self.dStats[pos*2 + 2:]
##
##            #how many things are overlapping
##            order = 1
##
##            diffSum = i
##
##            for j in testStats:
##
##                
##                
##                jPos = int(testStats.index(j)/2)
##                jEdge = j/2
##
##                iLef = (pos - edge) % lBs
##                iRig = (pos + edge) % lBS
##                jLef = (jPos - jEdge) % lBs
##                jRig = (jPos + jEdge) % lBs
##
##                
##
##                diffs = [iRig - jLef,jLef - iRig,
##
##                #test if coverage is total.
##                perfect = ((pos - edge) % lBs > (jPos - jEdge) % lBs) or\
##                          ((pos + edge) % lBs < (jPos + jEdge) % lBs)
##
##                #test if there is coverage, period
##                partial = ((pos + edge) > (jPos - jEdge)) or\
##                          ((pos - edge) < (jPos + jEdge)) 
##
##                if perfect or j == 7:
##
##                    diffs = [i]
##                    order += 1
##                    
##
##                elif partial:
##
##                    iEdgeOver = (pos - edge) % lBs < (pos + edge) % lBs
##                    jEdgeOver = (jPos - jEdge) % lBs < (jPos + jEdge) % lBs
##
##                    diffs = [(pos + edge) - (jPos - jEdge),
##                             (pos - edge) - (jPos + jEdge)]
##
##                    if iEdgeOver or jEdgeOver:
##
##                        flipped = [pos - edge != (pos - edge) % lBs,
##                                   pos + edge != (pos + edge) % lBs]
##
##                            
##                        diffs = [(pos - edge) % 7 - min(7,jPos+jEdge) if flipped[0] else diffs[0],
##                                 (pos + edge) % 7 - max(0,jPos-jEdge) if flipped[1] else diffs[1]]
##                            
##
##                    
##                        flipped = [jPos - jEdge != (jPos - jEdge) % lBs,
##                                    jPos + jEdge != (jPos + jEdge) % lBs]
##
##                        order += 1
##
##
##                #Discard negative values, which indicate no overlap.
##                diffSum += sum([val for val in diffs if val >= 0])
##                    
##
##            if order >= 7:
##
##                self.almighty[dsI + 1 if dsI % 2 == 0 else dsI - 1] = True
##
##            self.buffs[dsI + 1 if dsI % 2 == 0 else dsI - 1] = diffSum / (lBs * 2)
##
##                
##
##
##            
##
##        accumulator = 0
##
##        valRltL = #right side of region exceeds leftmost of curSeg
##        valLgtR = #left side reightmost
##        perfect = #if dStat = 7.0
##        null = #if dStat = 0
##
##        
##
##        if (valRltL or valLgtR) or perfect:
##
##            accumulator += rVal - lVal /len(self.dStats)
##            if unique(
##            
##
##        elif null: pass
##
##        else:
##
##            #code to determine number and what it gets subtracted from here.
##            #basically, it's smaller from larger.
##
##            diff = [val1,val2]
##            diff.sort()
##
##            accumulator +=
##
##        self.buffs[i+1 if blah else i-1] += accumulator
##
##        
##
##    def __testSeg__(self,index,order,segs,curSeg):
##        '''Figures out overlaps'''
##
##        bsL = len(self.bStats)
##
##        #Derestrict modular space. Prrrrobably should just kill modulus upstream
##        leftOff = curSeg[0] if curSeg[0] > curSeg[1] else curSeg[0] - bsL
##
##        eq = leftOff != curSeg[0]
##        
##        rightOff = curSeg[1] if curSeg[1] < curSeg[0] and eq else curSeg[1] + bsL
##
##        curSeg = [leftOff,rightOff] 
##
##        #prune self and shadow.
##        nInd = int(index/2) * 2
##        relSegs = segs[:nInd] + segs[nInd + 2:]
##
##        #kill bools
##        relSegs = [val for val in relSegs if type(val) != bool]
##        
##
##        #segments overlapping from left
##        olS = [curSeg[0]]
##
##        #from right
##        orS = [curSeg[1]]
##
##        #print(relSegs)
##
##        #Sort everything into overlaps that cross from the left of curSeg and
##        #those coming from the right.
##        for lens in relSegs:
##
##            lLeftOff = lens[0] if lens[0] > lens[1] else lens[0] - bsL
##
##            eq = lLeftOff != lens[0]
##            
##            lRightOff = lens[1] if lens[1] < lens[0] and eq else lens[1] + bsL
##        
##            centre = (lLeftOff + lRightOff)/2
##            
##
##            ineqs = [curSeg[0] < lRightOff < curSeg[1],
##                     curSeg[0] < lLeftOff < curSeg[1]]
##
##            if ineqs[0]:
##                olS += [lRightOff]
##
##            if ineqs[1]:
##                orS += [lLeftOff]
##                
##            #increase reported order of overlap.
##            if ineqs[0] or ineqs[1]: order += 1
##
##        #large-to-small val sort for iterative convenience.
##        olS.sort(reverse = True)
##        orS.sort(reverse = True)
##
##        #this needs to be put into an internal function, and made recursive.
##        diffsL =[(olS[i] - olS[i+1]) * (len(olS) - 1 - i) / (bsL * 2)
##                 for i in range(len(olS) - 1)]
##        diffsR =[(orS[i] - orS[i+1]) *  i / (bsL * 2) 
##                 for i in range(len(orS) - 1)]
##
##        self.buffs[index] += sum(diffsL) + sum(diffsR)
##
##        #Return order of region  because why the fuck
##        return order
##
##        
##
##
##    def __calcInnateBuffs__(self):
##
##        segs = self.__genSegs__()
##
##        for i in range(len(segs)):
##
##            order = 0
##
##
##            if type(segs[i]) is list:
##                #run the segtest, which is in another function because
##                #recursion
##                order = self.__testSeg__(i,order,segs,segs[i])
##                    
##
##            elif (type(segs[i]) is bool) and segs[i]: #if its bool/true
##
##                order += 1
##                self.buffs[i] += 1/len(self.dStats) * self.dStats[i]
##
##            if order >= 7:
##                
##                self.almighty[i] = True
##
##        #self.buffs = [item if item <= 3.5 else 3.5 for item in self.buffs]

        

            
        
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

    def __calcDerivFinal__(self):

        remoBuffs = self.stBuffs + self.ltBuffs

        for i in range(len(self.dStats)):

            self.dStatsFinal += [self.dStats[i] + self.dSDB[i] + self.buffs[i]]

            if self.almighty[i]: self.dStatsFinal[i] += self.buffs[i]

        for item in remoBuffs:

            self.dStatsFinal[remoBuffs[1]] += remoBuffs[0]

            

        

    def __init__(self,cls=['Undefined,ERR']):

        if self.CLS[1] == 'ERR': self.CLS = cls

        self.__calcBaseFinal__()

        self.__calcDerivStats__()

        self.__calcBuffs__()

        self.__calcDerivFinal__()

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
