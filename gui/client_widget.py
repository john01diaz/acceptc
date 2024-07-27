# gui/client_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QFormLayout, QMessageBox,
                             QTextEdit)
from PyQt5.QtCore import Qt

class ClientWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Client list
        self.client_list = QListWidget()
        self.refresh_client_list()
        self.client_list.itemDoubleClicked.connect(self.load_client_details)
        layout.addWidget(self.client_list)

        # Right side layout
        right_layout = QVBoxLayout()

        # Client details area
        self.details_area = QTextEdit()
        self.details_area.setReadOnly(True)
        right_layout.addWidget(self.details_area)

        # Form for adding/editing clients
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)
        right_layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Client")
        self.add_button.clicked.connect(self.add_client)
        self.edit_button = QPushButton("Edit Client")
        self.edit_button.clicked.connect(self.edit_client)
        self.delete_button = QPushButton("Delete Client")
        self.delete_button.clicked.connect(self.delete_client)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        
        right_layout.addLayout(button_layout)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    def refresh_client_list(self):
        self.client_list.clear()
        clients = self.db.get_all_clients()
        for client in clients:
            self.client_list.addItem(f"{client[1]} - {client[2]}")

    def load_client_details(self, item):
        client_id = self.db.get_all_clients()[self.client_list.row(item)][0]
        client = self.db.get_client(client_id)
        sessions = self.db.get_client_sessions(client_id)
        conditions = self.db.get_client_conditions(client_id)

        details = f"Name: {client[1]}\nEmail: {client[2]}\nPhone: {client[3]}\n\n"

        details += "Conditions:\n"
        for condition in conditions:
            details += f"- {condition[1]} ({condition[2]} - {condition[3]})\n"

        details += "\nSessions:\n"
        for session in sessions:
            details += f"\nSession ID: {session[0]}\nDate: {session[2]}\n"
            details += f"Notes: {session[5][:30]}... (double-click to expand)\n"
            
            techniques = self.db.get_session_techniques(session[0])
            for technique in techniques:
                details += f"Technique: {technique[1]} - Feedback: {technique[4][:30]}... (double-click to expand)\n"

        self.details_area.setText(details)

        # Fill in the input fields
        self.name_input.setText(client[1])
        self.email_input.setText(client[2])
        self.phone_input.setText(client[3])

    def add_client(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        if name and email:
            self.db.add_client(name, email, phone)
            self.refresh_client_list()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Name and Email are required.")

    def edit_client(self):
        selected = self.client_list.currentItem()
        if selected:
            client_id = self.db.get_all_clients()[self.client_list.currentRow()][0]
            name = self.name_input.text()
            email = self.email_input.text()
            phone = self.phone_input.text()
            if name and email:
                self.db.update_client(client_id, name, email, phone)
                self.refresh_client_list()
                self.clear_inputs()
            else:
                QMessageBox.warning(self, "Input Error", "Name and Email are required.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a client to edit.")

    def delete_client(self):
        selected = self.client_list.currentItem()
        if selected:
            client_id = self.db.get_all_clients()[self.client_list.currentRow()][0]
            reply = QMessageBox.question(self, 'Delete Client', 
                                         'Are you sure you want to delete this client?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.delete_client(client_id)
                self.refresh_client_list()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a client to delete.")

    def clear_inputs(self):
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()