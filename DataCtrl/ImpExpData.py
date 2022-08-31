import os, json, logging


# Logger Setup
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


#Class
class infoData():
    def __init__(self):
        super(infoData, self).__init__()
        """ IN/OUT Base Data """
        #Variables
        self.defaultDir = os.path.dirname(__file__)
        self.defaultLibPath = os.path.join(self.defaultDir, 'extList.json')
        
        self.dictExt = {}
    


    #####
    # Import Export Data CTRL saved
    #####
    def exportInfo(self, currentDict = {}):
        """write base data to file json"""
        self.dictExt = currentDict
        # debug
        
        with open(self.defaultLibPath, 'w') as outfile:
            json.dump(self.dictExt, outfile, indent=4)
        _logger.warning(f"Updated .ext Dictionary")
        

    def importInfo(self):
        """Upload CRTL from file json"""
        self.dictExt = {}
        try:
            self.dictExt = json.load(open(self.defaultLibPath, 'r'))
            _logger.warning(f"DICT from file json: {self.dictExt}")
            return self.dictExt
        except:
            _logger.error(f"No File json found")
            return self.dictExt


    def getPathFile(self):
        """ get path directory """
        return self.defaultDir