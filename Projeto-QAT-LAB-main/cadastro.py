# cadastro.py
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
import sqlite3

class TelaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("cadastro.ui", self)

        # Botão ENTRAR
        self.pushButton.clicked.connect(self.verificar_login)

    def verificar_login(self):
        nome = self.lineEdit.text()
        senha = self.lineEdit_2.text()

        con = sqlite3.connect("usuarios.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
        resultado = cursor.fetchone()
        con.close()

        if resultado:
            self.close()  # Fecha a tela de login

            from main_window import MainWindow
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit.setPlaceholderText("Usuário ou senha inválidos")