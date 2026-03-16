import os



import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,QComboBox,QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIntValidator, QPixmap,QIcon,QRegularExpressionValidator
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt,QSize


app = QApplication(sys.argv)
app.setStyle("Fusion")

class hlavni_okno(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fyzikální Kalkulačka Materiálů")
        self.setFixedSize(600, 650) 
        self.setStyleSheet("""
            QWidget { background-color: #FFDD99; color: #000000; font-family: 'Segoe UI', sans-serif; }
            QGroupBox { 
                font-weight: bold; border: 2px solid #D18B00; 
                margin-top: 1.5em; border-radius: 5px; padding: 10px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
            QPushButton {
                background-color: #FFAA00; border-radius: 8px; font-weight: bold; min-height: 35px;
            }
            QPushButton:hover { background-color: #FFC04D; }
            QLineEdit { background-color: #ffffff; border: 1px solid #D18B00; border-radius: 4px; padding: 5px; min-height: 30px; }
            QComboBox { background-color: #D18B00; border-radius: 4px; padding: 5px; }
            QLabel { font-size: 13px; }               
        """)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)

        mat_group = QtWidgets.QGroupBox("Vyber materialu")
        mat_layout = QtWidgets.QHBoxLayout()

        self.test1 = QtWidgets.QLineEdit()
        self.test2 = QtWidgets.QLabel("sd")
        self.test3 = QtWidgets.QPushButton("wda")

        mat_layout.addWidget(self.test2) 
        mat_layout.addWidget(self.test1,2)   
        mat_layout.addWidget(self.test3,1)
        mat_group.setLayout(mat_layout)
        main_layout.addWidget(mat_group)
        
        main_layout.addStretch()

        mat_grid = QtWidgets.QGridLayout()

        self.t1 = QtWidgets.QPushButton("Dwa")
        self.t2 = QtWidgets.QPushButton("wdad")
        self.t3 = QtWidgets.QPushButton("dwa")
        self.t4 = QtWidgets.QPushButton("dw")
        self.t5 = QtWidgets.QPushButton("test")
        self.t6 = QtWidgets.QPushButton("dff")
        self.t7 = QtWidgets.QPushButton("2e")
        self.t8 = QtWidgets.QPushButton("65")

        mat_grid.addWidget(self.t1, 0,0)
        mat_grid.addWidget(self.t2,0,1)
        mat_grid.addWidget(self.t3,0,2)
        mat_grid.addWidget(self.t4,0,3)
        mat_grid.addWidget(self.t5,1,0)
        mat_grid.addWidget(self.t6,1,1)
        mat_grid.addWidget(self.t7,1,2)
        mat_grid.addWidget(self.t8,1,3)

        main_layout.addLayout(mat_grid)
        main_layout.addStretch(4)

        qvlayout = QtWidgets.QHBoxLayout()
        qvlayout.setAlignment(QtCore.Qt.AlignCenter)

        self.t11 = QtWidgets.QPushButton("Dwa")
        self.t12 = QtWidgets.QPushButton("wdad")
        self.t13 = QtWidgets.QPushButton("dwa")
        self.t14 = QtWidgets.QPushButton("dw")
        self.t15 = QtWidgets.QPushButton("test")
        self.t16 = QtWidgets.QPushButton("dff")
        self.t17 = QtWidgets.QPushButton("2e")
        self.t18 = QtWidgets.QPushButton("65")

        self.t11.setFixedWidth(200)
        self.t12.setFixedWidth(200)
        qvlayout.addWidget(self.t11)
        qvlayout.addWidget(self.t12)



        
        main_layout.addLayout(qvlayout)










hlavni_ok = hlavni_okno()
hlavni_ok.show()
sys.exit(app.exec())