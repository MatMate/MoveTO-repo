import os, sys, shutil, importlib

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import (
                            QApplication, 
                            QMainWindow, 
                            QLabel, 
                            QGridLayout, 
                            QVBoxLayout,
                            QWidget,
                            QLineEdit,
                            QComboBox,
                            QPushButton,
                            QFileDialog,
                            )
from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtGui import QPalette, QColor, QFont

"""from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *"""

#custom Imports
import DataCtrl.ImpExpData as ied
importlib.reload(ied)

def run():
    """Build UI
    """
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    

    try:
        #winMM.deleteLater()
        pass
    except NameError as e:
        pass
    
    winMM = FileManageUI()
    winMM.show()

    sys.exit(app.exec())

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class FileManageUI(QMainWindow): #Python2 QtGui.QDialog

    def __init__(self):
        super().__init__()

        #Variable
        #self.extList = ["txt", "mkv", "avi", "srt"]
        self.extCurrent = ""

        self.currentPath = ""

        self.listPathToMove = []

        #generate class for collecting data
        dataCls = ied.infoData()
        dictT = dataCls.importInfo()
        self.extList = dictT["extFile"]
        #dataCls.exportInfo(dictT)

        #Window Settings
        self.setWindowTitle("File Manage UI by MatMate")
        self.setFixedSize(QSize(350, 100))

        #Global Container
        self.mainVertLyt = QVBoxLayout()
        self.mainVertLyt.setContentsMargins(5, 5, 5, 5)
        #self.mainVertLyt.setSpacing(20)

        #Main body
        self.secGridLyt = QGridLayout()

        #Widgets
        self.titleLab = QLabel()
        self.pathFoulderEdLine = QLineEdit()
        self.extFileCBox = QComboBox()
        self.searchFoulderBtn = QPushButton()
        self.moveFileBtn = QPushButton()


        #Widgets to Layout
        #Title
        self.mainVertLyt.addWidget(self.titleLab)
        self.secGridLyt.addWidget(self.pathFoulderEdLine,0,0,1,1)
        self.secGridLyt.addWidget(self.searchFoulderBtn,0,1,1,1)
        self.secGridLyt.addWidget(self.extFileCBox,1,0,1,1)
        self.secGridLyt.addWidget(self.moveFileBtn,1,1,1,1)

        
        self.mainVertLyt.addLayout(self.secGridLyt)        

        #init Widget
        self.initWidget()
        self.connectWidget()
        

        #Execute Methods
        self.extComboBoxBody(comboBox = self.extFileCBox, extList = self.extList)

        
        widget = QWidget()
        widget.setLayout(self.mainVertLyt)
        self.setCentralWidget(widget)

    def initWidget(self):
        #title
        self.titleLab.setText("Find the .ext file \nin the entered path \nmove it to a unique folder")
        #self.titleLab.setStyleSheet("color: rgb(119, 136, 153);")
        self.titleLab.setStyleSheet("color: DimGrey;")
        font = QFont()
        font.setFamily(u"Verdana")
        font.setBold(True)
        font.setPointSize(8)
        self.titleLab.setFont(font)
        self.titleLab.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #self.titleLab = QLabel("Find .ext file \n in the path inserted")
        self.pathFoulderEdLine.setPlaceholderText("paste Path")
        #self.extFileCBox = QComboBox()

        self.moveFileBtn.setEnabled(False)
        self.moveFileBtn.setStyleSheet("color: rgb(250, 0, 0);")
        self.moveFileBtn.setGeometry(QRect(50, 100, 192, 28))
        self.moveFileBtn.setText("Move Files")

        self.searchFoulderBtn.setText("Browse")
        self.searchFoulderBtn.setStyleSheet("color: rgb(250, 250, 250);"
                                            "background-color: rgb(0, 0, 150);")


    def extComboBoxBody(self, comboBox = QComboBox, extList = []):

        for item in extList:
            comboBox.addItem(f"{item}")

    def connectWidget(self):       
        self.pathFoulderEdLine.textChanged.connect(self.pathInputTextChan)
        self.extFileCBox.currentIndexChanged.connect(self.extCBoxCom)
        #Combo Box called by button OK
        self.moveFileBtn.pressed.connect(self.moveFileComBut)
        self.searchFoulderBtn.pressed.connect(self.searchFoulderComBut)


    #####
    # Button Command
    #####

    def searchFoulderComBut(self):
        #fName = QFileDialog.getOpenFileName(self, "Search Foulder To Examinate", "D:")
        fPath = QFileDialog.getExistingDirectory(self, "Search Foulder To Examinate")
        #fName = QFileDialog.getExistingDirectoryUrl(self, "Search Foulder To Examinate")

        self.pathFoulderEdLine.setText(fPath)

        print(f"File: {fPath}")

    def moveFileComBut(self):
        self.checkMovieFile(self.currentPath)

        
        if len(self.listPathToMove) is not 0:
            self.moveFileTo()
        else:
            _logger.error(f"No File Found with: {self.extCurrent}")

        
        print("File Moved")


    def pathInputTextChan(self, text = ""):
        #check necessary for keyboard input
        if os.path.isdir(text):
            print(f"Valid Path: {text}")
            self.currentPath = text
            self.moveFileBtn.setEnabled(True)
            self.moveFileBtn.setStyleSheet("color: green;")

        else:
            print("No valid path found")
            self.moveFileBtn.setEnabled(False)
            self.moveFileBtn.setStyleSheet("color: red;")

    def extCBoxCom(self, index = 0):       
        self.extCurrent = self.extFileCBox.itemText(index)
        
        print(self.extCurrent)



    #####
    # Run methods
    #####

    def checkFileType(self, pathToExi = None, listToExi = None):
        """ create a list with all the file found """
        
        _logger.debug(f"inside check 2: {listToExi}")

        
        for file in listToExi:
            if f"{self.extCurrent}Destination" not in file:
                pathCurrentFile = os.path.join(pathToExi, file)
                if os.path.isdir(pathCurrentFile):
                    self.checkMovieFile(pathCurrentFile)            
                else:
                    if f".{self.extCurrent}" in file:
                        self.listPathToMove.append(pathCurrentFile)
                        _logger.warning(f"This File is the one: {pathCurrentFile}")
                    else:
                        _logger.debug(f"This file is not the one: {file}")
        
        

        



    def checkMovieFile(self, pathToExi = None):
        """ Ric create a list with all the file found """
        fileInFoulder = os.listdir(pathToExi)
        _logger.debug(f"inside check 1 {pathToExi}")

        self.checkFileType(pathToExi = pathToExi, listToExi = fileInFoulder)




    def moveFileTo(self):
        """move files in list to dest """
        _logger.warning(f"List File: {self.listPathToMove}")
        pathDest = os.path.join(self.currentPath, f"{self.extCurrent}Destination")
        if not os.path.exists(pathDest):
            os.mkdir(pathDest)
        for pathFile in self.listPathToMove:
            shutil.move(pathFile, pathDest)
        self.listPathToMove.clear()



run()
