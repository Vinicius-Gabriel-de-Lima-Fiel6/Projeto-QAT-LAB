import os, ssl, smtplib, time
from email.message import EmailMessage
from datetime import datetime

def _as_list(v):
    return v if isinstance(v, (list, tuple)) else [v]

def _send(to, subject, text=None, html=None, retries=3, delay=2):
    msg = EmailMessage()
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = ", ".join(_as_list(to))
    msg["Subject"] = subject
    msg.set_content((text or "Veja em HTML."), charset="utf-8")
    if html:
        msg.add_alternative(html, subtype="html", charset="utf-8")

    for i in range(retries):
        try:
            with smtplib.SMTP(os.environ.get("MAIL_HOST", "smtp.gmail.com"),
                              int(os.environ.get("MAIL_PORT", "587"))) as s:
                s.starttls(context=ssl.create_default_context())
                s.login(os.environ["MAIL_USER"], os.environ["MAIL_PASS"])
                s.send_message(msg)
            return
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(delay * (2**i))

def send_email(to, subject, text=None, html=None):
    _send(to, subject, text, html)

def alerta_estoque(destinatarios, nome_substancia, quantidade, tempo_restante_dias):
    subject = f"⚠️ Estoque Baixo: {nome_substancia}"
    text = (
        f"A substância '{nome_substancia}' está com estoque baixo.\n"
        f"Quantidade atual: {quantidade}\n"
        f"Tempo estimado até esgotar: {tempo_restante_dias} dias\n"
        f"(Sistema do Laboratório)"
    )
    html = f"""
    <div style="font-family:Arial,sans-serif">
      <h2>⚠️ Estoque Baixo</h2>
      <p>A substância <b>{nome_substancia}</b> está com estoque baixo.</p>
      <p>Quantidade atual: <b>{quantidade}</b></p>
      <p>Tempo estimado até esgotar: <b>{tempo_restante_dias} dias</b></p>
      <hr><small>Gerado em {datetime.now():%d/%m/%Y %H:%M}</small>
    </div>
    """
    _send(destinatarios, subject, text, html)

def alerta_prazo(destinatarios, tarefa, data_limite, responsavel=None):
    subject = f"⏰ Prazo Próximo: {tarefa}"
    text = (
        f"Tarefa: {tarefa}\n"
        f"Data limite: {data_limite}\n"
        + (f"Responsável: {responsavel}\n" if responsavel else "")
        + "(Sistema do Laboratório)"
    )
    html = f"""
    <div style="font-family:Arial,sans-serif">
      <h2>⏰ Prazo Próximo</h2>
      <p>Tarefa: <b>{tarefa}</b></p>
      <p>Data limite: <b>{data_limite}</b></p>
      {f"<p>Responsável: <b>{responsavel}</b></p>" if responsavel else ""}
      <hr><small>Gerado em {datetime.now():%d/%m/%Y %H:%M}</small>
    </div>
    """
    _send(destinatarios, subject, text, html)

def alerta_custom(destinatarios, assunto, texto, html=None):
    _send(destinatarios, assunto, texto, html)
