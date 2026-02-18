import os
import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QComboBox




script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

with open('data.json', 'r', encoding='utf-8') as file: # pro otevreni v cmd je potreba to otevrit absolutni cestou (c:/Users/wwtf8/Desktop/cviceni/zakaznicky_system/zakaznici_upd.py)
    data = json.load(file)   

def pridani_materialu():
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



def vypsat_materialy():
    for i, material in enumerate(data["material"], start=1):
        print(f"{i}. Material:", material["nazev"], "Bod tani:", material["bod_tani"],"°C", "Bod varu:", material["bod_varu"],"°C","\n") # vypsat materialy s jejich atributy

vypsat_materialy()

# pridani_materialu()


# testovaci zona




app = QtWidgets.QApplication([])

hlavni_okno = QtWidgets.QWidget()
hlavni_okno.setWindowTitle("Test")
hlavni_okno.setFixedSize(500,500)
hlavni_okno.setStyleSheet("""
        QPushButton {
            font-size: 18px;
            background-color: #f0f0f0;
        }
        QLineEdit {
            background-color: #ffffff
        }
    """)

layout = QtWidgets.QGridLayout()

hlavni_okno.setLayout(layout)



combo = QComboBox()

energie = QtWidgets.QLineEdit()
vaha = QtWidgets.QLineEdit()
poc_tepl = QtWidgets.QLineEdit()

debug1 = QtWidgets.QPushButton("Debug")


layout.addWidget(combo,0,0)
layout.addWidget(energie,0,1)
layout.addWidget(vaha,0,2)
layout.addWidget(poc_tepl,0,3)
layout.addWidget(debug1,0,4)


def debugs():

    index = combo.currentIndex()
    vybrany_material = data["material"][index]

    tani = vybrany_material["bod_tani"]
    varu = vybrany_material["bod_varu"]
    kapacita = vybrany_material["merna_kapacita"]

    vysl = tani - varu

    print(vybrany_material["nazev"],tani ,varu,kapacita,vysl, energie.text(),vaha.text(),poc_tepl.text())


debug1.clicked.connect(debugs)


with open('data.json','r',encoding='UTF-8') as f:
    data = json.load(f)
    seznam_nazvu = [m["nazev"] for m in data["material"]]
    combo.addItems(seznam_nazvu)

hlavni_okno.show()
app.exec()



























# Funkce
