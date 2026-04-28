import sys
import os
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QListWidget, QTableWidget, QHeaderView, QTableWidgetItem,
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
                outline: 0;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-bottom: 1px solid #374151;
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
        """

data = []
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# with open("data.json",'r') as file:
#     data = json.load(file)
    
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
        with open(self.db_file, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)    
    # def handle_register(self):
    #     print("hello world")
    #     u = self.reg_user_name.text()
    #     p = self.reg_user_pass.text()
    #     p_ver = self.reg_user_ver.text()

    #     self.db_file = "users.json"

    #     with open(self.db_file,'r') as file:
    #         data = json.load(file)

    #         users_db = {}

    #         username = u
    #         users_db[username] = {
    #             "id": len(users_db),
    #             "password": p,
    #             "role": "zakaznik"
    #         }

    #         with open(self.db_file,'a') as file:
    #             json.dump(users_db,file,indent=4, ensure_ascii=False)
                
        

        # if u in data:
        #         msg = QMessageBox()
        #         msg.setIcon(QMessageBox.Information)
        #         msg.setWindowTitle("Oznameni")
        #         msg.setText(f"Toto uzivatelske jmeno uz existuje.")
        #         msg.setStandardButtons(QMessageBox.Ok)
        #         msg.exec_()
            


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
            "Logy"
        ]
        self.sidebar.addItems(menu_items)
        self.sidebar.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)

        # ----- VYTVORENI STRANEK ------
        self.create_customers_list_page()
        self.create_orders_page()
        self.create_stats_page()
        self.create_logs_page()


        self.sidebar.setCurrentRow(0)


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

        with open(self.user_file,'w',encoding="utf-8") as file:
            json.dump(new_data,file,indent=7)

            print("Data byla uspesne ulozena!")


            
    def create_customers_list_page(self):
        page = QWidget()
        self.customer_layout = QVBoxLayout(page)
        self.customer_layout.addWidget(QLabel(f"Vitejte"))


        self.table = QTableWidget(0,8)
        self.table.setHorizontalHeaderLabels(["ID","Username","Jmeno","Prijmeni",'Telefonni Cislo','Firma','Heslo','role'])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedWidth(750)

        for i in range(7):
            self.table.setColumnWidth(i,200)

        self.load_data_button = QPushButton("klikni na me")
        self.load_data_button.clicked.connect(self.load_custommer_data)
        self.load_data_button.setFixedWidth(200)
        self.customer_layout.addWidget(self.load_data_button)



        self.save_data_button = QPushButton("Ulozit zmeny")
        self.save_data_button.clicked.connect(self.save_custommer_data)
        self.save_data_button.setFixedWidth(200)
        self.customer_layout.addWidget(self.save_data_button)

        self.add_new_row_button = QPushButton("Přidat nového uživatele")
        self.add_new_row_button.clicked.connect(self.add_blank_row)
        self.add_new_row_button.setFixedWidth(200)
        self.customer_layout.addWidget(self.add_new_row_button)




        self.customer_layout.addWidget(self.table)
        self.customer_layout.addStretch()


        # self.main_grid_layout = QtWidgets.QGridLayout()
        # self.grid_layout1 = QtWidgets.QGridLayout()
        # self.grid_layout1.setObjectName("Gridlayout1")
        # self.grid_layout1.addWidget(QLabel("test1"), 0, 0)
        # self.grid_layout1.addWidget(QLabel("test2"), 0, 1)
        # self.grid_layout1.addWidget(QLabel("test3"), 1, 0)
        # self.grid_layout1.addWidget(QLabel("test4"), 1, 1)
        # container = QtWidgets.QWidget()
        # container.setObjectName("MojeOblast")
        # container.setLayout(self.grid_layout1)

        # self.grid_layout2 = QtWidgets.QGridLayout()
        # self.grid_layout2.addWidget(QLabel("test1"),0,0)
        # self.grid_layout2.addWidget(QLabel("test2"),0,1)
        # self.grid_layout2.addWidget(QLabel("test3"),1,0)
        # self.grid_layout2.addWidget(QLabel("test4"),1,1)

        # self.main_grid_layout.addWidget(container, 0, 0)
        # self.customer_layout.addLayout(self.main_grid_layout)



        self.pages.addWidget(page)

        

    def create_orders_page(self):
        page = QWidget()
        self.customer_layout = QVBoxLayout(page)
        self.customer_layout.addWidget(QLabel(f"Vitejte1"))
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

        # levy navigacni panel
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)

        menu_items = [
            "Prehled",
            "Moje zakazky",
            "Vytvořit novou zakázku",
            "Můj profil",
            "Podpora/Kontakt"
        ]

        self.sidebar.addItems(menu_items)
        self.sidebar.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # vytvoreni stranek pres funkce

        self.create_dashboard_page()
        self.create_order_page()
        self.create_settings_page()

        self.sidebar.setCurrentRow(0)







        # -------------- stranky --------------


    def create_dashboard_page(self):
        page = QWidget()
        
        self.dashboard_layout = QVBoxLayout(page)
        self.dashboard_layout.addWidget(QLabel(f"<h2>Vitejte v systemu, {jmeno}"))
        self.dashboard_layout.addStretch()
        self.setStyleSheet('color: red;')
        self.pages.addWidget(page)

    def create_order_page(self):
        page = QWidget()
        self.order_layout = QVBoxLayout(page)
        self.label_welcome = QLabel("<h1> Tady muzete uvidet svoje zakazky a udelat novou objednavku.</h1>")
        self.order_layout.addWidget(self.label_welcome)
        self.order_layout.addStretch()
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
    login_window = AuthDialog()
    app.setStyleSheet(NORMAL_STYLE_MAIN)
    
    if login_window.exec_() == QDialog.Accepted:
        role = login_window.user_role
        # Získání jména, které jsme si uložili v handle_login
        username = login_window.final_username 
        jmeno = login_window.final_name 
        id = login_window.user_id
        
        if role == "admin":
            # Tady ho předáš do konstruktoru!
            window = AdminSystemMockup(username=username,jmeno=jmeno,id=id) 
            window.show()
            sys.exit(app.exec_())
        else:
            window = CustommerSystemMockup(username=username,jmeno=jmeno,id=id)
            window.show()
            sys.exit(app.exec_())
            
    else:
        # Pokud uživatel okno zavře křížkem, aplikace se ukončí
        sys.exit()


 