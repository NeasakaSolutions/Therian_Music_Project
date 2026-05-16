# Importaciones
from django.core.paginator import Paginator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smtplib import SMTPResponseException

from dotenv import load_dotenv

import smtplib
import os


def sendMail(html, asunto, para):
    
    # Cabeceras del modelo
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = os.getenv("SMTP_USER")
    msg['To'] = para
    
    msg.attach(MIMEText(html, 'html'))

    try:
        #server = smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))
        #server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        #server.sendmail(os.getenv("SMTP_USER"), para, msg.as_string())
        #server.quit()
        if os.getenv("SMTP_PORT") == "465":
            server = smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        else:
            server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
            server.starttls()

        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), para, msg.as_string())
        server.quit()

    except SMTPResponseException as e:
        print('error envio mail')

def paginar(request, queryset, limite=10):

    page = request.GET.get("page", 1)

    paginator = Paginator(queryset, limite)

    registros = paginator.get_page(page)

    return {
        "data": registros,
        "pagina_actual": registros.number,
        "total_paginas": paginator.num_pages,
        "total_registros": paginator.count,
        "hay_siguiente": registros.has_next(),
        "hay_anterior": registros.has_previous()
    }

