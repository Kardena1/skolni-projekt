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
                margin-top: 1.1em; border-radius: 5px; padding: 10px;
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



        mat_layout.addLayout


hlavni_ok = hlavni_okno()
hlavni_ok.show()
sys.exit(app.exec())