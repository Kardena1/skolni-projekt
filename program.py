import os
import sys
import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QComboBox


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

class hlavni_okno(QWidget):
    def __init__ (self):
        super().__init__()

        self.setWindowTitle("Kalkulacka")
        self.setFixedSize(500,500)
        self.setStyleSheet("""
        QPushButton {
            font-size: 18px;
            background-color: #f0f0f0;
        }
        QLineEdit {
            background-color: #ffffff
        }
        """)


        layout = QGridLayout()
        self.setLayout(layout)


        #TLACITKA -------------------------------------

        self.combo = QComboBox()
        with open('data.json','r',encoding='UTF-8') as f:
            data = json.load(f)
            seznam_nazvu = [m["nazev"] for m in data["material"]]
            self.combo.addItems(seznam_nazvu)

        self.energie = QtWidgets.QLineEdit()
        self.vaha = QtWidgets.QLineEdit()
        self.poc_tepl = QtWidgets.QLineEdit()
        self.debug1 = QtWidgets.QPushButton("Debug")
        # eventy
        self.debug1.clicked.connect(self.debugs)



        #layout
        layout.addWidget(self.combo,0,0)
        layout.addWidget(self.energie,0,1)
        layout.addWidget(self.vaha,0,2)
        layout.addWidget(self.poc_tepl,0,3)
        layout.addWidget(self.debug1,0,4)


        # ----------------------------------------------


    def pridani_materialu(self):
        nazev = input("Zadej nazev materialu: ")
        bod_tani = int(input("Zadej bod tani: "))
        bod_varu = int(input("Zadej bod varu: "))
        merna_kapacita = int(input("Zadejte mernou kapacitu"))
        novy_material = {
            "nazev": nazev,
            "bod_tani": bod_tani,
            "bod_varu": bod_varu,
            "merna_kapacita": merna_kapacita
        }
        data["material"].append(novy_material)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # ulozeni zpet do souboru 
        
    def vypsat_materialy(self):
        for i, material in enumerate(data["material"], start=1):
            print(f"{i}. Material:", material["nazev"], "Bod tani:", material["bod_tani"],"°C", "Bod varu:", material["bod_varu"],"°C","\n") # vypsat materialy s jejich atributy

    def debugs(self):

        index = self.combo.currentIndex()
        vybrany_material = data["material"][index]
        tani = vybrany_material["bod_tani"]
        varu = vybrany_material["bod_varu"]
        kapacita = vybrany_material["merna_kapacita"]

        vysl = tani - varu

        print(f" Nazev materialu: {vybrany_material["nazev"]}\n Bod tani: {tani}\n Bod varu: {varu}\n Merna kapacita: {kapacita}\n Testovy vysledek: {vysl}\n Zadana energie: {self.energie.text()}\n Zadana vaha: {self.vaha.text()}\n Zadana teplota: {self.poc_tepl.text()}\n")





app = QApplication(sys.argv)
okno = hlavni_okno()
okno.show()
sys.exit(app.exec())



























# Funkce
