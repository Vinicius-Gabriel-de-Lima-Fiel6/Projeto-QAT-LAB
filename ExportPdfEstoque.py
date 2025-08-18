from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf_estoque_e_consumo(produtos, consumos, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título Estoque
    title_estoque = Paragraph("Estoque Atual", styles['Title'])
    elements.append(title_estoque)
    elements.append(Spacer(1, 8))

    # Tabela Estoque
    table_data_estoque = [["ID", "Nome", "Quantidade", "Consumo Médio Diário", "Tempo até Esgotamento (dias)"]]
    for row in produtos:
        table_data_estoque.append([
            row.get('id', ''),
            row.get('nome', ''),
            row.get('quantidade', ''),
            f"{row.get('consumo_medio', 0):.2f}",
            f"{row.get('tempo_ate_fim', 0):.2f}"
        ])
    table_estoque = Table(table_data_estoque, colWidths=[30, 90, 60, 90, 110])
    table_estoque.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7), 
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table_estoque)
    elements.append(Spacer(1, 18))

    # Título Consumos
    title_consumo = Paragraph("Histórico de Consumo", styles['Title'])
    elements.append(title_consumo)
    elements.append(Spacer(1, 8))

    # Tabela Consumos
    table_data_consumo = [["ID", "Produto", "Quantidade Consumida", "Data do Consumo"]]
    for row in consumos:
        table_data_consumo.append([
            row.get('id', ''),
            row.get('produto_nome', ''),
            row.get('quantidade_consumida', ''),
            row.get('data_consumo', '')
        ])
    table_consumo = Table(table_data_consumo, colWidths=[30, 90, 90, 110])
    table_consumo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table_consumo)

    doc.build(elements)

if __name__ == "__main__":
    import sqlite3
    import numpy as np

    DB_PATH = "data/lab_data.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Buscar produtos e calcular consumo médio e tempo até fim
    cursor.execute("SELECT id, nome, quantidade FROM substancias")
    produtos_rows = cursor.fetchall()
    produtos = []
    for row in produtos_rows:
        produto_id = row[0]
        # Calcular consumo médio
        cursor.execute("SELECT quantidade_consumida, data_consumo FROM consumo WHERE produto_id = ?", (produto_id,))
        data = cursor.fetchall()
        if data:
            consumos = np.array([d[0] for d in data])
            import pandas as pd
            datas = pd.to_datetime([d[1] for d in data])
            dias = datas.diff().total_seconds() / (60*60*24)
            if len(dias) > 1:
                consumo_medio = np.sum(consumos[1:] / dias[1:]) / len(dias[1:])
            else:
                consumo_medio = 0
        else:
            consumo_medio = 0
        quantidade = row[2]
        tempo_ate_fim = quantidade / consumo_medio if consumo_medio > 0 else 0
        produtos.append({
            "id": row[0],
            "nome": row[1],
            "quantidade": quantidade,
            "consumo_medio": consumo_medio,
            "tempo_ate_fim": tempo_ate_fim
        })

    # Buscar histórico de consumo
    cursor.execute("""
        SELECT c.id, s.nome, c.quantidade_consumida, c.data_consumo
        FROM consumo c
        LEFT JOIN substancias s ON c.produto_id = s.id
    """)
    consumos_rows = cursor.fetchall()
    consumos = [
        {
            "id": row[0],
            "produto_nome": row[1],
            "quantidade_consumida": row[2],
            "data_consumo": row[3]
        }
        for row in consumos_rows
    ]

    conn.close()

    export_pdf_estoque_e_consumo(produtos, consumos, "estoque_e_consumos.pdf")
