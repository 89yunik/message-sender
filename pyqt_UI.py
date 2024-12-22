import sys, json, base64, re
from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QHBoxLayout, QPushButton, QTableWidgetItem, QMessageBox, QWidget, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont

from decorators import log_exceptions
from email_sender import EmailSender
from recipients_manager import RecipientsManager
from sms_sender import SmsSender


def get_full_path(file_name):
    base_path = Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).parent
    return base_path/file_name

@log_exceptions()
class SettingsDialog(QDialog): 
    def __init__(self, manager): 
        super().__init__()
        self.manager = manager 
        self.setWindowTitle("수신인 설정") 
        self.resize(600, 400)
        
        self.main_layout = QVBoxLayout()
        self.table = QTableWidget() 
        self.main_layout.addWidget(self.table)
        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("저장")
        self.add_button = QPushButton("추가")
        self.delete_button = QPushButton("삭제")

        self.button_layout.addWidget(self.add_button) 
        self.button_layout.addWidget(self.delete_button) 
        self.button_layout.addWidget(self.save_button) 
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        
        self.load_data()
        
        self.save_button.clicked.connect(self.save_changes)
        self.add_button.clicked.connect(self.add_recipient)
        self.delete_button.clicked.connect(self.delete_selected)

    
    def load_data(self):
        recipients = self.manager.recipients
        self.table.setRowCount (len (recipients))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels (['이름','연락처','이메일'])
        
        for row, recipient in enumerate(recipients):
            self.table.setItem(row, 0, QTableWidgetItem(recipient.get('name', ''))) 
            self.table.setItem(row, 1, QTableWidgetItem(recipient.get('phone', ''))) 
            self.table.setItem(row, 2, QTableWidgetItem(recipient.get('email', '')))
        
    def save_changes(self):
        recipients = []
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text() if self.table.item(row, 0) else ''
            phone = self.table.item(row, 1).text() if self.table.item(row, 1) else '' 
            email = self.table.item (row, 2).text() if self.table.item (row, 2) else '' 
            recipients.append({'name': name, 'phone': phone, 'email': email})
        
        self.manager.recipients = recipients 
        self.manager.save_recipients()
        QMessageBox.information (self, "저장", "저장 완료")

    def add_recipient(self):
        self.manager.add_recipient("이름", "0100000000", "example@google.com")
        self.load_data()

    def delete_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for index in sorted(selected_rows, reverse=True):
            self.manager.delete_recipient(index.row())
            self.load_data()


class MessageSenderWindow(QWidget):
    def __init__(self):
        super().__init__()
        with open(get_full_path('config.json'), 'r') as f: self.config = json.load(f)
        
        self.setWindowTitle("메시지 보내기")
        self.resize(600, 800)
        
        self.main_layout = QVBoxLayout()
        
        self.manager = RecipientsManager('recipients.json') 
        self.settings_button = QPushButton("수신인 설정") 
        self.main_layout.addWidget(self.settings_button)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        
        self.main_layout.addWidget(QLabel("메시지 제목"))
        self.subject_entry = QLineEdit() 
        self.main_layout.addWidget(self.subject_entry)
        
        self.main_layout.addWidget(QLabel("메시지 내용")) 
        self.text_edit = QTextEdit() 
        self.text_edit.setFont(QFont("Arial", 12)) 
        self.main_layout.addWidget(self.text_edit)
        
        self.button_layout = QHBoxLayout()
        self.send_email_button = QPushButton("이메일")
        self.send_email_button.clicked.connect(self.send_email)
        self.send_sms_button = QPushButton("문자")
        self.send_sms_button.clicked.connect(self.send_sms)

        self.button_layout.addWidget(self.send_email_button)
        self.button_layout.addWidget(self.send_sms_button)
        self.main_layout.addLayout(self.button_layout)

        self.result_label = QLabel('', self)
        self.main_layout.addWidget(self.result_label)

        self.setLayout(self.main_layout)
        
        self.email_sender = EmailSender(self.config['smtp_server'], 25, self.config['smtp_sender'])

    def send_email(self):
        self.result_label.setText("메일 전송 중...")

        subject = self.subject_entry.text()
        html_content = self.text_edit.toHtml() 
        modified_html_content = self.convert_images_to_base64(html_content)
        recipients = [recipeint_info['email'] for recipeint_info in self.manager.recipients] 
        result_message = self.email_sender.send_email(recipients, subject, modified_html_content)
        
        self.result_label.setText(result_message)

    def send_sms (self):
        self.result_label.setText("문자 전송 중...")
        message = f'{self.subject_entry.text()}\n{self.text_edit.toPlainText()}'
        recipients = [recipeint_info['phone'] for recipeint_info in self.manager.recipients]
        sms_sender = SmsSender(self.config['surem_id'], self.config['surem_company_code'], self.config['surem_sender']) 
        result_message = sms_sender.send_sms(recipients, message, "https://rest.surem.com/messages/mms")
        self.result_label.setText(result_message)

    def convert_images_to_base64(self, html_content):
        img_tag_pattern = r'<img\s+[^>]*src=["\'](file://[^"\']+)["\'][^>]*>' 
        img_paths = re.findall(img_tag_pattern, html_content)

        for img_path in img_paths:
            file_path = img_path[8] 
            with open(file_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode()
            
            base64_img_tag = f'data:image/png;base64, {encoded_string}' 
            html_content = html_content.replace(img_path, base64_img_tag)
        
        return html_content
    
    def open_settings_dialog(self):
        dialog = SettingsDialog(self.manager)
        dialog.exec_()