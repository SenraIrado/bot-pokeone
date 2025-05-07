#Create simple GUI with pyqt5 and matplotlib
import sys
from operator import truediv

import matplotlib
from matplotlib import style
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

matplotlib.use('QtAgg')
style.use('ggplot')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Poke bot")
        self.setGeometry(100,100,800,600)
        self.move(60,15)

        plabel1 = QLabel("Pokemon Name:", self)
        plabel1.setGeometry(50, 25, 200, 30)
        self.pline1 = QLineEdit(self)
        self.pline1.setGeometry(50, 50, 200, 30)

        plabel2 = QLabel("Nature Name:", self)
        plabel2.setGeometry(50, 75, 200, 30)
        self.pline2 = QLineEdit(self)
        self.pline2.setGeometry(50, 100, 200, 30)

        bname = QPushButton("Save Name", self)
        bname.setCheckable(True)
        bname.clicked.connect(self.namecheck)
        bname.setGeometry(260, 50, 100, 30)

        bnature = QPushButton("Save Nature", self)
        bnature.setCheckable(True)
        bnature.clicked.connect(self.naturecheck)
        bnature.setGeometry(260, 100, 100, 30)

        bstart = QPushButton("Start", self)
        bstart.setCheckable(True)
        bstart.clicked.connect(self.startbot)
        bstart.setGeometry(50, 150, 100, 30)
     
        bstop = QPushButton("Stop", self)
        bstop.setCheckable(True)
        bstop.clicked.connect(self.stopbot)
        bstop.setGeometry(50, 200, 100, 30)
        
        bexit = QPushButton("Exit", self)
        bexit.setCheckable(True)
        bexit.clicked.connect(self.closebot)
        bexit.setGeometry(50, 250, 100, 30)

    
    
    def namecheck(self):
        pname = self.pline1.text()
        print("Name saved:", pname)
        return pname
    
    def naturecheck(self):
        pnature = self.pline2.text()
        print("Nature saved:", pnature)
        return pnature

    def startbot(self):
        print("Bot started")
        botting = True
        return botting
    def stopbot(self):
        print("Bot stopped")
        stop = True
        return stop
    def closebot(self):
        print("Bot closed")
        exit = True
        return exit

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()    #execute app
