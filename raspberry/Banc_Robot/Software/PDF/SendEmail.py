import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def SendDiag(filename, date, receiver_email):

    # Envoi du rapport par mail

    try:  # On utilise try/except car il y a plusieurs tentatives d'envois et en cas de problème on ne crash pas le logiciel

        # Port et serveur d'envoi
        port = 587  # For starttls
        smtp_server = "smtp-mail.outlook.com"
        # Identifiants
        sender_email = "BancBVR.Faral53@outlook.com"
        password = 'Faral53000'
        # Destinataire et contenu du mail
        subject = "Fiche Diagnostique du " + date
        message = ""
        filepath = os.path.dirname(os.path.abspath(__file__)) + "/DiagReport/" + filename

        # Création de la trame du mail au format MIME
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        # Ajout du message
        msgText = MIMEText('%s' % (message), 'html')
        msg.attach(msgText)
        # Ajout de la pièce jointe
        pdf = MIMEApplication(open(filepath, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename= filename)
        msg.attach(pdf)

        # Connexion au serveur et envoi du mail
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True

    # On retourne False pour signaler qu'il y a eut une erreur et que le essage n'a pas été envoyé
    except:
        return False

#SendDiag("Fiche_Diag_PA6_2021-07-05_13h48_1.pdf", "31/02/2021")
