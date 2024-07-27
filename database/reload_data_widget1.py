# gui/reload_data_widget.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox

class ReloadDataWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.reload_button = QPushButton("Reload Data")
        self.reload_button.clicked.connect(self.reload_data)
        
        layout.addWidget(self.reload_button)
        self.setLayout(layout)

    def reload_data(self):
        reply = QMessageBox.question(self, 'Reload Data', 
                                     'Are you sure you want to reload all data? This will clear existing data.',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.db.clear_all_data()
                self.db.populate_dummy_data()
                self.db.add_dummy_sessions()  # Assuming you've added this method to DatabaseManager
                QMessageBox.information(self, "Success", "Data reloaded successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred while reloading data: {str(e)}")