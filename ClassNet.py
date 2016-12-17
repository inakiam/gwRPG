class ClassNet(object):

    '''the network of all classes that records the multipliers between classes. and applies them
       if no disparity is registered, it attempts to find one algorithmically'''

    #Fundamental Format: [classHierarchy,parent,[multvec], longName, shortName]
    #class Hierarchy starts at one - zero for the Default Class
    #parent is the longName for the class the Class comes from.
    #multvec is a vector of floats, which record how much stronger or weaker
    #a class is cmpared to its parent. the mVec of Default is all 1's
    #longName is the full name of the class - eg, "Zero"
    #shortName is a three-letter abbreviation - eg, "ZRO"
    
    #Disparity Database. Matrix of classVecs.
    disparaDB = []

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

        self.disparaDB += [0, None, [1]*14, "Default Class", "DCL"]
        print(self.__loadClassFromFile__())

    def __findRoute__(self, firstClass, secondClass):
        pass

    def findDisparity(self, firstClass, secondClass):

        #Find the two classes, saving the route to each.
        #Then, using one class, multiply down the tree to default
        #from default, divide up the tree
        #naturally, the dirparity of the destination class when it's acting
        #on the origin. Invert for origin-dest, and for fucks sake memoise it
        #actually, better idea - save that shit to file

        pass

        

    def registerClass(self,playerClass=''):
        
        if type(playerClass) is list: self.disparaDB += [playerClass]

a = ClassNet()
        
