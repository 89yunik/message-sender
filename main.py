from logging_config import setup_logging
from decorators import handle_exceptions

logger = setup_logging()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont

class MessageSenderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("메시지 보내기")

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("메시지 제목"))
        self.subject_entry = QLineEdit()
        self.layout.addWidget(self.subject_entry)

        self.layout.addWidget(QLabel("메시지 내용"))
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.text_edit)

        self.button_layout = QHBoxLayout()
        self.send_email_button = QPushButton("이메일")
        # self.send_email_button.clicked.connect(self.send_email)
        self.send_sms_button = QPushButton("문자")
        self.send_sms_button.clicked.connect(self.send_sms)
        self.button_layout.addWidget(self.send_email_button)
        self.button_layout.addWidget(self.send_sms_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    # def send_sms(self):
    #     subject = self.subject_entry.text()
    #     body = self.text_edit.toPlainText()
        # body = self.text_edit.toHtml()

    #     if send_method == "이메일":
    #         # 이메일 발송
    #         email_sender = EmailSender("smtp.gmail.com", 587, "your_email@gmail.com", "your_password")
    #         email_sender.send_email(recipient, subject, body)
    #     elif send_method == "문자":
    #         # 문자 발송
    #         sms_sender = SmsSender("your_twilio_sid", "your_twilio_token", "your_twilio_number")
    #         sms_sender.send_sms(recipient, body)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessageSenderWindow()
    window.show()
    sys.exit(app.exec_())

# from twilio.rest import Client

# class SmsSender:
#     def __init__(self, account_sid, auth_token, from_phone):
#         self.client = Client(account_sid, auth_token)
#         self.from_phone = from_phone

#     def send_sms(self, to_phone, message):
#         """문자 메시지를 보냅니다."""
#         try:
#             message = self.client.messages.create(
#                 body=message,
#                 from_=self.from_phone,
#                 to=to_phone
#             )
#             print(f"문자가 {to_phone}로 성공적으로 발송되었습니다.")
#         except Exception as e:
#             print(f"문자 발송 실패: {e}")

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# class EmailSender:
#     def __init__(self, smtp_server, smtp_port, username, password):
#         self.smtp_server = smtp_server
#         self.smtp_port = smtp_port
#         self.username = username
#         self.password = password

#     def send_email(self, to_email, subject, body):
#         """이메일을 보냅니다."""
#         msg = MIMEMultipart()
#         msg['From'] = self.username
#         msg['To'] = to_email
#         msg['Subject'] = subject
#         msg.attach(MIMEText(body, 'plain'))

#         try:
#             with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
#                 server.starttls()
#                 server.login(self.username, self.password)
#                 server.sendmail(self.username, to_email, msg.as_string())
#                 print(f"이메일이 {to_email}로 성공적으로 발송되었습니다.")
#         except Exception as e:
#             print(f"이메일 발송 실패: {e}")