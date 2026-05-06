import sys
import os
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QListWidget,QListWidgetItem, QTableWidget, QHeaderView, QTableWidgetItem,
                             QLineEdit, QDialog, QMessageBox,QGroupBox)
from PyQt5.QtCore import Qt, QRegularExpression,QSize
from PyQt5.QtGui import QPalette, QColor, QIntValidator, QPixmap,QIcon,QRegularExpressionValidator,QRegExpValidator,QDoubleValidator



NORMAL_STYLE_MAIN = """
            * {
                font-size: 14px;
            }

            AuthDialog {
                background-color:white;
            }
            QMainWindow {
                background-color: #F3F4F6;
            }
            QListWidget {
                background-color: #1F2937;
                color: #D1D5DB;
                border: none;
                padding-top: 20px;
                padding-left:20px;
                outline: 0;
            }
            QListWidget::item {
                padding: 15px 20px;

            }
            QListWidget::item:hover {
                background-color: #374151;
            }
            QListWidget::item:selected {
                background-color: #111827;
                color: #FFFFFF;
                border-left: 4px solid #3B82F6;
            }
            QLabel {
                color: #111827;
                padding: 10px 0px;
            }
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QTableWidget {
                background-color: white;
                color: #1F2937;
                border: none;
                gridline-color: #1F2937;
                selection-background-color: gray;
                selection-color: white;
            }
            QHeaderView {
                background-color: #1F2937;
            }
            QHeaderView::section {
                background-color: #1F2937;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #1F2937;
                border: none;
            }    
            QComboBox {
                color: black;
            }
            #MojeOblast {
                background-color: #FFFFFF;
                border: none;
                border-radius: 10px;
            }
            QMessageBox QLabel{
                color: white;
            }
        """

data = []
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
    
# ==========================================
# 1. PŘIHLAŠOVACÍ OKNO
# ==========================================

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setFixedSize(375,425)
        self.user_role = None
        self.check_db()

        self.main_layout = QVBoxLayout(self)

        self.auth_pages = QStackedWidget()
        self.main_layout.addWidget(self.auth_pages)

        self.create_login_page() # index 0
        self.create_register_page() # index 1

        

    def create_login_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h2>Prihlaseni</h2>"))

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Uzivatelske jmeno")
        layout.addWidget(self.login_user)

        gridlayout1 = QtWidgets.QGridLayout()

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Heslo")
        self.login_password.setEchoMode(QLineEdit.Password)
        gridlayout1.addWidget(self.login_password,0,0)


        self.btn_eye1 = QPushButton()
        self.btn_eye1.setIcon(QIcon("assets/eye_icon.png"))
        self.btn_eye1.setIconSize(QSize(28,28))
        self.btn_eye1.setFlat(True)  # Tohle odstraní standardní šedé pozadí a rámeček
        self.btn_eye1.setStyleSheet("border:none; background:transparent;width:10px;")
        self.btn_eye1.clicked.connect(lambda: self.make_password_visible(self.login_password))
        self.btn_eye1.setCursor(Qt.PointingHandCursor)
        gridlayout1.addWidget(self.btn_eye1,0,1)

        layout.addLayout(gridlayout1)

        btn_login = QPushButton("Vstoupit")
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)


        btn_to_reg = QPushButton("Nemate ucet? Zaregistrujte se")
        btn_to_reg.setFlat(True)
        btn_to_reg.clicked.connect(lambda: self.auth_pages.setCurrentIndex(1))
        layout.addWidget(btn_to_reg)

        #----------------
        #  VALIDATORY


        regex_USERNAME = QRegularExpression(r"^[a-zA-Z0-9]+([._][a-zA-Z0-9]+)?$")
        validator_user = QRegularExpressionValidator(regex_USERNAME)
        self.login_user.setValidator(validator_user)

        regex_password = QRegularExpression(r"^[a-zA-Z0-9!@#$%^&*_\-+=]+$")
        validator_password = QRegularExpressionValidator(regex_password)
        self.login_password.setValidator(validator_password)


        #----------------
        layout.addStretch()
        self.auth_pages.addWidget(page)


    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel("<h3>Registrace</h3>"))

        self.reg_user_login = QLineEdit()
        self.reg_user_login.setPlaceholderText("Uzivatelske jmeno")
        layout.addWidget(self.reg_user_login)

        self.reg_user_name = QLineEdit()
        self.reg_user_name.setPlaceholderText("Vase jmeno")
        layout.addWidget(self.reg_user_name)

        self.reg_user_surname = QLineEdit()
        self.reg_user_surname.setPlaceholderText("Vase prijmeni")
        layout.addWidget(self.reg_user_surname)

        self.reg_user_number = QLineEdit()
        self.reg_user_number.setPlaceholderText("Vase telefonni cislo")
        layout.addWidget(self.reg_user_number)

        self.reg_user_firm = QLineEdit()
        self.reg_user_firm.setPlaceholderText("Firma")
        layout.addWidget(self.reg_user_firm)

        gridlayout = QtWidgets.QGridLayout()

        self.reg_user_pass = QLineEdit()
        self.reg_user_pass.setPlaceholderText("Zvolte heslo")
        self.reg_user_pass.setEchoMode(QLineEdit.Password)  
        gridlayout.addWidget(self.reg_user_pass,0,0)

        self.reg_user_ver = QLineEdit()
        self.reg_user_ver.setPlaceholderText("Zopakujte heslo")
        self.reg_user_ver.setEchoMode(QLineEdit.Password)
        gridlayout.addWidget(self.reg_user_ver,0,1)
        self.echomode = 0


        self.btn_eye = QPushButton()
        self.btn_eye.setIcon(QIcon("assets/eye_icon.png"))
        self.btn_eye.setIconSize(QSize(28,28))
        self.btn_eye.setFlat(True)  # Tohle odstraní standardní šedé pozadí a rámeček
        self.btn_eye.setStyleSheet("border:none; background:transparent;width:10px;")
        self.btn_eye.clicked.connect(lambda: self.make_password_visible(self.reg_user_pass,self.reg_user_ver))
        self.btn_eye.setCursor(Qt.PointingHandCursor)
        gridlayout.addWidget(self.btn_eye,0,2)

        layout.addLayout(gridlayout)
        
        btn_reg = QPushButton("Vytvorit ucet")
        btn_reg.clicked.connect(self.handle_register)
        layout.addWidget(btn_reg)

        btn_to_log = QPushButton("Zpet na login")
        btn_to_log.setFlat(True)
        btn_to_log.clicked.connect(lambda: self.auth_pages.setCurrentIndex(0))
        layout.addWidget(btn_to_log)



        #----------------
        #  VALIDATORY


        regex_USERNAME = QRegularExpression(r"^[a-zA-Z0-9]+([._][a-zA-Z0-9]+)?$")
        validator_user = QRegularExpressionValidator(regex_USERNAME)
        self.reg_user_name.setValidator(validator_user)

        regex_password = QRegularExpression(r"^[a-zA-Z0-9!@#$%^&*_\-+=]+$")
        validator_password = QRegularExpressionValidator(regex_password)
        self.reg_user_pass.setValidator(validator_password)
        self.reg_user_ver.setValidator(validator_password)


        #----------------

        layout.addStretch()
        self.auth_pages.addWidget(page)



    def handle_login(self):
        try:
            u = self.login_user.text()
            passw = self.login_password.text()

            self.db_file = "users.json"

            with open(self.db_file,'r') as file:
                data = json.load(file)
            
            for user_data in data.values():
                if user_data.get("username") == u:
                    found_user = user_data
                    break
            if found_user:
                if found_user.get("password") == passw:
                    jmeno = found_user.get("jmeno")
                    self.user_role = found_user.get("role")
                    self.user_id = found_user.get("id")
                    self.final_username = u
                    self.final_name = jmeno
                    self.accept()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Oznameni")
            msg.setText(f"Neplatne prihlasovaci udaje.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

                

             
        # if u in data:
        #     if data[u]["password"] == passw:
        #         jmeno = data[u]["jmeno"]   
        #         self.user_role = data[u]["role"]
        #         self.final_username = u  
        #         self.final_name = jmeno
        #         self.accept()
                

    def handle_register(self):
        u = self.reg_user_login.text()
        p = self.reg_user_pass.text()
        jmen = self.reg_user_name.text()
        prijm = self.reg_user_surname.text()
        telefon = self.reg_user_number.text()
        firma = self.reg_user_firm.text()
        self.db_file = "users.json"

        # cteni starych dat
        with open(self.db_file, 'r', encoding="utf-8") as file:
            data = json.load(file)


        if data:
            max_id = max(uzivatel["id"] for uzivatel in data.values())
            if max_id:
                new_id = max_id + 1
        elif not data:
            new_id = 1

        # zapisovani dat  
        if u in data:
            print("chyba")   
            return   
        data[f"user_{new_id}"] = {
            "id": new_id,  # nejvetsi id +1
            "username": u,
            "jmeno":jmen,
            "prijmeni":prijm,
            "telefon":telefon,
            "firma": firma,
            "password": p,
            "role": "zakaznik"
            
        }

        # prepis souboru
        if jmen == "" or prijm == "" or telefon == "" or firma == "" or u == "" or p == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Oznameni")
            msg.setText(f"Nezadali jste vsechny udaje.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        for polozka in data.values():
            jmeno = polozka.get("username")
            if jmeno == u:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Oznameni")
                msg.setText(f"Uzivatelske jmeno uz existuje.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        
        
        with open(self.db_file, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def make_password_visible(self,*inputs):
        if self.echomode == 0:
            for inp in inputs:
                inp.setEchoMode(QLineEdit.Normal)
            self.echomode = 1
        else:
            for inp in inputs:
                inp.setEchoMode(QLineEdit.Password)
            self.echomode = 0

    def check_db(self):

        self.db_file = "users.json"


        if not os.path.exists(self.db_file):
            print("hello world")

            users_db = {}

            username = "admin"
            users_db[f"user_1"] = {
                    "id": 1,
                    "username": "Admin",
                    "jmeno": "Admin",
                    "prijmeni": "Admin",
                    "telefon": "Admin",
                    "firma": "Admin",
                    "password": "Admin",
                    "role": "admin"
            }

            with open(self.db_file,'w') as file:
                json.dump(users_db,file,indent=4, ensure_ascii=False)


            

            print("users.json neexistoval. Vytvoreny novy seznam")

        else:
            print("users.json jiz existuje.")
            
        

# ================================
#             ADMIN OKNO
# ================================
        

        
class AdminSystemMockup(QMainWindow):
    def __init__(self,username,jmeno,id):
        super().__init__()
        self.current_user = username
        self.current_user_name = jmeno
        self.current_id = id
        print(id)


        self.user_file = "users.json"
        self.setWindowTitle(f"Admin - Prihlasen jako: {username}")
        self.setFixedSize(1000,600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(20)
        self.setCentralWidget(main_widget)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)

        menu_items = [
            "Správa uživatelů",
            "Přehled zakázek",
            "Statistiky",
            "Logy",
        ]
        self.sidebar.addItems(menu_items)
        spacer = QListWidgetItem()
        for i in range(5):
            name = "spacer"+f"{i}"
            name = QListWidgetItem()
            name.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            self.sidebar.addItem(name)
        self.sidebar.addItem("Nastaveni")
        self.sidebar.addItem("Odhlasit")
        self.sidebar.currentRowChanged.connect(self.switch_page)
        self.sidebar.itemClicked.connect(self.handle_sidebar_click)
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        # ----- VYTVORENI STRANEK ------
        self.create_customers_list_page()
        self.create_orders_page()
        self.create_stats_page()
        self.create_logs_page()


        self.sidebar.setCurrentRow(0)

    
    def logout_action(self):
        odpoved = QMessageBox.question(
            self, "Odhlášení", "Opravdu se chcete odhlásit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if odpoved == QMessageBox.StandardButton.Yes:
            self.close() # Tímto vyskočíš z app.exec() v main loopu a objeví se login

        


    def handle_sidebar_click(self,item):
        text = item.text()
        if text == "Odhlasit":
            self.logout_action()

    def switch_page(self,index):
        self.pages.setCurrentIndex(index)
    def add_blank_row(self):
        max_id = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                try:
                    # Převedeme text na číslo pro porovnání
                    current_id = int(item.text())
                    if current_id > max_id:
                        max_id = current_id
                except ValueError:
                    continue 

        new_id = max_id + 1
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        id_item = QTableWidgetItem(str(new_id))
        

        id_item.setFlags(id_item.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table.setItem(row_position, 0, id_item)
        
        for i in range(1, 7):
            self.table.setItem(row_position, i, QTableWidgetItem(""))
            

        combo = QtWidgets.QComboBox()
        combo.addItems(["zakaznik", "admin"])
        self.table.setCellWidget(row_position, 7, combo)

    def delete_user(self):
        current_row = self.table.currentRow()

        if current_row <0:
            QtWidgets.QMessageBox.warning(self, "Chyba", "Nejdrive vyberte uzivatele, ktereho chcete smazat.")
            return
            
        username = self.table.item(current_row,1).text()

        odpoved = QtWidgets.QMessageBox.question(
            self,
            "Podtvrdit smazani",
            f"opravdu chcete smazat uzivatele {username}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
        
        if odpoved == QtWidgets.QMessageBox.StandardButton.Yes:
            self.table.removeRow(current_row)
            self.save_custommer_data()
            QtWidgets.QMessageBox.information(self, "Hotovo", "Uzivatel byl smazan.")


    def oznamit_zmenu(self,index,combo):

        if combo.itemText(index) == "admin":
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Potvrzení změny role")
            msg.setText("Opravdu chcete tomuto uživateli přidělit práva ADMINA?")
            msg.setStyleSheet("color:white;")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok | 
                                   QtWidgets.QMessageBox.StandardButton.Cancel)
            
            vysledek = msg.exec()

            if vysledek == QMessageBox.StandardButton.Cancel:
                combo.setCurrentIndex(0)

    def load_custommer_data(self):
        if not os.path.exists(self.user_file):
            with open(self.user_file,'w',encoding="utf-8") as f:
                json.dump([],f)

        with open(self.user_file,'r',encoding="utf-8") as file:
            data = json.load(file)

        self.table.setRowCount(0)
        for polozka in data.values():
            row = self.table.rowCount()
            self.table.insertRow(row)


            combo = QtWidgets.QComboBox()
            combo.addItems(["zakaznik","admin"])

            aktualni_role = polozka.get("role","zakaznik")
            combo.setCurrentText(aktualni_role)
            combo.currentIndexChanged.connect(lambda index,c=combo: self.oznamit_zmenu(index,c))
            
            id_item = QTableWidgetItem(str(polozka.get("id", "")))
            username_item = QTableWidgetItem(str(polozka.get("username","")))
            jmeno_item = QTableWidgetItem(str(polozka.get("jmeno","")))
            prijmeni_item = QTableWidgetItem(str(polozka.get("prijmeni", "")))
            telefon_item = QTableWidgetItem(str(polozka.get("telefon", "")))
            firma_item = QTableWidgetItem(str(polozka.get("firma", "")))
            password_item = QTableWidgetItem(str(polozka.get("password","")))
            role_item = QTableWidgetItem(str(polozka.get("role")))

            id_item.setFlags(id_item.flags() ^ QtCore.Qt.ItemIsEditable)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, username_item)
            self.table.setItem(row, 2, jmeno_item)
            self.table.setItem(row, 3, prijmeni_item)
            self.table.setItem(row, 4, telefon_item)
            self.table.setItem(row, 5, firma_item)
            self.table.setItem(row, 6, password_item)
            self.table.setCellWidget(row, 7, combo)

    def save_custommer_data(self):
        new_data = {}

        for row in range(self.table.rowCount()):
            id_val  = self.table.item(row, 0).text()
            username_val = self.table.item(row,1).text()
            jmeno_val = self.table.item(row, 2).text()
            prijmeni_val = self.table.item(row, 3).text()
            telefon_val = self.table.item(row, 4).text()
            firma_val = self.table.item(row, 5).text()
            password_val = self.table.item(row, 6).text()
            combo = self.table.cellWidget(row, 7)
            vybrana_role = "zakaznik"
            if combo:
                vybrana_role = combo.currentText()

            key = f"user_{id_val}"

            new_data[key] = {
                "id": int(id_val),
                "username": username_val,
                "jmeno": jmeno_val,
                "prijmeni": prijmeni_val,
                "telefon": telefon_val,
                "firma": firma_val,
                "password": password_val,
                "role": vybrana_role
            }

        if username_val == "" or jmeno_val == "" or prijmeni_val == "" or telefon_val == "" or firma_val == "" or password_val == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Oznameni")
            msg.setText(f"Nezadali jste vsechny udaje.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        
        with open(self.user_file,'w',encoding="utf-8") as file:
            json.dump(new_data,file,indent=7)

            print("Data byla uspesne ulozena!")


            
    def create_customers_list_page(self):
        page = QWidget()
        self.customer_layout = QVBoxLayout(page)
        self.grid_button_layout = QtWidgets.QGridLayout()


        self.table = QTableWidget(0,8)
        self.table.setHorizontalHeaderLabels(["ID","Username","Jmeno","Prijmeni",'Telefonni Cislo','Firma','Heslo','role'])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedWidth(700)

        for i in range(1,7):
            self.table.setColumnWidth(i,200)
        

        self.load_data_button = QPushButton("Obnovit tabulku")
        self.load_data_button.clicked.connect(self.load_custommer_data)
        self.load_data_button.setFixedWidth(165)
        self.grid_button_layout.addWidget(self.load_data_button,0,0)



        self.save_data_button = QPushButton("Ulozit zmeny")
        self.save_data_button.clicked.connect(self.save_custommer_data)
        self.save_data_button.setFixedWidth(165)
        self.grid_button_layout.addWidget(self.save_data_button,0,1)

        self.add_new_row_button = QPushButton("Přidat uživatele")
        self.add_new_row_button.clicked.connect(self.add_blank_row)
        self.add_new_row_button.setFixedWidth(165)
        self.grid_button_layout.addWidget(self.add_new_row_button,0,2)

        self.delete_custommer_button = QPushButton("Smazat uzivatele")
        self.delete_custommer_button.clicked.connect(self.delete_user)
        self.delete_custommer_button.setFixedWidth(165)
        self.grid_button_layout.addWidget(self.delete_custommer_button,0,3)

        self.customer_layout.addWidget(self.table)
        self.customer_layout.addLayout(self.grid_button_layout)
        # self.customer_layout.addStretch()

        self.pages.addWidget(page)

# ============================================================================================================================================================================

    def load_user_orders(self):
            try:
                with open("orders.json", "r", encoding="utf-8") as f:
                    all_orders_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):

                self.table1.setRowCount(0)
                return

            self.table1.setRowCount(0)

            for key, data in all_orders_data.items():
                    row_position = self.table1.rowCount()
                    self.table1.insertRow(row_position)
                    
                    self.table1.setItem(row_position, 0, QTableWidgetItem(str(data.get("id", ""))))
                    self.table1.setItem(row_position, 1, QTableWidgetItem(str(data.get("user_id", ""))))
                    self.table1.setItem(row_position, 2, QTableWidgetItem(str(data.get("produkt", ""))))
                    self.table1.setItem(row_position, 3, QTableWidgetItem(str(data.get("pocet", "0"))))
                    self.table1.setItem(row_position, 4, QTableWidgetItem(str(data.get("description", ""))))
                    self.table1.setItem(row_position, 5, QTableWidgetItem(str(data.get("stav", "Nová"))))


    def save_all_orders_admin(self):
            # 1. Načteme aktuální stav JSONu (abychom měli základ pro případná ID)
            try:
                with open("orders.json", "r", encoding="utf-8") as f:
                    all_orders_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_orders_data = {}

            # Zjistíme nejvyšší ID pro případ, že admin přidal úplně nové řádky
            current_max_id = 0
            if all_orders_data:
                current_max_id = max([int(d["id"]) for d in all_orders_data.values()])

            # Vytvoříme si nový slovník pro uložení (admin přepisuje celý soubor tím, co vidí)
            new_json_data = {}

            # 2. Procházíme tabulku řádek po řádku
            for row in range(self.table1.rowCount()):
                # Načtení položek (pozor na indexy, u admina jich máš 7)
                item_id      = self.table1.item(row, 0)
                item_user_id = self.table1.item(row, 1)
                item_nazev   = self.table1.item(row, 2)
                item_pocet   = self.table1.item(row, 3)
                item_popis   = self.table1.item(row, 4) 
                item_stav    = self.table1.item(row, 5)
                item_datum   = self.table1.item(row, 6)

                # --- LOGIKA ID ---
                # Pokud ID v tabulce už existuje, použijeme ho. Pokud ne, vyrobíme nové.
                raw_id = item_id.text() if item_id else ""
                if raw_id.isdigit():
                    this_id = int(raw_id)
                else:
                    current_max_id += 1
                    this_id = current_max_id

                # Klíč v JSONu (např. order_1)
                key = f"order_{this_id}"

                # 3. Sestavení dat pro jeden řádek
                new_json_data[key] = {
                    "id": this_id,
                    "user_id": int(item_user_id.text()) if item_user_id and item_user_id.text().isdigit() else 0,
                    "produkt": item_nazev.text() if item_nazev else "",
                    "pocet": item_pocet.text() if item_pocet else "0",
                    "description": item_popis.text() if item_popis else "",
                    "stav": item_stav.text() if item_stav else "Nová",
                    "datum": item_datum.text() if item_datum else "2024-05-23"
                }

            # 4. Zápis do souboru (admin uloží vše)
            try:
                with open("orders.json", "w", encoding="utf-8") as f:
                    json.dump(new_json_data, f, indent=4, ensure_ascii=False)
                QtWidgets.QMessageBox.information(self, "Hotovo", "Všechny zakázky byly uloženy.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Chyba", f"Chyba při ukládání: {e}")







# ============================================================================================================================================================================        

    def create_orders_page(self):
        page = QWidget()
        self.order_layout = QVBoxLayout(page)
        
        self.table1 = QTableWidget(0,7)
        self.table1.setHorizontalHeaderLabels(["ID","USER_ID","Nazev","Pocet","Popis","Vyrizeno","Datum"])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table1.setFixedWidth(725)
        

        for i in range(2,4):
            self.table1.setColumnWidth(i,150)
        self.order_layout.addWidget(self.table1)
        
        grid_layout = QtWidgets.QGridLayout()

        self.update_button1 = QPushButton("Obnovit tabulku")
        self.update_button1.setFixedWidth(170)
        self.update_button1.clicked.connect(self.load_user_orders)
        grid_layout.addWidget(self.update_button1,0,0)


        self.save_button1 = QPushButton("Ulozit zmeny")
        self.save_button1.setFixedWidth(170)
        self.save_button1.clicked.connect(self.save_all_orders_admin)
        grid_layout.addWidget(self.save_button1,0,1)
        

        self.add_order_button = QPushButton("Pridat objednavku")
        self.add_order_button.setFixedWidth(170)
  #      grid_layout.addWidget(self.add_order_button,0,2)
        self.add_order_button.clicked.connect(self.add_blank_row)

        self.remove_customer_button = QPushButton("Smazat objednavku")
        self.remove_customer_button.setFixedWidth(170)
  #      grid_layout.addWidget(self.remove_customer_button,0,3)

        self.order_layout.addLayout(grid_layout)
        
        self.pages.addWidget(page) 



    def create_stats_page(self):
        page = QWidget()
        self.customer_layout = QVBoxLayout(page)
        self.customer_layout.addWidget(QLabel(f"Vitejte2"))
        self.pages.addWidget(page)

    def create_logs_page(self):
        page = QWidget()
        self.customer_layout = QVBoxLayout(page)
        self.customer_layout.addWidget(QLabel(f"Vitejte3"))
        self.pages.addWidget(page)

    


    
# ==========================================


class CustommerSystemMockup(QMainWindow):

    def __init__(self, username,jmeno,id):
        super().__init__()

        self.current_user = username
        self.current_user_name = jmeno
        self.current_id = id

        self.setWindowTitle(f"Zakaznik - Prihlasen jako: {username}")
        self.setFixedSize(1000,600)


        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(20)
        self.setCentralWidget(main_widget)

# ===================================================
#                   LEVY PANEL
# ===================================================
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)

        menu_items = [
            "Prehled",
            "Moje zakazky",
            "Můj profil"
        ]
        self.sidebar.addItems(menu_items)
        spacer = QListWidgetItem()
        for i in range(4):
            name = "spacer"+f"{i}"
            name = QListWidgetItem()
            name.setFlags(QtCore.Qt.ItemFlag.NoItemFlags)
            self.sidebar.addItem(name)
        self.sidebar.addItem("Nastaveni")
        self.sidebar.addItem("Podpora/Kontakt")
        self.sidebar.addItem("Odhlasit")
        self.sidebar.currentRowChanged.connect(self.switch_page)
        self.sidebar.itemClicked.connect(self.handle_sidebar_click)
        main_layout.addWidget(self.sidebar)


# ====================================================================
        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        
        # vytvoreni stranek pres funkce

        self.create_dashboard_page()
        self.create_order_page()
        self.create_settings_page()

        self.sidebar.setCurrentRow(0)

# ==========================================
#           FUNKCE APLIKACE
# ==========================================
    def logout_action(self):
        odpoved = QMessageBox.question(
            self, "Odhlasení", "Opravdu se chcete odhlasit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if odpoved == QMessageBox.StandardButton.Yes:
            self.close() # Tímto vyskočíš z app.exec() v main loopu a objeví se login

    def handle_sidebar_click(self,item):
        text = item.text()
        if text == "Odhlasit":
            self.logout_action()


    def add_blank_row(self):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            

            self.table.setItem(row_position, 0, QTableWidgetItem(""))
            

            self.table.setItem(row_position, 1, QTableWidgetItem(""))

            self.table.setItem(row_position, 2, QTableWidgetItem(""))
            
            description_item = QTableWidgetItem("")
            description_item.setFlags(description_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable) 
            self.table.setItem(row_position, 3, description_item)

            status_item = QTableWidgetItem("Ne")
            status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_position, 4, status_item)

    def load_user_orders(self):
        try:
            with open("orders.json", "r", encoding="utf-8") as f:
                all_orders_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.table.setRowCount(0)
            return

        self.table.setRowCount(0)
        for key, data in all_orders_data.items():
            # Filtrujeme podle tvého current_id
            if str(data.get("user_id")) == str(self.current_id):
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                # Tady načítáme data do tvých sloupců
                # Pokud máš ID v tabulce vidět, nechej to tak, pokud ne, 
                # ujisti se, že indexy sedí (0=ID, 1=Nazev, 2=Pocet, 3=Popis, 4=Stav)
                self.table.setItem(row, 0, QTableWidgetItem(str(data.get("id", ""))))
                self.table.setItem(row, 1, QTableWidgetItem(str(data.get("produkt", ""))))
                self.table.setItem(row, 2, QTableWidgetItem(str(data.get("pocet", "0"))))
                
                desc_item = QTableWidgetItem(str(data.get("description", "")))
                desc_item.setFlags(desc_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 3, desc_item)
                
                status_item = QTableWidgetItem(str(data.get("stav", "Ne")))
                status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 4, status_item)

                # Volitelné: Seřazení tabulky (pokud chceš)
                # self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def save_user_orders(self):
        try:
            with open("orders.json", "r", encoding="utf-8") as f:
                all_orders_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_orders_data = {}

        # Smažeme jen záznamy tohoto uživatele v paměti, abychom je nahradili novými z tabulky
        keys_to_remove = [k for k, v in all_orders_data.items() if str(v.get("user_id")) == str(self.current_id)]
        for key in keys_to_remove:
            del all_orders_data[key]

        # Zjistíme nejvyšší ID pro nové kousky
        current_max_id = 0
        if all_orders_data:
            current_max_id = max([int(d["id"]) for d in all_orders_data.values()])

        for row in range(self.table.rowCount()):
            id_item = self.table.item(row, 0)
            
            # Pokud řádek už má ID (bylo načteno), použijeme ho. Pokud ne, vyrobíme nové.
            if id_item and id_item.text() != "":
                this_id = int(id_item.text())
            else:
                current_max_id += 1
                this_id = current_max_id

            key = f"order_{this_id}"
            all_orders_data[key] = {
                "id": this_id,
                "user_id": self.current_id,
                "produkt": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
                "pocet": self.table.item(row, 2).text() if self.table.item(row, 2) else "0",
                "description": self.table.item(row, 3).text() if self.table.item(row, 3) else "",
                "stav": self.table.item(row, 4).text() if self.table.item(row, 4) else "Ne",
                "datum": "2024-05-23"
            }

        with open("orders.json", "w", encoding="utf-8") as f:
            json.dump(all_orders_data, f, indent=4, ensure_ascii=False)
        
        # Důležité: hned po uložení načíst, aby se v tabulce objevila ta nová ID
        self.load_user_orders()

    def delete_user(self):
        current_row = self.table.currentRow()

        if current_row <0:
            QtWidgets.QMessageBox.warning(self, "Chyba", "Nejdrive vyberte uzivatele, ktereho chcete smazat.")
            return
            
        username = self.table.item(current_row,1).text()

        odpoved = QtWidgets.QMessageBox.question(
            self,
            "Podtvrdit smazani",
            f"opravdu chcete smazat uzivatele {username}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
        
        if odpoved == QtWidgets.QMessageBox.StandardButton.Yes:
            self.table.removeRow(current_row)
            self.save_user_orders()
            QtWidgets.QMessageBox.information(self, "Hotovo", "Uzivatel byl smazan.")    
                
# ==========================================
#               VYTVORENI STRANEK
# ==========================================     

    def create_dashboard_page(self):
        page = QWidget()
        
        self.dashboard_layout = QVBoxLayout(page)
        self.dashboard_layout.addStretch()
        self.pages.addWidget(page)

        first_stat = QtWidgets.QGroupBox("Prvni statistika")
        first_stat = QtWidgets.QGroupBox("Druha statistika")
        treti_stat = QtWidgets.QGroupBox("Treti statistika")
        ctvrta_stat = QtWidgets.QGroupBox("Ctvrta statistika")


    def create_order_page(self):
        page = QWidget()
        self.order_layout = QVBoxLayout(page)
        
        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID", "Nazev", "Pocet", "Popis", "Vyrizeno"])
        self.table.setColumnHidden(0, True) 
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedWidth(725)
        

        for i in range(0,4):
            self.table.setColumnWidth(i,173)
        self.order_layout.addWidget(self.table)
        
        grid_layout = QtWidgets.QGridLayout()

        self.update_button1 = QPushButton("Obnovit tabulku")
        self.update_button1.setFixedWidth(170)
        self.update_button1.clicked.connect(self.load_user_orders)
        grid_layout.addWidget(self.update_button1,0,0)


        self.save_button1 = QPushButton("Ulozit zmeny")
        self.save_button1.setFixedWidth(170)
        self.save_button1.clicked.connect(self.save_user_orders)
        grid_layout.addWidget(self.save_button1,0,1)
        

        self.add_order_button = QPushButton("Pridat objednavku")
        self.add_order_button.setFixedWidth(170)
        grid_layout.addWidget(self.add_order_button,0,2)
        self.add_order_button.clicked.connect(self.add_blank_row)

        self.remove_customer_button = QPushButton("Smazat objednavku")
        self.remove_customer_button.setFixedWidth(170)
        self.remove_customer_button.clicked.connect(self.delete_user)
        grid_layout.addWidget(self.remove_customer_button,0,3)

        self.order_layout.addLayout(grid_layout)
        
        self.pages.addWidget(page) 
    def create_settings_page(self):
        page = QWidget()
        self.settings_layout = QVBoxLayout(page)
        self.settings_layout.addWidget(QLabel("<h2>Nastavení</h2>"
                                        "<p>Konfigurace aplikace.</p>"))
        self.settings_layout.addStretch()
        self.pages.addWidget(page)



        # -------------- funkce ------------------

    def switch_page(self,index):
        self.pages.setCurrentIndex(index)


        

# ==========================================
# 3. SPOUŠTĚCÍ BLOK
# ==========================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(NORMAL_STYLE_MAIN)
    app.setWindowIcon(QIcon("assets/logo.png"))

    while True:  # Smyčka, která drží aplikaci naživu
        login_window = AuthDialog()
        login_window.setWindowFlags(login_window.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 1. Spustíme LOGIN
        if login_window.exec() == QDialog.DialogCode.Accepted:
            role = login_window.user_role
            username = login_window.final_username 
            jmeno = login_window.final_name 
            user_id = login_window.user_id
            
            # 2. Vytvoříme HLAVNÍ OKNO podle role
            if role == "admin":
                window = AdminSystemMockup(username=username, jmeno=jmeno, id=user_id)
            else:
                window = CustommerSystemMockup(username=username, jmeno=jmeno, id=user_id)
            
            # 3. Spustíme hlavní okno a ČEKÁME
            window.show()
            
            # Tady je ten hlavní trik:
            # app.exec() se zastaví tady, dokud je hlavní okno otevřené.
            # Jakmile zavoláš self.close() v okně, kód pokračuje dál.
            app.exec() 
            
            # Pokud chceš úplně vypnout aplikaci, když se zavře okno křížkem 
            # (a ne tlačítkem Odhlásit), musel bys v logout_action nastavit příznak.
            # Pro teď se to po zavření okna prostě vrátí na login.
        else:
            # Uživatel zavřel login okno (křížkem) -> úplný konec
            break

    sys.exit()



 