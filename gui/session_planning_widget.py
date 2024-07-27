# gui/session_planning_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QFormLayout, QMessageBox, 
                             QComboBox, QDateTimeEdit, QTextEdit)
from PyQt5.QtCore import QDateTime

class SessionPlanningWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Session list
        self.session_list = QListWidget()
        self.refresh_session_list()
        self.session_list.itemDoubleClicked.connect(self.load_session_details)  # Add this line
        layout.addWidget(self.session_list)

        # Form for adding/editing sessions
        form_layout = QFormLayout()
        
        self.client_combo = QComboBox()
        self.refresh_client_list()
        
        self.date_time_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_time_edit.setCalendarPopup(True)
        
        self.component_combo = QComboBox()
        self.refresh_component_list()
        
        self.technique_combo = QComboBox()
        self.refresh_technique_list()
        
        self.notes_edit = QTextEdit()
        
        form_layout.addRow("Client:", self.client_combo)
        form_layout.addRow("Date & Time:", self.date_time_edit)
        form_layout.addRow("ACT Component:", self.component_combo)
        form_layout.addRow("Technique:", self.technique_combo)
        form_layout.addRow("Session Notes:", self.notes_edit)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Session")
        self.add_button.clicked.connect(self.add_session)
        self.edit_button = QPushButton("Edit Session")
        self.edit_button.clicked.connect(self.edit_session)
        self.delete_button = QPushButton("Delete Session")
        self.delete_button.clicked.connect(self.delete_session)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        right_layout = QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addLayout(button_layout)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    # Add this method
    def load_session_details(self, item):
        session_id = self.db.get_all_sessions()[self.session_list.row(item)][0]
        session = self.db.get_session(session_id)
        if session:
            client_index = self.client_combo.findData(session[1])
            self.client_combo.setCurrentIndex(client_index)
            
            self.date_time_edit.setDateTime(QDateTime.fromString(session[2], "yyyy-MM-dd HH:mm:ss"))
            
            component_index = self.component_combo.findData(session[3])
            self.component_combo.setCurrentIndex(component_index)
            
            technique_index = self.technique_combo.findData(session[4])
            self.technique_combo.setCurrentIndex(technique_index)
            
            self.notes_edit.setText(session[5])

    def refresh_session_list(self):
        self.session_list.clear()
        sessions = self.db.get_all_sessions()
        for session in sessions:
            client_name = self.db.get_client_name(session[1])
            self.session_list.addItem(f"{client_name} - {session[2]}")

    def refresh_client_list(self):
        self.client_combo.clear()
        clients = self.db.get_all_clients()
        for client in clients:
            self.client_combo.addItem(client[1], client[0])

    def refresh_component_list(self):
        self.component_combo.clear()
        components = self.db.get_all_act_components()
        for component in components:
            self.component_combo.addItem(component[1], component[0])

    def refresh_technique_list(self):
        self.technique_combo.clear()
        techniques = self.db.get_all_act_techniques()
        for technique in techniques:
            self.technique_combo.addItem(technique[1], technique[0])

    def add_session(self):
        client_id = self.client_combo.currentData()
        date_time = self.date_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        component_id = self.component_combo.currentData()
        technique_id = self.technique_combo.currentData()
        notes = self.notes_edit.toPlainText()
        
        if client_id and date_time:
            self.db.add_session(client_id, date_time, component_id, technique_id, notes)
            self.refresh_session_list()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Client and Date & Time are required.")

    def edit_session(self):
        selected = self.session_list.currentItem()
        if selected:
            session_id = self.db.get_all_sessions()[self.session_list.currentRow()][0]
            client_id = self.client_combo.currentData()
            date_time = self.date_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            component_id = self.component_combo.currentData()
            technique_id = self.technique_combo.currentData()
            notes = self.notes_edit.toPlainText()
            
            if client_id and date_time:
                self.db.update_session(session_id, client_id, date_time, component_id, technique_id, notes)
                self.refresh_session_list()
                self.clear_inputs()
            else:
                QMessageBox.warning(self, "Input Error", "Client and Date & Time are required.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a session to edit.")

    def delete_session(self):
        selected = self.session_list.currentItem()
        if selected:
            session_id = self.db.get_all_sessions()[self.session_list.currentRow()][0]
            reply = QMessageBox.question(self, 'Delete Session', 
                                         'Are you sure you want to delete this session?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.delete_session(session_id)
                self.refresh_session_list()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a session to delete.")
            
        def load_session_details(self, item):
            session_id = self.db.get_all_sessions()[self.session_list.row(item)][0]
            session = self.db.get_session(session_id)
            if session:
                client_index = self.client_combo.findData(session[1])
                self.client_combo.setCurrentIndex(client_index)
                
                self.date_time_edit.setDateTime(QDateTime.fromString(session[2], "yyyy-MM-dd HH:mm:ss"))
                
                component_index = self.component_combo.findData(session[3])
                self.component_combo.setCurrentIndex(component_index)
                
                technique_index = self.technique_combo.findData(session[4])
                self.technique_combo.setCurrentIndex(technique_index)
                
                self.notes_edit.setText(session[5])

    def clear_inputs(self):
        self.client_combo.setCurrentIndex(0)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.component_combo.setCurrentIndex(0)
        self.technique_combo.setCurrentIndex(0)
        self.notes_edit.clear()