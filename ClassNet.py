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

    def __loadClassFromFile(self):

        

    def __init__(self):

        disparaDB += [0, None, [1]*14, "Default Class", "DCL"]
        self.__loadClassFromFile()__

    def registerClass(self):

        
