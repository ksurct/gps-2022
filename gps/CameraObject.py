
class CameraObject():
    
    def __init__(self, objectId, color, x, width):
        self.objectId = objectId
        self.color = color
        self.x = x
        self.width = width
        
    def getColor(self):
        return self.color
        
    def __repr__(self):
        return "id:%s color:%s x:%s width:%s" % (self.objectId, self.color, self.x, self.width)
