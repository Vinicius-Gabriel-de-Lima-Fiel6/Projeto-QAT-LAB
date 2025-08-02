# pages/graphs_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sqlite3
import os
import plotly.express as px
import pandas as pd

DB_PATH = "data/lab_data.db"

class GraphsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("📊 Painel de Gráficos")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FFFF;")
        layout.addWidget(title)

        btn_gerar1 = QPushButton("📈 Gráfico: Quantidade de Substâncias")
        btn_gerar1.clicked.connect(self.gerar_grafico_substancias)
        layout.addWidget(btn_gerar1)

        btn_gerar2 = QPushButton("📘 Gráfico: Projetos por Status")
        btn_gerar2.clicked.connect(self.gerar_grafico_projetos)
        layout.addWidget(btn_gerar2)

        self.view = QWebEngineView()
        layout.addWidget(self.view)

    def gerar_grafico_substancias(self):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT nome, quantidade FROM substancias", conn)
        conn.close()

        if df.empty:
            self.view.setHtml("<h3 style='color:white'>Nenhuma substância encontrada.</h3>")
            return

        fig = px.bar(df, x="nome", y="quantidade", title="Quantidades de Substâncias no Estoque")
        fig.update_layout(template="plotly_dark")
        html = fig.to_html(include_plotlyjs='cdn')
        self.view.setHtml(html)

    def gerar_grafico_projetos(self):
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT status FROM projetos", conn)
        conn.close()

        if df.empty:
            self.view.setHtml("<h3 style='color:white'>Nenhum projeto encontrado.</h3>")
            return

        contagem = df['status'].value_counts().reset_index()
        contagem.columns = ['Status', 'Quantidade']

        fig = px.pie(contagem, values='Quantidade', names='Status', title='Distribuição de Projetos por Status')
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(template="plotly_dark")
        html = fig.to_html(include_plotlyjs='cdn')
        self.view.setHtml(html)