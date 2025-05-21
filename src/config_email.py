import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_avaliacao(nome, comentario, pratos_favoritos, sugestao_pratos, media_geral):
    remetente = 'paulo.walraven@cocobambu.com'
    senha = 'hqse xvbh dusl cvwe'

    destinatarios = [
        'robson.cardoso@cocobambu.com',
        'renata.silva@cocobambu.com',
        'gerencia1.alphaville@cocobambu.com'
    ]

    assunto = f'Nova Avaliação Recebida - {nome}'
    corpo = f"""
    <h2>Nova Avaliação do Buffet</h2>
    <p><strong>Nome:</strong> {nome}</p>
    <p><strong>Média Geral:</strong> {media_geral} estrelas</p>
    <p><strong>Comentário:</strong> {comentario or 'Nenhum comentário.'}</p>
    <p><strong>Pratos Favoritos:</strong> {pratos_favoritos or 'Não informado.'}</p>
    <p><strong>Sugestão de Novos Pratos:</strong> {sugestao_pratos or 'Nenhuma sugestão.'}</p>
    """

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatarios, msg.as_string())
        print('E-mail enviado com sucesso.')
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')