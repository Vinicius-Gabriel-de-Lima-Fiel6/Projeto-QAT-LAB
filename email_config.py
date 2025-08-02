# email_alerta.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_alerta_email(destinatario, nome_substancia, quantidade, tempo_restante):
    remetente = "viniciuslima09321@gmail.com"
    senha = "47575"
    destinatario="viniciuslima09321@gmail.com"

    assunto = f"⚠️ Alerta de Estoque Baixo: {nome_substancia}"
    corpo = f"""==========Atenção!============\nA substância '{nome_substancia}' está com o estoque baixo.\nQuantidade atual: {quantidade}\nTempo estimado até esgotamento: {tempo_restante} dias\nRecomenda-se realizar uma nova compra o quanto antes.\n(Sistema LabSmartAI)
    """

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        texto = msg.as_string()
        servidor.sendmail(remetente, destinatario, texto)
        servidor.quit()
        print(f"✔️ Alerta enviado para {destinatario}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")