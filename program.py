import os
import sys
import json
import ctypes
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout,QComboBox,QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIntValidator, QPixmap,QIcon,QRegularExpressionValidator
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt,QSize


NORMAL_STYLE_MAIN = """
    QWidget { background-color: #FFDD99; color: #000000; font-family: sans-serif; }
    hlavni_okno QGroupBox { 
        font-weight: bold; border: 2px solid #D18B00; 
        margin-top: 1.1em; border-radius: 5px; padding: 10px;
    }
    hlavni_okno QPushButton { background-color: #FFAA00; border-radius: 8px; font-weight: bold; min-height: 35px; }
    hlavni_okno QLineEdit { background-color: #ffffff; border: 1px solid #D18B00; border-radius: 4px; padding: 5px; }
    hlavni_okno QComboBox { background-color: #D18B00;  border-radius: 4px; padding: 5px; }
    pridani_materialu    QWidget {
            background-color: #FFDD99;                 
        }
    pridani_materialu    QPushButton {
            font-size: 18px;
            background-color: #FFAA00;
        }
    pridani_materialu    QLineEdit {
            background-color: #FFAA00;
            color: #ffffff;
        }
    nastaveni_okno QGroupBox { 
        font-weight: bold; border: 2px solid #D18B00; 
        margin-top: 1.1em; border-radius: 5px; padding: 10px;
    }
    nastaveni_okno QPushButton { background-color: #FFAA00; border-radius: 8px; font-weight: bold; min-height: 35px; }
    nastaveni_okno QLineEdit { background-color: #ffffff; border: 1px solid #D18B00; border-radius: 4px; padding: 5px; }
    nastaveni_okno QComboBox { background-color: #D18B00; color: #ffffff;  border-radius: 4px; padding: 5px; }
"""

BARVOSLEPY_STYLE = """
/* GLOBÁLNÍ ZÁKLAD */
    QWidget { background-color: #000000; color: #FFFFFF; font-family: sans-serif; }

    /* HLAVNÍ OKNO */
    hlavni_okno QGroupBox { 
        font-weight: bold; border: 3px solid #FFFF00; 
        margin-top: 1.1em; border-radius: 5px; padding: 10px; color: #FFFF00;
    }
    hlavni_okno QPushButton { background-color: #0055FF; border: 2px solid #FFFF00; color: #FFFFFF; font-weight: bold; min-height: 35px; }
    hlavni_okno QLineEdit { background-color: #ffffff; color: #000000; border: 2px solid #FFFF00; border-radius: 4px; padding: 5px; }
    hlavni_okno QComboBox { background-color: #FFFF00; color: #000000; border-radius: 4px; padding: 5px; font-weight: bold; }

    /* PŘIDÁNÍ MATERIÁLU */
    pridani_materialu QWidget {
        background-color: #000000;                 
    }
    pridani_materialu QPushButton {
        font-size: 18px;
        background-color: #0055FF;
        border: 2px solid #FFFF00;
        color: #FFFFFF;
    }
    pridani_materialu QLineEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 2px solid #FFFF00;
    }

    /* NASTAVENÍ OKNO */
    nastaveni_okno QGroupBox { 
        font-weight: bold; border: 3px solid #FFFF00; 
        margin-top: 1.1em; border-radius: 5px; padding: 10px; color: #FFFF00;
    }
    nastaveni_okno QPushButton { background-color: #0055FF; border: 2px solid #FFFF00; color: #FFFFFF; font-weight: bold; min-height: 35px; }
    nastaveni_okno QLineEdit { background-color: #ffffff; color: #000000; border: 2px solid #FFFF00; border-radius: 4px; padding: 5px; }
    nastaveni_okno QComboBox { background-color: #FFFF00; color: #000000; border-radius: 4px; padding: 5px; font-weight: bold; }

    /* GLOBÁLNÍ MESSAGEBOX PRO SLEPÉ */
    QMessageBox { background-color: #000000; border: 2px solid #FFFF00; }
    QMessageBox QLabel { color: #FFFFFF; font-size: 16px; font-weight: bold; }
    QMessageBox QPushButton { background-color: #0055FF; color: #FFFFFF; border: 2px solid #FFFF00; min-width: 80px; }
"""

# global funkce pro zmenu
def aplikuj_vzhled(vzhled_jmeno):
    app = QApplication.instance()
    if vzhled_jmeno == "Barvoslepý":
        app.setStyleSheet(BARVOSLEPY_STYLE)
    else:
        app.setStyleSheet(NORMAL_STYLE_MAIN)

import logika
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Načtení dat
try:
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except Exception as e:
    print(f"Chyba při načítání JSON: {e}")
    data = {"material": []}

class hlavni_okno(QWidget):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Fyzikální Kalkulačka Materiálů")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(600, 650)
        # self.setStyleSheet(NORMAL_STYLE_MAIN)

                           

        # main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(20)

        # vyber mat
        mat_group = QtWidgets.QGroupBox("Výběr materiálu")
        mat_layout = QtWidgets.QHBoxLayout()
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.combo.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        # combo se naplni datama
        seznam_nazvu = [m["nazev"] for m in data["material"]]
        self.combo.addItems(seznam_nazvu)
        
        self.btn_info = QtWidgets.QPushButton("Informace o mat.")
        self.btn_info.clicked.connect(self.zobrazit_info)
        
        mat_layout.addWidget(QtWidgets.QLabel("Materiál:"))
        mat_layout.addWidget(self.combo, 2) # Poměr 2 pro combobox
        mat_layout.addWidget(self.btn_info, 1)
        mat_group.setLayout(mat_layout)
        main_layout.addWidget(mat_group)

        # A
        group_a = QtWidgets.QGroupBox("Cvičení A: Výpočet výsledné teploty")
        layout_a = QtWidgets.QGridLayout()
        
        self.energie = QtWidgets.QLineEdit(); self.energie.setPlaceholderText("Joulů (J)")
        self.vaha = QtWidgets.QLineEdit(); self.vaha.setPlaceholderText("Kilogramů (kg)")
        self.poc_tepl = QtWidgets.QLineEdit(); self.poc_tepl.setPlaceholderText("Celsia (°C)")
        self.vypoct = QtWidgets.QPushButton("VYPOČÍTAT VÝSLEDEK")
        self.vypoct.clicked.connect(self.vypocitat)

        layout_a.addWidget(QtWidgets.QLabel("Vstupní energie:"), 0, 0)
        layout_a.addWidget(self.energie, 1, 0)
        layout_a.addWidget(QtWidgets.QLabel("Hmotnost:"), 0, 1)
        layout_a.addWidget(self.vaha, 1, 1)
        layout_a.addWidget(QtWidgets.QLabel("Počáteční teplota:"), 0, 2)
        layout_a.addWidget(self.poc_tepl, 1, 2)
        layout_a.addWidget(self.vypoct, 2, 0, 1, 3) # pres 3 sloupce
        
        group_a.setLayout(layout_a)
        main_layout.addWidget(group_a)

        # B
        group_b = QtWidgets.QGroupBox("Cvičení B: Výpočet potřebné energie")
        layout_b = QtWidgets.QGridLayout()
        
        self.hmotnost2 = QtWidgets.QLineEdit(); self.hmotnost2.setPlaceholderText("kg")
        self.poc_teplota2 = QtWidgets.QLineEdit(); self.poc_teplota2.setPlaceholderText("°C")
        self.cilova_teplota = QtWidgets.QLineEdit(); self.cilova_teplota.setPlaceholderText("°C")
        self.btn_vypocet_b = QtWidgets.QPushButton("SPOČÍTAT POTŘEBNOU ENERGII")
        self.btn_vypocet_b.clicked.connect(self.vypocitat_b)

        layout_b.addWidget(QtWidgets.QLabel("Hmotnost:"), 0, 0)
        layout_b.addWidget(self.hmotnost2, 1, 0)
        layout_b.addWidget(QtWidgets.QLabel("Počáteční teplota:"), 0, 1)
        layout_b.addWidget(self.poc_teplota2, 1, 1)
        layout_b.addWidget(QtWidgets.QLabel("Cílová teplota:"), 0, 2)
        layout_b.addWidget(self.cilova_teplota, 1, 2)
        layout_b.addWidget(self.btn_vypocet_b, 2, 0, 1, 3)

        group_b.setLayout(layout_b)
        main_layout.addWidget(group_b)

        # sprava matra
        layout_c = QtWidgets.QHBoxLayout()
        main_layout.addStretch() # Toto odsune zbytek nahoru
        self.button = QtWidgets.QPushButton("⚙ SPRÁVA MATERIÁLŮ")
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.test)
        layout_c.addWidget(self.button, 0, QtCore.Qt.AlignLeft)

        self.button1 = QtWidgets.QPushButton("⚙ Nastaveni") 
        self.button1.setFixedWidth(200)

        self.button1.clicked.connect(self.nastaveni)
        layout_c.addWidget(self.button1,0,QtCore.Qt.AlignRight)
        main_layout.addLayout(layout_c)

        # Validatory
        regex_teplota = QRegularExpression(r"^-?\d*\.?\d*$")
        self.teplota_validator = QRegularExpressionValidator(regex_teplota)
        self.poc_tepl.setValidator(self.teplota_validator)

        regex = QRegularExpression(r"^[0-9]*\.?[0-9]*$")
        validator = QRegularExpressionValidator(regex)
        for field in [self.energie, self.vaha, self.hmotnost2, self.cilova_teplota]:
            field.setValidator(validator)





        # ----------------------------------------------

    def test(self):
        self.pridani_materialu_okno = pridani_materialu(self)
        self.pridani_materialu_okno.show()

    def nastaveni(self):
        self.okno_nastaveni = nastaveni_okno(self)
        self.okno_nastaveni.show()
        

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
        msg.setWindowIcon(QIcon('icon.png'))
        msg.setText(f"Název materiálu: {nazev}\nBod tání: {bod_tani} °C\nBod varu: {bod_varu} °C\nTepelná kapacita pevné skupenství: {tep_kap_pev} J/kg°C\nTepelná kapacita kapalné skupenství: {tep_kap_kapal} J/kg°C\nSkupenské teplo tání: {skup_tani} J/kg\nSkupenské teplo varu: {skup_varu} J/kg")

        tlacitko_tajne = msg.addButton("", QMessageBox.ActionRole)
        tlacitko_tajne.setStyleSheet('background-color:#FFDD50;border:none;')
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()
        if msg.clickedButton() == tlacitko_tajne:
            self.otevrit_easter_egg()
    def otevrit_easter_egg(self):
            # 1. Vytvoření okna (uložíme do self, aby nezmizelo)
            self.tajne_okno = QWidget() 
            self.tajne_okno.setWindowTitle("Easter Egg!")
            self.tajne_okno.setBaseSize(1000,600)
            self.tajne_okno.setStyleSheet("background-color: black; color: lime;")

            # 2. Nejdříve vytvoříme layout
            main_layout = QtWidgets.QVBoxLayout()

            # 3. Vytvoříme tlačítko a přidáme ho do layoutu
            self.btn_easter = QtWidgets.QPushButton()
            self.btn_easter.setIcon(QtGui.QIcon("icon.png"))
            self.btn_easter.setIconSize(QtCore.QSize(1000, 500)) # Aby ikona nebyla prťavá
            self.btn_easter.setStyleSheet("background-color: transparent; border: none;")
            
            main_layout.addWidget(self.btn_easter, 0, QtCore.Qt.AlignCenter)

            # 4. TEPRVE TEĎ nastavíme layout oknu
            self.tajne_okno.setLayout(main_layout)
            
            # 5. Zobrazíme
            self.tajne_okno.show()
            
      

        




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
            msg.setWindowIcon(QIcon('icon.png'))
            msg.setText("Zadejte platné číselné hodnoty.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def vypocitat_b(self):
        try: 
            index = self.combo.currentIndex()
            vybrany_material = data["material"][index]
            celkova_energie = logika.vypocitat_b(vybrany_material,self.cilova_teplota.text(),self.hmotnost2.text(),self.poc_teplota2.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Výsledek")
            msg.setText(f"Potřebna energie: {celkova_energie} J")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Chyba")
            msg.setWindowIcon(QIcon('icon.png'))
            msg.setText("Zadejte platné číselné hodnoty.")
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
        # self.setStyleSheet(NORMAL_STYLE_MATERIAL)



        layout = QGridLayout()
        self.setLayout(layout)
        layout.setAlignment(QtCore.Qt.AlignLeft)


        validator = QIntValidator()
        regex_teplota = QRegularExpression(r"^\d*\.?\d*$")
        self.teplota_validator = QRegularExpressionValidator(regex_teplota)


        self.nazev_napis = QtWidgets.QLabel("Nazev materialu")
        self.t_tani_napis = QtWidgets.QLabel("Bod tání")
        self.t_varu_napis = QtWidgets.QLabel("Bod varu")
        self.c_pevne_napis = QtWidgets.QLabel("Tepelná kapacita\n pevné skupenství")
        self.c_kapalina_napis = QtWidgets.QLabel("Tepelná kapacita\nkapalné skupenství")
        self.t_kapacita_plyn = QtWidgets.QLabel("Tepelná kapacita\nplynne skupenstvi")
        self.l_tani_napis = QtWidgets.QLabel("Skup. teplo tání")
        self.l_varu_napis = QtWidgets.QLabel("Skup. teplo varu")

        self.t_tani_napis_po = QtWidgets.QLabel("(°C)")
        self.t_varu_napis_po = QtWidgets.QLabel("(°C)")
        self.c_pevne_napis_po = QtWidgets.QLabel("(J/kg°C)")
        self.c_kapalina_napis_po = QtWidgets.QLabel("(J/kg°C)")
        
        self.l_tani_napis_po = QtWidgets.QLabel("(J/kg)")
        self.l_varu_napis_po = QtWidgets.QLabel("(J/kg)")

        self.btn_smazat = QtWidgets.QPushButton()
        self.btn_smazat.setIcon(QIcon("trash.png"))
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
                if int(self.t_tani.text()) >= int(self.t_varu.text()):
                    self.oznameni("Bod tání musí být menší než bod varu!")
                elif int(self.c_kapalina.text()) <= int(self.c_pevne.text()):
                    self.oznameni("Tepelná kapacita kapalné skupenství musí být větší než tepelná kapacita pevné skupenství!")
                elif int(self.l_tani.text()) >= int(self.l_varu.text()):
                    self.oznameni("Skupenské teplo tání musí být menší než skupenské teplo varu!")
                else:
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

class nastaveni_okno(QWidget):
    def __init__(self, hlavni_okno_ref):
        super().__init__()
        self.hlavni_okno_ref = hlavni_okno_ref
        self.setWindowTitle("Nastavení vzhledu")
        self.setFixedSize(300, 150)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        layout.addWidget(QtWidgets.QLabel("Vyberte režim zobrazení:"))
        
        self.combo_vzhled = QComboBox()
        self.combo_vzhled.addItems(["Normální", "Barvoslepý"])
        
        # Nastavíme combo na aktuální styl aplikace
        aktuatni_qss = QApplication.instance().styleSheet()
        if "background-color: #000000" in aktuatni_qss:
            self.combo_vzhled.setCurrentIndex(1)
            
        self.combo_vzhled.currentIndexChanged.connect(self.zmena_stylu)
        layout.addWidget(self.combo_vzhled)
        
        self.btn_zavrit = QtWidgets.QPushButton("Hotovo")
        self.btn_zavrit.clicked.connect(self.close)
        layout.addWidget(self.btn_zavrit)

    def zmena_stylu(self):
        vybrano = self.combo_vzhled.currentText()
        aplikuj_vzhled(vybrano)

    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Nastavíme výchozí styl hned při startu pro celou aplikaci
    app.setStyleSheet(NORMAL_STYLE_MAIN)
    
    window = hlavni_okno()
    window.show()
    
    sys.exit(app.exec_())













