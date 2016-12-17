class ClassNet(object):

    '''the network of all classes that records the multipliers between classes. and applies them
       if no disparity is registered, it attempts to find one algorithmically'''

    #Fundamental Format: [parent,[multvec], longName, shortName]
    #parent is the longName for the class the Class comes from.
    #multvec is a vector of floats, which record how much stronger or weaker
    #a class is cmpared to its parent. the mVec of Default is all 1's
    #longName is the full name of the class - eg, "Zero"
    #shortName is a three-letter abbreviation - eg, "ZRO"
    
    #Disparity Database. Matrix of classVecs.
    disparaDB = {}

    #Traceback memo. Contains ClassName-Keyset Pairs. Removes need for recursive
    #search whenever disparities need to be found.

    def __loadClassFromFile__(self):

        try: file = open("rsc/ClassNet.ini",'r')
        except:
            print("Error: ClassNet.ini is missing. What the fuck?")
            return -1

        curLine = file.readline()

        while curLine != '':

            curLine = curLine[:len(curLine) - 1] if curLine[-1] != ']' else\
                      curLine

            if (curLine != '') and (curLine[0] != '#'):

                self.registerClass(eval(curLine))

            curLine = file.readline()

        file.close()

    def __init__(self):

        self.disparaDB["DCL"] = [None, [1]*14, "Default Class", "DCL"]
        self.__loadClassFromFile__()

    def findDisparity(self, firstClass, secondClass):

        cont = True

        routes = [[],[]]

        while firstClass != "DCL" and secondClass != "DCL":

            if firstClass != "DCL":
                routes[0] += [self.disparaDB[firstClass][1]]
                firstClass = self.disparaDB[firstClass][0]
                
            if secondClass != "DCL":

                routes[1] += [self.disparaDB[secondClass][1]]
                secondClass = self.disparaDB[secondClass][0]

        def product(multList):

            transpose = [i for i in zip(*multList)]

            out = [1] * len(multList[0])

            for item in range(len(transpose)):
                for num in transpose[item]:

                    out[item] *= num

            return out

        rOP = product(routes[0])
        rTP = product(routes[1])

        return [rOP[i]/rTP[i] for i in range(len(rOP))]
        

    def registerClass(self,playerClass=''):
        
        if type(playerClass) is list:
            self.disparaDB[playerClass[-1]] = playerClass

a = ClassNet()
b = a.findDisparity("BRK","GTL")
