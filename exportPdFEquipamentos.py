from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf_equipments_and_maintenance(equipamentos, manutencoes, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título Equipamentos
    title_eq = Paragraph("Equipamentos", styles['Title'])
    elements.append(title_eq)
    elements.append(Spacer(1, 8))

    # Tabela Equipamentos
    table_data_eq = [["ID", "Nome", "Tipo", "Status", "Última\nManutenção", "Localização", "Responsável", "Categoria"]]
    for row in equipamentos:
        table_data_eq.append([
            row.get('id', ''),
            row.get('nome', ''),
            row.get('tipo', ''),
            row.get('status', ''),
            row.get('ultima_manutencao', ''),
            row.get('localizacao', ''),
            row.get('responsavel', ''),
            row.get('categoria', '')
        ])
    table_eq = Table(table_data_eq, colWidths=[30, 60, 45, 45, 80, 55, 55, 45])
    table_eq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table_eq)
    elements.append(Spacer(1, 18))

    # Título Manutenções
    title_mn = Paragraph("Histórico de Manutenções", styles['Title'])
    elements.append(title_mn)
    elements.append(Spacer(1, 8))

    # Tabela Manutenções
    table_data_mn = [["ID", "Equipamento", "Data da\n Manutenção", "Descrição"]]
    for row in manutencoes:
        table_data_mn.append([
            row.get('id', ''),
            row.get('equipamento_nome', ''),
            row.get('data_manutencao', ''),
            row.get('descricao', '')
        ])
    table_mn = Table(table_data_mn, colWidths=[30, 80, 80, 200])
    table_mn.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table_mn)

    doc.build(elements)

if __name__ == "__main__":
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
