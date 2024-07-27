# gui/technique_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QTextEdit, QFormLayout, 
                             QMessageBox, QComboBox, QLabel)

class TechniqueWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left side: Technique list
        left_layout = QVBoxLayout()
        self.technique_list = QListWidget()
        left_layout.addWidget(QLabel("Techniques:"))
        left_layout.addWidget(self.technique_list)
        main_layout.addLayout(left_layout)

        # Right side: Form for adding/editing techniques
        right_layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Breathing", "Chi Kung", "Other"])
        self.description_input = QTextEdit()
        self.instructions_input = QTextEdit()

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Instructions:", self.instructions_input)

        right_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Technique")
        self.add_button.clicked.connect(self.add_technique)
        button_layout.addWidget(self.add_button)

        right_layout.addLayout(button_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.refresh_technique_list()

    def refresh_technique_list(self):
        self.technique_list.clear()
        techniques = self.db.get_all_techniques()
        for technique in techniques:
            self.technique_list.addItem(f"{technique[1]} - {technique[2]}")

    def add_technique(self):
        name = self.name_input.text()
        category = self.category_input.currentText()
        description = self.description_input.toPlainText()
        instructions = self.instructions_input.toPlainText()
        if name and category:
            self.db.add_technique(name, category, description, instructions)
            self.refresh_technique_list()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Name and Category are required.")

    def clear_inputs(self):
        self.name_input.clear()
        self.category_input.setCurrentIndex(0)
        self.description_input.clear()
        self.instructions_input.clear()