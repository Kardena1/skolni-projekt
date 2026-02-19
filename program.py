import os
import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,QComboBox,QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIntValidator



script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   
    
app = QApplication(sys.argv)
app.setStyle("Fusion")

class hlavni_okno(QWidget):
    def __init__ (self):
        super().__init__()

        self.setWindowTitle("Kalkulacka")
        self.setFixedSize(500,500)
        self.setStyleSheet("""
                           
        QPushButton {
            font-size: 18px;
            # background-color: #000000;
        }

        """)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignTop)


        #TLACITKA -------------------------------------

        self.combo = QComboBox()
        with open('data.json','r',encoding='UTF-8') as f:
            data = json.load(f)
            seznam_nazvu = [m["nazev"] for m in data["material"]]
            self.combo.addItems(seznam_nazvu)
        
        self.button = QtWidgets.QPushButton("Pridat material")
        self.pole_napis = QtWidgets.QLabel("Material")
        self.energie_napis = QtWidgets.QLabel("Vstupni energie")
        self.vaha_napis = QtWidgets.QLabel("Vaha")
        self.poc_tepl_napis = QtWidgets.QLabel("Pocatecni teplota")
        self.debug1_napis = QtWidgets.QLabel("Vykonat")

        self.energie = QtWidgets.QLineEdit()
        self.vaha = QtWidgets.QLineEdit()
        self.poc_tepl = QtWidgets.QLineEdit()
        self.debug1 = QtWidgets.QPushButton("Debug")
        # eventy
        self.debug1.clicked.connect(self.debugs)
        self.button.clicked.connect(self.test)



        #layout
        layout.addWidget(self.pole_napis, 0,0)
        layout.addWidget(self.energie_napis,0,1)
        layout.addWidget(self.vaha_napis,0,2)
        layout.addWidget(self.poc_tepl_napis,0,3)
        layout.addWidget(self.debug1_napis,0,4)
        
        layout.addWidget(self.combo,1,0)
        layout.addWidget(self.energie,1,1)
        layout.addWidget(self.vaha,1,2)
        layout.addWidget(self.poc_tepl,1,3)
        layout.addWidget(self.debug1,1,4)

        layout.addWidget(self.button,3,4)








        # ----------------------------------------------

    def test(self):
        self.pridani_materialu_okno = pridani_materialu()
        self.pridani_materialu_okno.show()

        
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


class pridani_materialu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pridani materialu")
        self.setFixedSize(750,100)
        self.setStyleSheet("""
        QPushButton {
            font-size: 18px;
            #background-color: #f0f0f0;
        }
        QLineEdit {
            background-color: #000000;
            color: #ffffff;
            margin-top: 25px;
        }
        """)



        layout = QGridLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignCenter)


        validator = QIntValidator()


        self.nazev_napis = QtWidgets.QLabel("Nazev")
        self.t_tani_napis = QtWidgets.QLabel("Bod tání (°C)")
        self.t_varu_napis = QtWidgets.QLabel("Bod varu (°C)")
        self.c_pevne_napis = QtWidgets.QLabel("Měrná tepelná kapacita - pevné skupenství (J/kg°C)")
        self.c_kapalina_napis = QtWidgets.QLabel("Měrná tepelná kapacita - kapalné skupenství (J/kg°C)")
        self.l_tani_napis = QtWidgets.QLabel("Měrné skupenské teplo tání (J/kg)")
        self.l_varu_napis = QtWidgets.QLabel("Měrné skupenské teplo varu (J/kg)")


        self.nazev = QtWidgets.QLineEdit()
        self.t_tani = QtWidgets.QLineEdit()
        self.t_varu = QtWidgets.QLineEdit()
        self.c_pevne = QtWidgets.QLineEdit()
        self.c_kapalina = QtWidgets.QLineEdit()
        self.l_tani = QtWidgets.QLineEdit()
        self.l_varu = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("Přidat")
        self.test = QtWidgets.QPushButton("Test")


        layout.addWidget(self.nazev_napis,0,0)
        layout.addWidget(self.t_tani_napis,0,1)
        layout.addWidget(self.t_varu_napis,0,2)
        layout.addWidget(self.c_pevne_napis,0,3)
        layout.addWidget(self.c_kapalina_napis,0,4)
        layout.addWidget(self.l_tani_napis,0,5)
        layout.addWidget(self.l_varu_napis,0,6)

        layout.addWidget(self.nazev,1,0)   
        layout.addWidget(self.t_tani,1,1)
        layout.addWidget(self.t_varu,1,2)
        layout.addWidget(self.c_pevne,1,3)
        layout.addWidget(self.c_kapalina,1,4)
        layout.addWidget(self.l_tani,1,5)
        layout.addWidget(self.l_varu,1,6) 
        layout.addWidget(self.test,2,5)
        layout.addWidget(self.button,2,6)


        self.button.clicked.connect(self.pridani_materialu)
        self.test.clicked.connect(self.ukaz_upozorneni)


    def pridani_materialu(self):
        # nazev = input("Zadej název materiálu: ")
        # t_tani = float(input("Zadej bod tání (°C): "))
        # t_varu = float(input("Zadej bod varu (°C): "))
        # c_pevne = float(input("Zadej měrnou tepelnou kapacitu - pevné skupenství (J/kg°C): "))
        # c_kapalina = float(input("Zadej měrnou tepelnou kapacitu - kapalné skupenství (J/kg°C): "))
        # l_tani = float(input("Zadej měrné skupenské teplo tání (J/kg): "))
        # l_varu = float(input("Zadej měrné skupenské teplo varu (J/kg): "))
        novy_material = {
            "nazev": self.nazev.text(),
            "bod_tani": self.t_tani.text(),
            "bod_varu": self.t_varu.text(),
            "tepelna_kapacita_pevne": self.c_pevne.text(),
            "tepelna_kapacita_kapalina": self.c_kapalina.text(),
            "skupenske_teplo_tani": self.l_tani.text(),
            "skupenske_teplo_varu": self.l_varu.text()
        }
        data["material"].append(novy_material)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # ulozeni zpet do souboru 


    def ukaz_upozorneni(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Informace")
        msg.setText("Material byl úspěšně přidán.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()





okno_hlavni = hlavni_okno()
okno_hlavni.show()
sys.exit(app.exec())



























# Funkce
