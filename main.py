import sys
from PyQt5.QtWidgets import QApplication 
from pyqt_UI import MessageSenderWindow

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = MessageSenderWindow() 
    window.show() 
    sys.exit(app.exec_())