import smtplib
from pathlib import Path 
from typing import List
from email import encoders
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase
from decorators import log_exceptions


@log_exceptions()
class EmailSender:
    def __init__(self, smtp_server, smtp_port, username):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port 
        self.username = username
        
    def send_email(self, to_email:List[str], subject: str, html_body:str, attachment_paths: List[Path]=None):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(to_email)
        msg['Subject'] = subject
        msg.attach(MIMEText (html_body, 'html'))
        if attachment_paths:
            for attachment_path in attachment_paths:
                if attachment_path.is_file():
                    with attachment_path.open('rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload (attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {attachment_path.name}',
                        )
                        msg.attach (part)

        server = smtplib.SMTP(self.smtp_server, self.smtp_port) 
        server.starttls()
        server.sendmail(self.username, to_email, msg.as_string())
        server.quit()

        return "Email"