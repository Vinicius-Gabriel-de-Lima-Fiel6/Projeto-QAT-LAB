import sqlite3
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QSpinBox
)

# Caminho do banco de dados
DB_PATH = "data/lab_data.db"

class SubstancesPage(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.setLayout(QVBoxLayout())

        # Título
        title = QLabel("🔬 Cadastro e Gerenciamento de Substâncias")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FFFF;")
        self.layout().addWidget(title)

        # Layout dos campos de entrada
        self.inputs = {}
        form_layout = QHBoxLayout()
        
        # Campos de entrada
        for field in ["Nome", "Finalidade", "concentracao", "Quantidade", "Validade"]:
            input_field = QLineEdit()
            input_field.setPlaceholderText(field)
            self.inputs[field.lower()] = input_field
            form_layout.addWidget(input_field)

        # Botão de adicionar substância
        btn_add = QPushButton("➕ Adicionar")
        btn_add.clicked.connect(self.add_substance)
        form_layout.addWidget(btn_add)
        self.layout().addLayout(form_layout)

        # Tabela de substâncias
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Finalidade", "Concentração", "Quantidade", "Validade"])#######
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.layout().addWidget(self.table)

        # Botões para remover e atualizar
        buttons_layout = QHBoxLayout()
        self.btn_remove = QPushButton("❌ Remover Selecionado")
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_refresh = QPushButton("🔄 Atualizar")
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_export = QPushButton("📄 Exportar PDF")
        self.btn_export.clicked.connect(self.export_pdf_substances)
        buttons_layout.addWidget(self.btn_remove)
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(self.btn_export)
        self.layout().addLayout(buttons_layout)

        # Inicializa banco de dados
        self.init_db()
        self.load_data()

    def init_db(self):
        """Cria o banco de dados e a tabela se não existirem"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS substancias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                finalidade TEXT,
                concentracao TEXT,
                quantidade REAL,
                validade TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_substance(self):
        """Adicionar substância ao banco de dados"""
        data = {k: v.text().strip() for k, v in self.inputs.items()}
        
        # Verifica se todos os campos estão preenchidos
        if not all(data.values()):
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            # Valida se a quantidade é um número válido
            quantidade = float(data["quantidade"])
        except ValueError:
            QMessageBox.warning(self, "Erro", "Quantidade deve ser um número válido.")
            return

        try:
            # Conectar ao banco de dados e inserir os dados
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO substancias (nome, finalidade, concentracao, quantidade, validade)
                VALUES (?, ?, ?, ?, ?)
            """, (data["nome"], data["finalidade"], data["concentracao"], quantidade, data["validade"]))
            conn.commit()
            conn.close()

            # Limpar campos de entrada e atualizar a tabela
            self.clear_inputs()
            self.load_data()

        except Exception as e:
            QMessageBox.critical(self, "Erro Crítico", f"Erro ao adicionar substância:\n{e}")

    def load_data(self):
        """Carregar dados da tabela do banco de dados"""
        self.table.setRowCount(0)  # Limpa a tabela
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM substancias")
        for row_index, row in enumerate(cursor.fetchall()):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        conn.close()

    def remove_selected(self):
        """Remover a substância selecionada da tabela"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erro", "Nenhuma linha selecionada.")
            return
        
        # Obtém o ID da substância selecionada
        item_id = self.table.item(selected_row, 0).text()

        # Conectar ao banco de dados e remover o item
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM substancias WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        # Atualiza a tabela após remoção
        self.load_data()

    def clear_inputs(self):
        """Limpar os campos de entrada"""
        for field in self.inputs.values():
            field.clear()
    
    def export_pdf_substances(self):
        # Exportar dados de substâncias para um arquivo PDF
        from exportPdfSubstancias import export_pdf_substances
        
        # Coleta os dados da tabela
        data = []
        for row in range(self.table.rowCount()):
            row_data = {
                "id": self.table.item(row, 0).text(),
                "nome": self.table.item(row, 1).text(),
                "finalidade": self.table.item(row, 2).text(),
                "concentracao": self.table.item(row, 3).text(),
                "quantidade": self.table.item(row, 4).text(),
                "validade": self.table.item(row, 5).text()
            }
            data.append(row_data)

        # Exporta os dados para PDF
        export_pdf_substances(data, "substancias_exportadas.pdf")
        QMessageBox.information(self, "Exportação", "Substâncias exportadas com sucesso!")