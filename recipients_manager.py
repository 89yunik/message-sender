
import json
from decorators import log_exceptions
@log_exceptions()
class RecipientsManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.recipients = self.load_recipients()

    def load_recipients (self):
        with open(self.file_path, 'r', encoding='utf-8') as file: return json.load(file)
        
    def save_recipients (self):
        with open(self.file_path, 'w', encoding='utf-8') as file: json.dump(self.recipients, file, indent=4)

    def add_recipient(self, name, phone, email):
        self.recipients.append({'name': name, 'phone': phone, 'email': email})

    def delete_recipient(self, index):
        if 0 <= index < len(self.recipients): del self.recipients[index]
        
    def update_recipient(self, index, name, phone, email):
        if 0 <= index < len(self.recipients):
            self.recipients[index] = {'name': name, 'phone': phone, 'email': email}