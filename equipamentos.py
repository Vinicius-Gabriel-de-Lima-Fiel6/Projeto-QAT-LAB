from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,QMenu,QWidgetAction,QFileDialog
)
from PyQt6.QtCore import Qt
import sqlite3
import os
from exportPdFEquipamentos import export_pdf_equipments_and_maintenance

from PyQt6.QtWidgets import QDialog
from matplotlib.backends.backend_qtagg import FigureCanvas
import pandas as pd
import matplotlib.pyplot as plt

import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

from PyQt6.QtWidgets import QApplication

from PyQt6.QtCore import QDate,Qt

import sys
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
        # botão de exportação PDF
        self.btn_export = QPushButton ("📄 Exportar PDF")
        self.btn_export.clicked.connect(self.exportar_pdf_equipamentos)
        buttons_layout.addWidget(self.btn_export)
        #csv
        export_button = QPushButton("📁Exportar para Sistema Operacional")
        export_button.setMenu(self.create_export_menu())
        self.layout().addWidget(export_button)
         #gráficos
        graph_button = QPushButton("📊 Gráficos")
        graph_button.setMenu(self.create_graph_menu())  # Menu de gráficos
        buttons_layout.addWidget(graph_button)
        # Adicionando os botões ao layout principal
        self.layout().addLayout(buttons_layout)
        # Layout para os gráficos
        self.graph_layout = QVBoxLayout()
        self.layout().addLayout(self.graph_layout)
    

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
    def search_data(self):
        """Função para filtrar os dados com base na pesquisa"""
        search_text = self.search_input.text().lower()
        self.table.setRowCount(0)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM equipamentos WHERE nome LIKE ?", ('%' + search_text + '%',))
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.table.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        except sqlite3.Error as e:
            print(f"Erro ao carregar dados: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao carregar dados: {e}")
        finally:
            conn.close()

    def filter_data(self):
        """Função para filtrar os dados com base no filtro de status"""
        selected_filter = self.filter_combo.currentText()  # Obtém o texto selecionado do combo box
        self.table.setRowCount(0)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Condição para aplicar o filtro corretamente
            if selected_filter == "Todos":
                cursor.execute("SELECT * FROM equipamentos")
            else:
                cursor.execute("SELECT * FROM equipamentos WHERE status = ?", (selected_filter,))

            # Carregar os dados filtrados
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.table.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados filtrados: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao carregar dados filtrados: {e}")
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
    def create_export_menu(self):
        export_menu = QMenu(self)

    # Usando QWidgetAction para permitir o uso de widgets no menu
        export_csv_action = QWidgetAction(self)
        export_pdf_action = QWidgetAction(self)

    # Criando os widgets (botões) para o menu
        export_csv_button = QPushButton("Exportar para CSV")
        export_pdf_button = QPushButton("Exportar para PDF")

    # Conectando os botões aos métodos de exportação
        export_csv_button.clicked.connect(self.export_to_csv)
        export_pdf_button.clicked.connect(self.export_to_pdf)

    # Associando os botões ao QWidgetAction
        export_csv_action.setDefaultWidget(export_csv_button)
        export_pdf_action.setDefaultWidget(export_pdf_button)

    # Adicionando as ações ao menu
        export_menu.addAction(export_csv_action)
        export_menu.addAction(export_pdf_action)
    
        return export_menu
    def export_to_pdf(self):
       try:
        c = canvas.Canvas("equipamentos_exportados.pdf", pagesize=letter)
        width, height = letter

        c.setFont("Helvetica", 12)
        c.drawString(30, height - 40, "Relatório de Equipamentos - Empresa XYZ")
        c.drawString(30, height - 30, "Equipamentos - Relatório")

        # Cabeçalho da tabela
        header = ["ID", "Nome", "Tipo", "Status", "Última Manutenção", "Localização", "Responsável"]
        x_offset = 30
        y_offset = height - 60
        for i, text in enumerate(header):
            c.drawString(x_offset + (i * 80), y_offset, text)

        # Adicionando os dados da tabela ao PDF
        y_offset -= 20
        for row_index in range(self.table.rowCount()):
            for col_index in range(self.table.columnCount()):
                item = self.table.item(row_index, col_index)
                value = item.text() if item else ""
                c.drawString(x_offset + (col_index * 80), y_offset, value)
                y_offset -= 20

        # Exibe um diálogo para salvar o arquivo PDF
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo PDF", "", "PDF Files (*.pdf)")

        if not file_name:  # Se o usuário cancelar
            return

        # Salvar o PDF no arquivo escolhido
        c.save()

        QMessageBox.information(self, "Sucesso", "Dados exportados para PDF com sucesso!")
        
       except Exception as e:
        QMessageBox.warning(self, "Erro", f"Erro ao exportar para PDF: {e}")
        try:
            c = canvas.Canvas("equipamentos_exportados.pdf", pagesize=letter)
            width, height = letter

            c.setFont("Helvetica", 12)
            c.drawString(30, height - 30, "Equipamentos - Relatório")

        # Cabeçalho da tabela
            header = ["ID", "Nome", "Tipo", "Status", "Última Manutenção", "Localização", "Responsável"]
            x_offset = 30
            y_offset = height - 60
            for i, text in enumerate(header):
                c.drawString(x_offset + (i * 80), y_offset, text)

        # Adicionando os dados da tabela ao PDF
                y_offset -= 20
            for row_index in range(self.table.rowCount()):
                for col_index in range(self.table.columnCount()):
                    item = self.table.item(row_index, col_index)
                    value = item.text() if item else ""
                    c.drawString(x_offset + (col_index * 80), y_offset, value)
                    y_offset -= 20

        # Finalizar o arquivo PDF
                
                c.drawString(30, 30, f"Página {c.getPageNumber()}")
                c.save()

            QMessageBox.information(self, "Sucesso", "Dados exportados para PDF com sucesso!")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao exportar para PDF: {e}")
    def export_to_csv(self):
       try:
        rows = []
        for row_index in range(self.table.rowCount()):
            row_data = []
            for col_index in range(self.table.columnCount()):
                item = self.table.item(row_index, col_index)
                row_data.append(item.text() if item else "")
            rows.append(row_data)

        # Exibe um diálogo para salvar o arquivo CSV
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo CSV", "", "CSV Files (*.csv)")

        if not file_name:  # Se o usuário cancelar
            return

        # Salvar os dados no arquivo CSV escolhido
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nome", "Tipo", "Status", "Última Manutenção", "Localização", "Responsável"])  # Cabeçalho
            writer.writerows(rows)

        QMessageBox.information(self, "Sucesso", "Dados exportados para CSV com sucesso!")
       except Exception as e:
        QMessageBox.warning(self, "Erro", f"Erro ao exportar para CSV: {e}")

    def exportar_pdf_equipamentos(self):
        import sqlite3
        DB_PATH = "data/lab_data.db"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

    # Buscar equipamentos
        cursor.execute("SELECT id, nome, tipo, status, ultima_manutencao, localizacao, responsavel, categoria FROM equipamentos")
        equipamentos_rows = cursor.fetchall()
        equipamentos = [
        {
            "id": row[0],
            "nome": row[1],
            "tipo": row[2],
            "status": row[3],
            "ultima_manutencao": row[4],
            "localizacao": row[5],
            "responsavel": row[6],
            "categoria": row[7]
        }
        for row in equipamentos_rows
       ]

    # Buscar manutenções (com nome do equipamento)
        cursor.execute("""
        SELECT m.id, e.nome, m.data_manutencao, m.descricao
        FROM manutencao m
        LEFT JOIN equipamentos e ON m.equipamento_id = e.id
        """)
        manutencoes_rows = cursor.fetchall()
        manutencoes = [
        {
            "id": row[0],
            "equipamento_nome": row[1],
            "data_manutencao": row[2],
            "descricao": row[3]
        }
        for row in manutencoes_rows
       ]

        conn.close()

        export_pdf_equipments_and_maintenance(equipamentos, manutencoes, "equipamentos_e_manutencoes.pdf")
        QMessageBox.information(self, "Exportação", "Equipamentos e manunteções exportados com sucesso!")
    def save_preferences(self):
        preferences = {
        "default_path": "C:/meu/diretorio",
        "default_format": "CSV"
    }
        with open("preferences.json", "w") as file:
            json.dump(preferences, file)

    def load_preferences(self):
        try:
            with open("preferences.json", "r") as file:
                preferences = json.load(file)
                return preferences
        except FileNotFoundError:
            return None
    def create_graph_menu(self):
        graph_menu = QMenu(self)

       # Criar ações para o menu (tipos de gráficos)
        bar_graph_action = QWidgetAction(self)
        pie_chart_action = QWidgetAction(self)
        stacked_bar_graph_action = QWidgetAction(self)
        line_graph_action = QWidgetAction(self)
        area_graph_action = QWidgetAction(self)
        scatter_graph_action = QWidgetAction(self)
        histogram_graph_action = QWidgetAction(self)
  

        # Criando os botões para o menu
        bar_graph_button = QPushButton("Gráfico de Barras")
        pie_chart_button = QPushButton("Gráfico de Pizza")
        stacked_bar_graph_button = QPushButton("Gráfico de Barras Empilhadas")
        line_graph_button = QPushButton("Gráfico de Linhas")
        area_graph_button = QPushButton("Gráfico de Área")
        scatter_graph_button = QPushButton("Gráfico de Dispersão")
        histogram_graph_button = QPushButton("Histograma")
       

        # Conectando os botões aos métodos de geração de gráficos
        bar_graph_button.clicked.connect(lambda: self.generate_graph("Gráfico de Barras"))
        pie_chart_button.clicked.connect(lambda: self.generate_graph("Gráfico de Pizza"))
        stacked_bar_graph_button.clicked.connect(lambda: self.generate_graph("Gráfico de Barras Empilhadas"))
        line_graph_button.clicked.connect(lambda: self.generate_graph("Gráfico de Linhas"))
        area_graph_button.clicked.connect(lambda: self.generate_graph("Gráfico de Área"))
        scatter_graph_button.clicked.connect(lambda: self.generate_graph("Gráfico de Dispersão"))
        histogram_graph_button.clicked.connect(lambda: self.generate_graph("Histograma"))
 

        # Associando os botões aos QWidgetAction
        bar_graph_action.setDefaultWidget(bar_graph_button)
        pie_chart_action.setDefaultWidget(pie_chart_button)
        stacked_bar_graph_action.setDefaultWidget(stacked_bar_graph_button)
        line_graph_action.setDefaultWidget(line_graph_button)
        area_graph_action.setDefaultWidget(area_graph_button)
        scatter_graph_action.setDefaultWidget(scatter_graph_button)
        histogram_graph_action.setDefaultWidget(histogram_graph_button)
   
 
        # Adicionando as ações ao menu
        graph_menu.addAction(bar_graph_action)
        graph_menu.addAction(pie_chart_action)
        graph_menu.addAction(stacked_bar_graph_action)
        graph_menu.addAction(line_graph_action)
        graph_menu.addAction(area_graph_action)
        graph_menu.addAction(scatter_graph_action)
        graph_menu.addAction(histogram_graph_action)
        
        
        # --- Dashboard (tipo Power BI) ---
        dashboard_action = QWidgetAction(self)
        dashboard_button = QPushButton("📊 Dashboard (tipo Power BI)")
        dashboard_button.clicked.connect(self.open_dashboard)
        dashboard_action.setDefaultWidget(dashboard_button)
        graph_menu.addSeparator()
        graph_menu.addAction(dashboard_action)


        return graph_menu
    def show_graph(self, fig):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gráfico")
        dialog.setMinimumSize(600, 400)  # Definindo o tamanho da janela
        layout = QVBoxLayout()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        dialog.setLayout(layout)
        dialog.exec()
    def generate_graph(self, graph_type):
        try:
            conn = sqlite3.connect('data/lab_data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT tipo, COUNT(*) FROM equipamentos GROUP BY tipo")
            data = cursor.fetchall()
            conn.close()
            tipos = [row[0] for row in data]
            contagens = [row[1] for row in data]
            if graph_type == "Gráfico de Barras":
                self.create_bar_graph(tipos, contagens)
            elif graph_type == "Gráfico de Pizza":
                self.create_pie_chart(tipos, contagens)
            elif graph_type == "Gráfico de Barras Empilhadas":
                self.create_stacked_bar_graph(tipos, contagens)
            elif graph_type == "Gráfico de Linhas":
                self.create_line_graph(tipos, contagens)
            elif graph_type == "Gráfico de Área":
                self.create_area_graph(tipos, contagens)
            elif graph_type == "Gráfico de Dispersão":
                self.create_scatter_graph(tipos, contagens)
            elif graph_type == "Histograma":
                self.create_histogram(tipos)
      
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao gerar gráfico: {e}")
    def create_bar_graph(self, tipos, contagens):
        fig, ax = plt.subplots()
        ax.bar(tipos, contagens)
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Quantidade de Equipamentos por Tipo')
        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_pie_chart(self, tipos, contagens):
        fig, ax = plt.subplots()
        ax.pie(contagens, labels=tipos, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Garantir que o gráfico de pizza tenha formato circular
        ax.set_title('Distribuição de Equipamentos por Tipo')

        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_stacked_bar_graph(self, tipos, contagens):
        fig, ax = plt.subplots()
        ax.bar(tipos, contagens, label="Equipamentos", color='r')
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Equipamentos por Tipo e Status')
        ax.legend()
        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_line_graph(self, tipos, contagens):
   
        fig, ax = plt.subplots()
        ax.plot(tipos, contagens, marker='o')
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Quantidade de Equipamentos por Tipo (Gráfico de Linhas)')

        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_area_graph(self, tipos, contagens):
        fig, ax = plt.subplots()
        ax.fill_between(tipos, contagens, color="skyblue", alpha=0.4)
        ax.plot(tipos, contagens, color="Slateblue", alpha=0.6)
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Equipamentos por Tipo (Gráfico de Área)')

        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_scatter_graph(self, tipos, contagens):
        fig, ax = plt.subplots()
        ax.scatter(tipos, contagens)
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Equipamentos por Tipo (Gráfico de Dispersão)')

        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def create_histogram(self, tipos):
        fig, ax = plt.subplots()
        ax.hist(tipos, bins=10)
        ax.set_xlabel('Tipo de Equipamento')
        ax.set_ylabel('Quantidade')
        ax.set_title('Distribuição de Equipamentos (Histograma)')

        self.show_graph(fig)  # Exibindo o gráfico em um pop-up
    def _apply_filters(self, df_eq: pd.DataFrame, df_m: pd.DataFrame):
        status = self.cb_status.currentText()
        if status != "Todos":
            df_eq = df_eq[df_eq["status"] == status].copy()
        if not df_m.empty:
            di = self.dt_ini.date().toPyDate()  # data inicial
            df = self.dt_fim.date().toPyDate()  # data final
            df_m = df_m[(df_m["data_manutencao"] >= di) & (df_m["data_manutencao"] <= df)].copy()

        return df_eq, df_m
    def open_dashboard(self):
        import webbrowser
        webbrowser.open("https://app.powerbi.com/")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window =ControleEquipamentos()
    window.show()
    sys.exit(app.exec())
