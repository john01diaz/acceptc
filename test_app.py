import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Window')
        self.setGeometry(100, 100, 300, 200)
        label = QLabel('Test Label', self)
        label.move(100, 80)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()