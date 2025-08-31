from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QInputDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
import sqlite3
import os
import webbrowser
import numpy as np
import pandas as pd
from ExportPdfEstoque import export_pdf_estoque_e_consumo  # Importando a função de exportação PDF

from notifier_smtp import alerta_estoque

DB_PATH = "data/lab_data.db"
ALERT_RECIPIENTS = ["juliabcohen@icloud.com", "julia.brito.cohen@gmail.com"]  # ajustar

class ControleEstoque(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.title = QLabel("🔧 Controle de Estoque de Produtos")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #00FFFF;")
        self.layout().addWidget(self.title)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Quantidade", "Consumo Médio \nDiário", "Tempo até \nEsgotamento",
            "Comprar", "Adicionar Compras", "Adicionar Consumo", "Adicionar \nConsumo Diário"
        ])
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout().addWidget(self.table)
        self.table.setColumnWidth(8, 180)

        buttons_layout = QHBoxLayout()
        self.btn_remove = QPushButton("❌ Excluir Substância Selecionada")
        self.btn_remove.clicked.connect(self.delete_selected_substance)
        self.btn_refresh = QPushButton("🔄 Atualizar")
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_export = QPushButton("📄 Exportar PDF")
        self.btn_export.clicked.connect(self.export_pdf_estoque_e_consumo)  
        buttons_layout.addWidget(self.btn_remove)
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(self.btn_export)
        self.layout().addLayout(buttons_layout)


        self.init_db()
        self.load_data()

    def init_db(self):
        os.makedirs("data", exist_ok=True)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consumo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    
                    quantidade_consumida INTEGER,
                    data_consumo TEXT,
                    FOREIGN KEY (produto_id) REFERENCES substancias(id)
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inicializar banco de dados: {e}")
        finally:
            conn.close()

    def load_data(self):
        self.table.setRowCount(0)
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, quantidade FROM substancias")
            produtos = cursor.fetchall()

            for row_index, substancia in enumerate(produtos):
                self.table.insertRow(row_index)

                self.table.setItem(row_index, 0, QTableWidgetItem(str(substancia[0])))
                self.table.setItem(row_index, 1, QTableWidgetItem(substancia[1]))
                self.table.setItem(row_index, 2, QTableWidgetItem(str(substancia[2])))

                consumo_medio = self.calculate_average_consumption(substancia[0])
                tempo_ate_fim = substancia[2] / consumo_medio if consumo_medio > 0 else 0

                # coluna consumo médio
                item_consumo = QTableWidgetItem(f"{consumo_medio:.2f}")
                item_consumo.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, 3, item_consumo)

                # coluna tempo até acabar
                item_tempo = QTableWidgetItem(f"{tempo_ate_fim:.2f} dias")
                item_tempo.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row_index, 4, item_tempo)

                # botões
                buy_button = QPushButton("Comprar")
                buy_button.clicked.connect(lambda _, p=substancia: self.open_purchase_link(p))
                self.table.setCellWidget(row_index, 5, buy_button)

                add_buy_button = QPushButton("Adicionar \nCompra(g)")
                add_buy_button.clicked.connect(lambda _, p=substancia: self.add_quantity(p, "comprada"))
                self.table.setCellWidget(row_index, 6, add_buy_button)

                add_consume_button = QPushButton("Registrar \nConsumo(g)")
                add_consume_button.clicked.connect(lambda _, p=substancia: self.add_quantity(p, "consumo"))
                self.table.setCellWidget(row_index, 7, add_consume_button)

                add_daily_button = QPushButton("Adicionar Consumo \nDiário(g)")
                add_daily_button.clicked.connect(lambda _, p=substancia: self.add_daily_consumption(p))
                self.table.setCellWidget(row_index, 8, add_daily_button)

                # destaque e alerta
                if consumo_medio > 0 and tempo_ate_fim < 5:
                    for col in range(self.table.columnCount()):
                         item = self.table.item(row_index, col)
                         if item:
                            item.setBackground(QBrush(QColor("#FF6961")))
                    if tempo_ate_fim < 2:  # exemplo: menos de 2 dias restantes
                        try:
                            alerta_estoque(
                                destinatarios=ALERT_RECIPIENTS,
                                nome_substancia=substancia[1],
                                quantidade=f"{substancia[2]} g",
                                tempo_restante_dias=round(tempo_ate_fim, 1)
                            )
                            print(f"✔️ Alerta enviado para {ALERT_RECIPIENTS} ({substancia[1]})")
                        except Exception as e:
                            print(f"❌ Falha ao enviar alerta: {e}")

            conn.close()

        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")


    def calculate_average_consumption(self, produto_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT quantidade_consumida, data_consumo FROM consumo WHERE produto_id = ?", (produto_id,))
            data = cursor.fetchall()
            conn.close()

            if not data:
                return 0

            consumos = np.array([d[0] for d in data])
            datas = pd.to_datetime([d[1] for d in data])
            dias = datas.diff().total_seconds() / 1

            if len(dias) <= 1:
                return 0

            consumo_diario = np.sum(consumos[1:] / dias[1:]) / len(dias[1:])
            return consumo_diario
        except Exception as e:
            print(f"Erro ao calcular consumo médio: {e}")
            return 0

    def add_quantity(self, produto, tipo):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            quantidade, ok = QInputDialog.getInt(self, f"Adicionar Quantidade {tipo.capitalize()}",
                                                  f"Informe a quantidade {tipo}:", 1, 1, 100000, 1)
            if ok:
                if tipo == "comprada":
                    cursor.execute("UPDATE substancias SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto[0]))
                elif tipo == "consumo":
                    cursor.execute("INSERT INTO consumo (produto_id, quantidade_consumida, data_consumo) VALUES (?, ?, CURRENT_TIMESTAMP)", (produto[0], quantidade))
                    cursor.execute("UPDATE substancias SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto[0]))
                conn.commit()
                self.load_data()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar quantidade: {e}")
        finally:
            conn.close()

    def open_purchase_link(self, produto):
        product_name = produto[1].lower().replace(" ", "+")
        url = f"https://www.mercadolivre.com.br/search?q={product_name}"
        webbrowser.open(url)

    def delete_selected_substance(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Erro", "Selecione uma substância para excluir.")
            return

        item = self.table.item(selected_row, 0)
        if item is None:
            QMessageBox.warning(self, "Erro", "ID não encontrado.")
            return

        id_value = item.text()
        self.delete_substance_from_db(id_value)

    def delete_substance_from_db(self, id_value):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM substancias WHERE id = ?", (id_value,))
            conn.commit()
            QMessageBox.information(self, "Sucesso", "Substância excluída com sucesso!")
            self.load_data()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao excluir substância: {e}")
        finally:
            conn.close()

    def add_daily_consumption(self, produto):
        try:
            quantidade, ok = QInputDialog.getInt(self, "Adicionar Consumo Diário", "Informe a quantidade consumida hoje:", 1, 1, 100000, 1)
            if ok:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO consumo (produto_id, quantidade_consumida, data_consumo) VALUES (?, ?, CURRENT_TIMESTAMP)", (produto[0], quantidade))
                cursor.execute("UPDATE substancias SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto[0]))
                conn.commit()
                self.load_data()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar consumo diário: {e}")
        finally:
   
            conn.close()

    def export_pdf_estoque_e_consumo(self):
        try:
            from ExportPdfEstoque import export_pdf_estoque_e_consumo

            produtos = []
            for row in range(self.table.rowCount()):
                produto_id = self.table.item(row, 0).text()
                nome = self.table.item(row, 1).text()
                quantidade = float(self.table.item(row, 2).text())
                consumo_medio = float(self.table.item(row, 3).text())
                tempo_ate_fim = self.table.item(row, 4).text()

                produtos.append({
                    "id": produto_id,
                    "nome": nome,
                    "quantidade": quantidade,
                    "consumo_medio": consumo_medio,
                    "tempo_ate_fim": tempo_ate_fim
                })

            consumos = []
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, s.nome, c.quantidade_consumida, c.data_consumo
                FROM consumo c
                LEFT JOIN substancias s ON c.produto_id = s.id
            """)
            consumos_rows = cursor.fetchall()
            for row in consumos_rows:
                consumos.append({
                    "id": row[0],
                    "produto_nome": row[1],
                    "quantidade_consumida": row[2],
                    "data_consumo": row[3]
                })
            conn.close()

            export_pdf_estoque_e_consumo(produtos, consumos, "estoque_e_consumos.pdf")
            QMessageBox.information(self, "Exportação", "PDF exportado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao exportar PDF", str(e))