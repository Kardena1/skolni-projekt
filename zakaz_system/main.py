import sys
import os
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QListWidget, QTableWidget, QHeaderView, QTableWidgetItem,
                             QLineEdit, QDialog, QMessageBox,QGroupBox)
from PyQt5.QtCore import Qt, QRegularExpression
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
        self.setFixedSize(350,400)
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

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Heslo")
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)

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

        layout.addWidget(QLabel("<h2>Registrace</h2>"))

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

        
        if u in data:
            if data[u]["password"] == passw:
                self.user_role = data[u]["role"]
                self.final_username = u  # <--- TADY si to jméno uložíš pro pozdější použití
                self.accept()
                

    def handle_register(self):
        u = self.reg_user_name.text()
        p = self.reg_user_pass.text()
        jmen = self.reg_user_name
        prijm = self.reg_user_surname
        telefon = self.reg_user_number
        firma = self.reg_user_firm

        self.db_file = "users.json"

        # 1. NAČTENÍ (čteme stará data)
        with open(self.db_file, 'r', encoding="utf-8") as file:
            data = json.load(file)


        if data:
            max_id = max(uzivatel["id"] for uzivatel in data.values())
            new_id = max_id + 1

        # 2. PŘIDÁNÍ DO PAMĚTI (přidáváme přímo do načteného slovníku 'data')
        data[u] = {
            "id": new_id,  # nejvetsi id +1
            "password": p,
            "role": "zakaznik"
        }

        # 3. PŘEPSÁNÍ SOUBORU (zápis pomocí 'w' - write)
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
            



    def check_db(self):

        self.db_file = "users.json"

        if not os.path.exists(self.db_file):
            print("hello world")

            users_db = {}

            username = "admin"
            users_db[username] = {
                "id": 1,
                "password": "heslo",
                "role": "admin"
            }

            with open(self.db_file,'w') as file:
                json.dump(users_db,file,indent=4, ensure_ascii=False)

            print("users.json neexistoval. Vytvoreny novy seznam")

        else:
            print("users.json jiz existuje.")
            
        

        

        
class AdminSystemMockup(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.current_user = username

        self.setWindowTitle(f"Admin - Prihlasen jako: {username}")
        self.setFixedSize(1000,600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(20)
        self.setCentralWidget(main_widget)

    

class CustommerSystemMockup(QMainWindow):

    def __init__(self, username):
        super().__init__()

        self.current_user = username

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
            "Zakaznici"
            "Vase objednavky"
        ]

        self.sidebar.addItems(menu_items)
        self.sidebar.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        self.pages = QStackedWidget()
        main_layout.addWidget(self.pages)
        
        # vytvoreni stranek pres funkce

        self.create_dashboard_page()
        self.create_settings_page()

        self.sidebar.setCurrentRow(0)







        # -------------- stranky --------------


    def create_dashboard_page(self):
        page = QWidget()
        
        self.dashboard_layout = QVBoxLayout(page)
        self.dashboard_layout.addWidget(QLabel(f"<h2>Vitejte v systemu, {username}"))
        self.dashboard_layout.addStretch()
        self.setStyleSheet('color: red;')
        self.pages.addWidget(page)

    def create_settings_page(self):
        page = QWidget()
        self.settings_layout = QVBoxLayout(page)
        self.settings_layout.addWidget(QLabel("<h2>Nastavení</h2><p>Konfigurace aplikace.</p>"))
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
        
        if role == "admin":
            # Tady ho předáš do konstruktoru!
            window = AdminSystemMockup(username=username) 
            window.show()
            sys.exit(app.exec_())
        else:
            window = CustommerSystemMockup(username=username)
            window.show()
            sys.exit(app.exec_())
            
    else:
        # Pokud uživatel okno zavře křížkem, aplikace se ukončí
        sys.exit()


 

# hlavni_okn = MainWindow()
# hlavni_okn.show()