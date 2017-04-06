from math import log,ceil
from random import random
from ClassNet import ClassNet

class Stats(ClassNet):
    #Class name and Abbrevs?
    CLS = ['UNDEFINED','UND']
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
    offset = [3.5] * len(bStats) * 2


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
    bStats = [33+1j, 1+44444j, 1j+332552, 1j + 22249, 1j+11232, 1j+2, 1j+7**7]
    bStats = [7**7 + 1j] * 7

    bStats = [49+1j] * 2 + [1+1j]*5


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

                #print(bStats[i],lRe,lIm,baseDiffs,effectiveOffsets,offset,nStat)

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


    def __buildDiffs__(self,segs,statRange):
        '''Builds a list of line segments from another list. New list is
           non-overlapping while containing an additional term that
           records how many segments overlapped there on original.'''

        overlaps = 1

        # #rewrite segs so all segments obey s[0] < s[1]
        # for item in segs:
        #
        #     if item[0] > item[1]:
        #
        #         segs.remove(item)
        #         segs += [0,item[1]]
        #         segs += [item[0],7]

        for i in segs:

            if i[0] > i[1]:

                #If statRange subsumed
                if i[1] > statRange[1] or i[0] < statRange[0]:

                    segs[segs.index(i)] = statRange.copy()

                elif i[1] < statRange[0] or i[0] > statRange[1]: #If outside the range

                    segs.remove(i)
            #If no overlap, and normal segment
            elif not((i[0] <= statRange[1]) or (i[1] >= statRange[0])):

                segs.remove(i)


        #purge repetitive elements
        for i in segs:

            totalCover = i == statRange
            overlaps += 1 if totalCover else 0
            if totalCover: segs.remove(i)


        leftSides = [i[0] for i in segs if statRange[0] < i[0] < statRange[1]]
        rightSides =[i[1] for i in segs if statRange[1] > i[1] > statRange[0]]

        #no seg with a left side < statRange[0] should have survived.
        leftEdge = statRange[0]
        diffs = []

        iterLen = len(leftSides) + len(rightSides)

        for i in range(iterLen):

            minL = min(leftSides) if len(leftSides) > 0 else statRange[1] + 1
            minR = min(rightSides) if len(rightSides) > 0 else statRange[1] + 1
            minT = min(minL,minR)

            #is n of overlaps increasing or decreasing at edge? False = increasing
            inDec = minT == minL

            #purge element
            if inDec: leftSides.remove(minT)
            else: rightSides.remove(minT)

            #add new segment
            if i == 0:
                diffs += [[statRange[0], minT, overlaps]]

            if i == iterLen - 1:
                diffs += [[minT, statRange[1], overlaps + inDec]]

            else:
                diffs += [[leftEdge, minT, overlaps]]

            #if segment is right edge, increment overlap of current
            # segment by 1
            if not(inDec):
                for i in range(len(diffs) - 1):
                    diffs[i][2] += 1
                overlaps -= 1

            else: overlaps += 1

            leftEdge = minT

        #if EVERY FUCKING THING IS SEVENS
        if overlaps > 0 and diffs == []:
            diffs += [[statRange[0],statRange[1],overlaps]]

        #this math problem is now solved in the stupidest way
        #possible, we're quite sure.
        return diffs


    def __calcBuffs__(self):
        '''Calculates innate buffs by translating them into line segments in
           mod 7 (assuming baseling setup) space and adding 1/numDStats the
           length. If more than seven stats overlap, doubles buff.'''

        mod = len(self.bStats)

        for statIndex in range(len(self.dStats)):

            stat = self.dStats[statIndex]

            overlaps = 0
            total = stat

            statCentre = int(statIndex / 2)

            statRange = [(statCentre - stat/2),
                         (statCentre + stat/2)]

            #determine how much to shift the range to ensure that the stat
            #doesn't spill over boundaries. This eliminates a significant amount
            #of ifthen logic downstream by making the problem invariant.
            #this trick only works if the modulus of the space >= maxval of stat
            if statRange[0] < 0: displace = statRange[0] * -1
            elif statRange[1] > mod: displace = mod - statRange[1]
            else: displace = 0

            statRange = [(item + displace) % mod for item in statRange]

            statInv = statRange[0] < statRange[1]

            #Those stats not related to the one under consideration...
            temp = self.dStats[:statCentre] + self.dStats[statCentre + 2:]
            temp = [item for item in temp if item != 0]


            #make vectors of start and endpoints
            leftSides = [(int(self.dStats.index(line) / 2) - line/2 + displace)
                         % mod for line in temp]
            rightSides = [(int(self.dStats.index(line) / 2) + line/2 + displace)
                         % mod for line in temp]

            segs = [[leftSides[i],rightSides[i]] for i in range(len(temp))]
            print(segs)
            diffs = self.__buildDiffs__(segs,statRange)
            print(diffs)
            isAlmighty = False
            for diff in diffs:

                total += (diff[1] - diff[0]) *  diff[2] / (len(self.dStats) * 2)

                if diff[2] >= 6: isAlmighty = True

            diffIndex = statIndex + 1 if statIndex % 2 == 0 else statIndex - 1
            self.buffs[diffIndex] = total
            self.almighty[diffIndex] = isAlmighty




    def __calcDerivFinal__(self):

        remoBuffs = self.stBuffs + self.ltBuffs

        for i in range(len(self.dStats)):

            self.dStatsFinal += [self.dStats[i] + self.dSDB[i] + self.buffs[i]]

            if self.almighty[i]: self.dStatsFinal[i] += self.buffs[i]

        for item in remoBuffs:

            self.dStatsFinal[remoBuffs[1]] += remoBuffs[0]





    def __init__(self,cls=['Undefined,ERR']):

        if self.CLS[1] == 'ERR':
            print("YOU. ARE. DOING. IT. WRONG.")

        else:
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

        disparity = [1/item for item in self.findDisparity(self.CLS[1],
                                                           newclass)]

        self.CLS = [self.disparaDB[newclass][-2],newclass]

        self.offset = [self.offset[i]/disparity[i] for i in
                        range(len(self.offset))]

        tempDStats = [self.bStats[int(i/2)].real if i % 2 == 0 else
                      self.bStats[int(i/2)].imag for i in range(len(self.dStats
                      ))]

        tempDStats = [log(tempDStats[i],7)/disparity[i] for i in
                      range(len(tempDStats))]

        #if we're actually doing a class down, prevents stats greater than 7
        tempDStats = [item if item <= 7 else 7 for item in tempDStats]

        self.bStats = [round(7**tempDStats[i*2]) + round(7**tempDStats[i*2 + 1])
                       * 1j for i in range(len(self.bStats))]



    def __validBuff__(self,buff):

        assert (type(buff[0]) is int) or (type(buff[0]) is float)
        assert (type(buff[1]) is int) and (0 <= buff[1] <= len(self.dStats) - 1)

    def setSTBuff(self,buff):

        __validBuff__(buff)

        self.stBuffs += buff

    def setLTBuff(self,buff):

        __validBuff__(buff)

        self.ltBuffs += buff

    def remSTBuff(self,buff):

        __validBuff__(buff)

        self.stBuffs.remove(buff)

    def remLTBuff(self,buff):

        __validBuff__(buff)

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


a = Stats(['Zero','ZRO'])
#a.textReport()
#print(a.buffs,a.almighty)
print(a.dStats,a.buffs,a.almighty,a.dStatsFinal)
