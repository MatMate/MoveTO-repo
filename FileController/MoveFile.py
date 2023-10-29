

class FileController():
    def __init__(self, FolderPath = None, extType = None):
        
        #Variables
        self.FolderPath = FolderPath
        self.extType = extType

        #Variable in
        self.listPathToMove = []

    