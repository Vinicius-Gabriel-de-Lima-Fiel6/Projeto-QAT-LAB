from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
import sqlite3
import os

DB_PATH = "data/lab_data.db"

class ControleEquipamentos(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        title = QLabel("🔧 Controle de Equipamentos")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00FFFF;")
        self.layout().addWidget(title)

        # Formulário de Cadastro de Equipamentos
        self.inputs = {}
        form_layout = QHBoxLayout()
        for field in ["Nome", "Tipo", "Status", "Data da Última Manutenção", "localizacao", "responsavel", "Categoria"]:
            input_field = QLineEdit()
            input_field.setPlaceholderText(field)
            self.inputs[field.lower()] = input_field
            form_layout.addWidget(input_field)

        btn_add = QPushButton("➕ Adicionar Equipamento")
        btn_add.clicked.connect(self.add_equipment)
        form_layout.addWidget(btn_add)
        self.layout().addLayout(form_layout)

        # Tabela de Equipamentos
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "Tipo", "Status", "Última Manutenção", "localizacao", "responsavel"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.layout().addWidget(self.table)

        # Histórico de Manutenções
        self.history_layout = QVBoxLayout()
        self.history_label = QLabel("🔧 Histórico de Manutenções:")
        self.history_layout.addWidget(self.history_label)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(
            ["ID", "Equipamento", "Data da Manutenção", "Descrição"]
        )
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_layout.addWidget(self.history_table)

        # Formulário de Cadastro de Manutenção
        self.inputs_history = {}
        history_form_layout = QHBoxLayout()
        for field in ["Equipamento", "Data da Manutenção", "Descrição"]:
            input_field = QLineEdit()
            input_field.setPlaceholderText(field)
            self.inputs_history[field.lower()] = input_field
            history_form_layout.addWidget(input_field)

        btn_add_history = QPushButton("➕ Adicionar Manutenção")
        btn_add_history.clicked.connect(self.add_maintenance)
        history_form_layout.addWidget(btn_add_history)
        self.layout().addLayout(self.history_layout)
        self.layout().addLayout(history_form_layout)

        # Botões Inferiores
        buttons_layout = QHBoxLayout()
        self.btn_remove = QPushButton("❌ Remover Equipamento Selecionado")
        self.btn_remove.clicked.connect(self.remove_selected)
        buttons_layout.addWidget(self.btn_remove)
        self.btn_refresh = QPushButton("🔄 Atualizar Lista")
        self.btn_refresh.clicked.connect(self.load_data)
        buttons_layout.addWidget(self.btn_refresh)
        self.layout().addLayout(buttons_layout)

        # Inicialização
        self.init_db()
        self.load_data()

    def init_db(self):
        """Função para inicializar o banco de dados"""
        os.makedirs("data", exist_ok=True)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS equipamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    tipo TEXT,
                    status TEXT,
                    ultima_manutencao TEXT,
                    localizacao TEXT,
                    responsavel TEXT,
                    categoria TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS manutencao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equipamento_id INTEGER,
                    data_manutencao TEXT,
                    descricao TEXT,
                    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
                )
            """)
            conn.commit()
            print("Banco de dados inicializado com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao inicializar o banco de dados: {e}")
        finally:
            conn.close()

    def add_equipment(self):
        """Função para adicionar um novo equipamento"""
        data = {k: v.text().strip() for k, v in self.inputs.items()}
        print(f"Dados coletados: {data}")  # Diagnóstico para conferir os dados coletados
        if not all(data.values()):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO equipamentos (nome, tipo, status, ultima_manutencao, localizacao, responsavel, categoria)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data["nome"], data["tipo"], data["status"], data["data da última manutenção"], data["localizacao"], 
                data["responsavel"], data["categoria"]
            ))
            conn.commit()
            print("Equipamento adicionado com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao adicionar equipamento: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar equipamento: {e}")
        finally:
            conn.close()

        self.clear_inputs()
        self.load_data()

    def add_maintenance(self):
        """Função para adicionar manutenção ao equipamento"""
        data = {k: v.text().strip() for k, v in self.inputs_history.items()}
        if not all(data.values()):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return

        equipamento_nome = data["equipamento"]
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM equipamentos WHERE nome = ?", (equipamento_nome,))
            equipamento_id = cursor.fetchone()
            if equipamento_id is None:
                QMessageBox.warning(self, "Erro", "Equipamento não encontrado.")
                return

            cursor.execute("""
                INSERT INTO manutencao (equipamento_id, data_manutencao, descricao)
                VALUES (?, ?, ?)
            """, (equipamento_id[0], data["data da manutenção"], data["descrição"]))
            conn.commit()
            print("Manutenção registrada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao registrar manutenção: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao registrar manutenção: {e}")
        finally:
            conn.close()

        self.clear_inputs_history()
        self.load_data()

    def load_data(self):
        """Carregar dados dos equipamentos e histórico de manutenções"""
        print("Carregando dados...")
        self.table.setRowCount(0)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipamentos")
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.table.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

            self.history_table.setRowCount(0)
            cursor.execute("SELECT * FROM manutencao")
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.history_table.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.history_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao carregar dados: {e}")
        finally:
            conn.close()

    def remove_selected(self):
        """Remover o equipamento selecionado"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Erro", "Nenhuma linha selecionada.")
            return

        id_value = self.table.item(selected, 0).text()
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM equipamentos WHERE id = ?", (id_value,))
            conn.commit()
            print(f"Equipamento {id_value} removido com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao remover equipamento: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao remover equipamento: {e}")
        finally:
            conn.close()

        self.load_data()

    def clear_inputs(self):
        """Limpar os campos de entrada"""
        for field in self.inputs.values():
            field.clear()

    def clear_inputs_history(self):
        """Limpar os campos de histórico de manutenção"""
        for field in self.inputs_history.values():
            field.clear()