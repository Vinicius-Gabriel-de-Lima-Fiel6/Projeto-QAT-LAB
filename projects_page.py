# pages/projects_page.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit,QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout,QMessageBox, QHeaderView)
import sqlite3
import os
import exportPDFProjetos  # Importando a função de exportação PDF

DB_PATH = "data/lab_data.db"

class ProjectsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        title = QLabel("📚 Gerenciamento de Projetos Científicos")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FFFF;")
        self.layout().addWidget(title)

        # Campos do formulário
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nome do Projeto")

        self.input_description = QTextEdit()
        self.input_description.setPlaceholderText("Descrição / Objetivo do Projeto")

        self.input_status = QLineEdit()
        self.input_status.setPlaceholderText("Status (ex: Em andamento, Finalizado)")

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_description)
        form_layout.addWidget(self.input_status)

        btn_add = QPushButton("➕ Adicionar Projeto")
        btn_add.clicked.connect(self.add_project)
        form_layout.addWidget(btn_add)

        self.layout().addLayout(form_layout)

        # Tabela de projetos
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Status", "Descrição"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout().addWidget(self.table)

        buttons_layout = QHBoxLayout()

        btn_refresh = QPushButton("🔄 Atualizar Lista")
        btn_refresh.clicked.connect(self.load_data)
        buttons_layout.addWidget(btn_refresh)

        btn_export = QPushButton("📄 Exportar PDF") #botão para exportação
        btn_export.clicked.connect(self.export_pdf_projects)
        buttons_layout.addWidget(btn_export)
        self.layout().addLayout(buttons_layout)

        self.init_db()
        self.load_data()

    def init_db(self):
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                status TEXT,
                descricao TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_project(self):
        nome = self.input_name.text().strip()
        status = self.input_status.text().strip()
        descricao = self.input_description.toPlainText().strip()

        if not nome or not status or not descricao:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projetos (nome, status, descricao)
            VALUES (?, ?, ?)
        """, (nome, status, descricao))
        conn.commit()
        conn.close()

        self.input_name.clear()
        self.input_status.clear()
        self.input_description.clear()
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projetos")
        for i, row in enumerate(cursor.fetchall()):
            self.table.insertRow(i)
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
        conn.close()

    def export_pdf_projects(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, status, descricao FROM projetos")
        rows = cursor.fetchall()
        conn.close()

        dados = [
            {
                "id": row[0],
                "nome": row[1],
                "status": row[2],
                "descricao": row[3]
            }
            for row in rows
        ]

        exportPDFProjetos.export_pdf_projects(dados, "projetos_exportados.pdf")
        QMessageBox.information(self, "Exportação", "Projetos exportados com sucesso!")