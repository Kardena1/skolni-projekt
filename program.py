import os
import sys
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,QComboBox,QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIntValidator, QPixmap,QIcon,QRegularExpressionValidator
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt,QSize



script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
import logika

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
        QWidget {
            background-color: #FFDD99;
            color: #000000;
                           }                  
        QPushButton {
            font-size: 17px;
            background-color: #FFAA00;
            color: #000000;
            border-radius: 10px;   
            border-color: #000000;
            min-width: 105px;
            min-height: 40px;                                                     
        }
        QLineEdit {
            background-color: #FFAA00;
            color: #000000;
            margin-top: 0px;
            min-height: 40px;
            font-size: 17px; 
            min-width: 60px;
                                                   
        }
        QComboBox {
            background-color: #D18B00;
            color: #000000;  
            min-height: 40px;
            font-size: 17px;                                        
        }
        QMessageBox {
            background-color: #FFDD99;
            color: #000000;
        }
                           
                        
        """)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignTop)
        regex = QRegularExpression(r"^[0-9]*\.?[0-9]*$")
        validator = QRegularExpressionValidator(regex)


        #TLACITKA -------------------------------------

        self.combo = QComboBox()
        with open('data.json','r',encoding='UTF-8') as f:
            data = json.load(f)
            seznam_nazvu = [m["nazev"] for m in data["material"]]
            self.combo.addItems(seznam_nazvu)


        
        self.button = QtWidgets.QPushButton("Sprava Mat.")
        self.pole_napis = QtWidgets.QLabel("Material")
        self.energie_napis = QtWidgets.QLabel("Vstupni energie")
        self.vaha_napis = QtWidgets.QLabel("Vaha        ")
        self.poc_tepl_napis = QtWidgets.QLabel("Pocatecni teplota")
        self.debug1_napis = QtWidgets.QLabel("Vykonat")

        self.energie = QtWidgets.QLineEdit()
        self.vaha = QtWidgets.QLineEdit()
        self.poc_tepl = QtWidgets.QLineEdit()
        self.debug1 = QtWidgets.QPushButton("Vypocitat")
        layout.setRowStretch(2, 1)

        self.energie.setPlaceholderText("J")
        self.poc_tepl.setPlaceholderText("°C")
        self.vaha.setPlaceholderText("Kg")

        self.poc_tepl.setObjectName("poc_tepl")



        self.energie.setValidator(validator)
        self.vaha.setValidator(validator)
        self.poc_tepl.setValidator(validator)
        # eventy

        self.combo.currentIndexChanged.connect(self.zobrazit_info)
        self.debug1.clicked.connect(self.vypocitat)
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

        layout.addWidget(self.button,3,4, QtCore.Qt.AlignBottom)








        # ----------------------------------------------

    def test(self):
        self.pridani_materialu_okno = pridani_materialu(self)
        self.pridani_materialu_okno.show()

    def zobrazit_info(self):
        index = self.combo.currentIndex()

        data1 = data["material"][index]

        nazev = data1["nazev"]
        bod_tani = float(data1['bod_tani'])
        bod_varu = float(data1['bod_varu'])
        tep_kap_pev = float(data1['tepelna_kapacita_pevne'])
        tep_kap_kapal = float(data1['tepelna_kapacita_kapalina'])
        skup_tani = float(data1['skupenske_teplo_tani'])
        skup_varu = float(data1['skupenske_teplo_varu'])

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Informace")
        msg.setText(f"Název materiálu: {nazev}\nBod tání: {bod_tani} °C\nBod varu: {bod_varu} °C\nTepelná kapacita pevné skupenství: {tep_kap_pev} J/kg°C\nTepelná kapacita kapalné skupenství: {tep_kap_kapal} J/kg°C\nSkupenské teplo tání: {skup_tani} J/kg\nSkupenské teplo varu: {skup_varu} J/kg")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        




    def vypsat_materialy(self):
        for i, material in enumerate(data["material"], start=1):
            print(f"{i}. Material:", material["nazev"], "Bod tani:", material["bod_tani"],"°C", "Bod varu:", material["bod_varu"],"°C","\n") # vypsat materialy s jejich atributy


    def vypocitat(self):
        try: 
            index = self.combo.currentIndex()
            vybrany_material = data["material"][index]

            teplota, skupenstvi = logika.vypocitat_a(vybrany_material,self.energie.text(),self.vaha.text(),self.poc_tepl.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Výsledek")
            msg.setText(f"Výsledná teplota: {teplota} °C\nSkupenství: {skupenstvi}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Chyba")
            msg.setText("Zadejte platné číselné hodnoty pro energii, váhu a počáteční teplotu.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        




    # def debugs(self):

    #     index = self.combo.currentIndex()
    #     vybrany_material = data["material"][index]

    #     tani = vybrany_material["bod_tani"]
    #     varu = vybrany_material["bod_varu"]
    #     tep_kapacita_pevne = vybrany_material["tepelna_kapacita_pevne"]
    #     tep_kapacita_kapalina = vybrany_material["tepelna_kapacita_kapalina"]
    #     skupenske_teplo_tani = vybrany_material["skupenske_teplo_tani"]
    #     skupenske_teplo_varu = vybrany_material["skupenske_teplo_varu"]

    #     vysl = logika.vypocitat_a(vybrany_material,self.energie.text(),self.vaha.text(),self.poc_tepl.text())

    #     print(f" Nazev materialu: {vybrany_material['nazev']}\n Bod tani: {tani}\n Bod varu: {varu}\n Merna kapacita: {tep_kapacita_pevne}\n Testovy vysledek: {vysl}\n Zadana energie: {self.energie.text()}\n Zadana vaha: {self.vaha.text()}\n Zadana teplota: {self.poc_tepl.text()} \n test: {int(varu)-int(tani)}")
    #     print("test2:", float(self.energie.text())/(float(self.vaha.text())*int(self.poc_tepl.text())))
    #     print(f"test3: {vysl}")

class pridani_materialu(QWidget):
    def __init__(self, hlavni_okno_ref):
        super().__init__()

        self.hlavni_okno_ref = hlavni_okno_ref
        self.setWindowTitle("Pridani materialu")
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setStyleSheet("""
        QWidget {
            background-color: #FFDD99;                 
        }
        QPushButton {
            font-size: 18px;
            background-color: #FFAA00;
        }
        QLineEdit {
            background-color: #FFAA00;
            color: #ffffff;
        }
        """)



        layout = QGridLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignLeft)


        validator = QIntValidator()


        self.nazev_napis = QtWidgets.QLabel("Nazev materialu")
        self.t_tani_napis = QtWidgets.QLabel("Bod tání")
        self.t_varu_napis = QtWidgets.QLabel("Bod varu")
        self.c_pevne_napis = QtWidgets.QLabel("Tepelná kapacita\n pevné skupenství")
        self.c_kapalina_napis = QtWidgets.QLabel("Tepelná kapacita\nkapalné skupenství")
        self.l_tani_napis = QtWidgets.QLabel("Skup. teplo tání")
        self.l_varu_napis = QtWidgets.QLabel("Skup. teplo varu")

        self.t_tani_napis_po = QtWidgets.QLabel("(°C)")
        self.t_varu_napis_po = QtWidgets.QLabel("(°C)")
        self.c_pevne_napis_po = QtWidgets.QLabel("(J/kg°C)")
        self.c_kapalina_napis_po = QtWidgets.QLabel("(J/kg°C)")
        self.l_tani_napis_po = QtWidgets.QLabel("(J/kg)")
        self.l_varu_napis_po = QtWidgets.QLabel("(J/kg)")

        self.btn_smazat = QtWidgets.QPushButton()
        self.btn_smazat.setIcon(QIcon("kos.png"))
        self.btn_smazat.setIconSize(QSize(30, 30)) # Velikost ikony
        self.btn_smazat.setFixedSize(50, 50)
        self.btn_smazat.setStyleSheet("background-color: transparent; border: none; ")

        self.combosmazat = QComboBox()
        with open('data.json','r',encoding='UTF-8') as f:
            data = json.load(f)
            seznam_nazvu = [m["nazev"] for m in data["material"]]
            self.combosmazat.addItems(seznam_nazvu)   

        self.smazat = QtWidgets.QPushButton("Smazat")
        self.smazat.setStyleSheet("background-color: #FF0000; color: white; font-size: 18px;")

        self.nazev = QtWidgets.QLineEdit()
        self.t_tani = QtWidgets.QLineEdit()
        self.t_varu = QtWidgets.QLineEdit()
        self.c_pevne = QtWidgets.QLineEdit()
        self.c_kapalina = QtWidgets.QLineEdit()
        self.l_tani = QtWidgets.QLineEdit()
        self.l_varu = QtWidgets.QLineEdit()

        self.nazev.setFixedWidth(150)
        self.l_varu.setFixedWidth(150)
        self.l_tani.setFixedWidth(150)
        self.c_kapalina.setFixedWidth(150)
        self.c_pevne.setFixedWidth(150)
        self.t_varu.setFixedWidth(150)
        self.t_tani.setFixedWidth(150)


        self.button = QtWidgets.QPushButton("Přidat")

        self.t_tani.setValidator(validator)
        self.t_varu.setValidator(validator)
        self.c_pevne.setValidator(validator)
        self.c_kapalina.setValidator(validator)
        self.l_tani.setValidator(validator)
        self.l_varu.setValidator(validator)

        layout.addWidget(self.btn_smazat,0,2)


        layout.addWidget(self.nazev_napis,1,0)
        layout.addWidget(self.t_tani_napis,2,0)
        layout.addWidget(self.t_varu_napis,3,0)
        layout.addWidget(self.c_pevne_napis,4,0)
        layout.addWidget(self.c_kapalina_napis,5,0)
        layout.addWidget(self.l_tani_napis,6,0)
        layout.addWidget(self.l_varu_napis,7,0)

        layout.addWidget(self.t_tani_napis_po,2,2)
        layout.addWidget(self.t_varu_napis_po,3,2)
        layout.addWidget(self.c_pevne_napis_po,4,2)
        layout.addWidget(self.c_kapalina_napis_po,5,2)
        layout.addWidget(self.l_tani_napis_po,6,2)
        layout.addWidget(self.l_varu_napis_po,7,2)

        layout.addWidget(self.nazev,1,1)   
        layout.addWidget(self.t_tani,2,1)
        layout.addWidget(self.t_varu,3,1)
        layout.addWidget(self.c_pevne,4,1)
        layout.addWidget(self.c_kapalina,5,1)
        layout.addWidget(self.l_tani,6,1)
        layout.addWidget(self.l_varu,7,1) 
        layout.addWidget(self.button,8,2,QtCore.Qt.AlignRight)
        layout.setColumnStretch(3, 1)
        layout.setRowStretch(9, 1)

       
        layout.addWidget(self.combosmazat, 1, 3,2,2, QtCore.Qt.AlignCenter) # Přidání testovacího labelu do pravého horního rohu
        layout.addWidget(self.smazat, 3, 3,2,2, QtCore.Qt.AlignCenter) # Přidání tlačítka smazat vedle testovacího labelu
        self.combosmazat.setStyleSheet("font-size: 20px;") # Nastavení stylu pro testovací label
        self.combosmazat.hide()
        self.smazat.hide()
        
        

       
        self.smazat.clicked.connect(self.smazani_materialu)
        self.btn_smazat.clicked.connect(self.rozsireni)
        self.button.clicked.connect(self.pridani_materialu)


    def pridani_materialu(self):
        # nazev = input("Zadej název materiálu: ")
        # t_tani = float(input("Zadej bod tání (°C): "))
        # t_varu = float(input("Zadej bod varu (°C): "))
        # c_pevne = float(input("Zadej měrnou tepelnou kapacitu - pevné skupenství (J/kg°C): "))
        # c_kapalina = float(input("Zadej měrnou tepelnou kapacitu - kapalné skupenství (J/kg°C): "))
        # l_tani = float(input("Zadej měrné skupenské teplo tání (J/kg): "))
        # l_varu = float(input("Zadej měrné skupenské teplo varu (J/kg): "))
        if self.nazev.text() and self.t_tani.text() and self.t_varu.text() and self.c_pevne.text() and self.c_kapalina.text() and self.l_tani.text() and self.l_varu.text():
            if  self.nazev.text() in [m["nazev"] for m in data["material"]]:
                self.oznameni("Materiál s tímto názvem již existuje!")

            else:
                novy_material = {
                    "nazev": self.nazev.text(),
                    "bod_tani": self.t_tani.text(),
                    "bod_varu": self.t_varu.text(),
                    "tepelna_kapacita_pevne": self.c_pevne.text(),
                    "tepelna_kapacita_kapalina": self.c_kapalina.text(),
                    "skupenske_teplo_tani": self.l_tani.text(),
                    "skupenske_teplo_varu": self.l_varu.text()
                }

                self.hlavni_okno_ref.combo.addItem(self.nazev.text())
                data["material"].append(novy_material)
                with open('data.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)  # ulozeni zpet do souboru
                self.oznameni("Materiál byl úspěšně přidán.")
                self.close()

        else:
            self.oznameni("Vyplňte všechna pole!")

    def smazani_materialu(self):
        index = self.combosmazat.currentIndex()
        vybrany_material = data["material"][index]
        data["material"].remove(vybrany_material)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)  # ulozeni zpet do souboru
        self.hlavni_okno_ref.combo.removeItem(index)
        self.hlavni_okno_ref.combo.setCurrentIndex(0)
        self.combosmazat.removeItem(index)
        self.combosmazat.setCurrentIndex(0)
        self.oznameni("Materiál byl úspěšně smazán.")
        self.close()  

    def rozsireni(self,__init__):
        if self.combosmazat.isVisible():
            self.setMinimumSize(400, 300)
            self.setMaximumSize(400, 300)
            self.combosmazat.hide()
            self.smazat.hide()
            self.resize(400, 300)
        else:
            self.setMaximumSize(600, 300)
            self.setMinimumSize(600, 300)
            self.resize(600, 300) 
            self.combosmazat.show()   
            self.smazat.show()       

    def oznameni(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Oznámení")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()






okno_hlavni = hlavni_okno()
okno_hlavni.show()
sys.exit(app.exec())













