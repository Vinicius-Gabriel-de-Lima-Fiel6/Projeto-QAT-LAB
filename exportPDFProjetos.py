from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf_projects(data, filename):
    """
    Exportar dados dos projetos para um arquivo PDF.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    title = Paragraph("Projetos", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  
    table_data = [["ID", "Nome", "Status", "Descrição"]]
    for row in data:
        table_data.append([
            row.get('id', ''),
            row.get('nome', ''),
            row.get('status', ''),
            row.get('descricao', ''),
        ])
    table = Table(table_data)
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),  # Fonte menor
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Menos espaço no cabeçalho
    ('TOPPADDING', (0, 0), (-1, -1), 2),   # Menos espaço nas células
    ('BOTTOMPADDING', (0, 1), (-1, -1), 2), # Menos espaço nas células
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

    export_pdf_projects(dados, "projetos_exportados.pdf")