from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf_substances(data, filename):
    """
    Exportar dados de substâncias para um arquivo PDF.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("Substâncias", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  
    table_data = [["ID", "Nome", "Finalidade", "Concentração", "Quantidade", "Validade"]]
    for row in data:
        table_data.append([
            row.get('id', ''),
            row.get('nome', ''),
            row.get('finalidade', ''),
            row.get('concentracao', ''),
            row.get('quantidade', ''),
            row.get('validade', '')
        ])
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    doc.build(elements)

if __name__ == "__main__":
    import sqlite3

    DB_PATH = "data/lab_data.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, finalidade, concentracao, quantidade, validade FROM substancias")
    rows = cursor.fetchall()
    conn.close()

    dados = [
        {
            "id": row[0],
            "nome": row[1],
            "finalidade": row[2],
            "concentracao": row[3],
            "quantidade": row[4],
            "validade": row[5]
        }
        for row in rows
    ]

    export_pdf_substances(dados, "substancias_exportadas.pdf")