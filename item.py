from ClassNet import ClassNet

class Item(ClassNet):

    itemName = "Dummy"
    itemStats = [0] * 7
    itemQuality = 0
    itemBuffs = 0
    itemClass = "DCL"
    ownerClass  = "DCL"

    def __init__(self):

        effectiveStats = self.findDisparity(itemClass,ownerClass)

    def setOwnerClass(self,oClass):
        self.ownerClass = oClass
        effectiveStats = self.findDisparity(itemClass,ownerClass)