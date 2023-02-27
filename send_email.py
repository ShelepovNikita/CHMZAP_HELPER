
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import os
import mimetypes
import config


def send_email_from_db(recipient, user_folder, message_text='Default request'):
    sender = config.sender
    password = config.password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = "Сформирован ответ на ваш запрос в базу данных"

        msg.attach(MIMEText(message_text))

        for file in os.listdir(user_folder):
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            filetype, subtype = ftype.split('/')
            with open(f'{user_folder}/{file}', 'rb') as f:
                file = MIMEBase(filetype, subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

            file.add_header(
                'content-disposition',
                'attachment',
                filename=filename
            )
            msg.attach(file)

        server.sendmail(sender, recipient, msg.as_string())
        return True
    except Exception:
        return False
