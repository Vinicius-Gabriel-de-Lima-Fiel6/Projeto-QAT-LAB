from PyQt6.QtWidgets import *

import os

# Páginas (importações modulares)
from dashboard_page import DashboardPage
from substancias import SubstancesPage
from projects_page import ProjectsPage
from calculadora import CalculadoraQuimicaPage
from IA import ChatbotApp
from equipamentos import ControleEquipamentos
from ControleEstoque import ControleEstoque
from tabelas import TabelaQuimica
from graficos import GraficosA


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "LabSmartAI PRO – Sistema Inteligente de Laboratório")
        self.setMinimumSize(1300, 800)
        self.apply_stylesheet()

        # Layout principal
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Menu lateral
        menu_layout = QVBoxLayout()
        menu_frame = QFrame()
        menu_frame.setLayout(menu_layout)
        menu_frame.setFixedWidth(200)
        menu_frame.setStyleSheet("background-color: #1E1E1E;")
        layout.addWidget(menu_frame)

        # QStackedWidget: para alternar entre páginas
        self.stacked_widget = QStackedWidget()  # Corrigido aqui
        layout.addWidget(self.stacked_widget)  # Corrigido aqui

        # Páginas
        self.dashboard = DashboardPage()
        self.substancias = SubstancesPage()  # Corrigido
        self.projects = ProjectsPage()
        self.calculadora = CalculadoraQuimicaPage()
        self.IA = ChatbotApp()
        self.ControleEquipamentos = ControleEquipamentos()
        self.ControleEstoque = ControleEstoque()
        self.tabelas = TabelaQuimica()
        self.graficos = GraficosA()

        # Adicionando as páginas ao QStackedWidget
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.substancias)  # Corrigido
        self.stacked_widget.addWidget(self.projects)
        self.stacked_widget.addWidget(self.IA)
        self.stacked_widget.addWidget(self.ControleEquipamentos)
        self.stacked_widget.addWidget(self.ControleEstoque)
        self.stacked_widget.addWidget(self.calculadora)
        self.stacked_widget.addWidget(self.tabelas)
        self.stacked_widget.addWidget(self.graficos)

        # Botões do menu
        buttons = [
            ("Dashboard", self.dashboard),
            ("Cadastro de Substâncias", self.substancias),
            ("Projetos", self.projects),
            ("IA", self.IA),
            ("Controle de equipamentos", self.ControleEquipamentos),
            ("Controle do estoque", self.ControleEstoque),
            ("Calculadora química", self.calculadora),
            ("Tabelas periódica/solubilidade", self.tabelas),
            ("Gráficos", self.graficos),
        ]

        # Adicionando os botões ao menu
        for i, (name, widget) in enumerate(buttons):
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    padding: 10px;
                    font-size: 14px;
                    text-align: left;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #444444;
                    color: #00FFFF;
                }
            """)
            # Conecta o botão ao método que altera a página
            btn.clicked.connect(lambda _, index=i: self.stacked_widget.setCurrentIndex(
                index))  # Corrigido aqui
            menu_layout.addWidget(btn)

        menu_layout.addStretch()

    def apply_stylesheet(self):
        qss_path = os.path.join("style", "white_theme.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as file:
                self.setStyleSheet(file.read())
