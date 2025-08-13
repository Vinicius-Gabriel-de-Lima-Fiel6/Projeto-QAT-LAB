from notifier_smtp import alerta_custom

alerta_custom(
    destinatarios="juliabcohen@icloud.com",
    assunto="Teste de Envio - Lab",
    texto="Este é um teste simples de envio usando notifier_smtp.py",
    html="<h3>Teste OK</h3><p>Este é um teste simples de envio usando <b>notifier_smtp.py</b>.</p>"
)

print("✅ Email enviado!")
