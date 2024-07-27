# gui/act_components_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QFormLayout, QMessageBox, QComboBox)

class ACTComponentsWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Components list
        self.components_list = QListWidget()
        self.refresh_components_list()
        self.components_list.itemDoubleClicked.connect(self.load_component_details)
        layout.addWidget(self.components_list)
        

        # Form for adding/editing components
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.model_input = QComboBox()
        self.model_input.addItems(["Hexaflex", "Triflex"])
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Model:", self.model_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Component")
        self.add_button.clicked.connect(self.add_component)
        self.edit_button = QPushButton("Edit Component")
        self.edit_button.clicked.connect(self.edit_component)
        self.delete_button = QPushButton("Delete Component")
        self.delete_button.clicked.connect(self.delete_component)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        right_layout = QVBoxLayout()
        right_layout.addLayout(form_layout)
        right_layout.addLayout(button_layout)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    def refresh_components_list(self):
        self.components_list.clear()
        components = self.db.get_all_act_components()
        for component in components:
            self.components_list.addItem(f"{component[1]} - {component[3]}")

    def load_component_details(self, item):
        component_id = self.db.get_all_act_components()[self.components_list.row(item)][0]
        component = self.db.get_act_component(component_id)
        if component:
            self.name_input.setText(component[1])
            self.description_input.setText(component[2])
            self.model_input.setCurrentText(component[3])

    def add_component(self):
        name = self.name_input.text()
        description = self.description_input.text()
        model = self.model_input.currentText()
        if name and description:
            self.db.add_act_component(name, description, model)
            self.refresh_components_list()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "Name and Description are required.")

    def edit_component(self):
        selected = self.components_list.currentItem()
        if selected:
            component_id = self.db.get_all_act_components()[self.components_list.currentRow()][0]
            name = self.name_input.text()
            description = self.description_input.text()
            model = self.model_input.currentText()
            if name and description:
                self.db.update_act_component(component_id, name, description, model)
                self.refresh_components_list()
                self.clear_inputs()
            else:
                QMessageBox.warning(self, "Input Error", "Name and Description are required.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to edit.")

    def delete_component(self):
        selected = self.components_list.currentItem()
        if selected:
            component_id = self.db.get_all_act_components()[self.components_list.currentRow()][0]
            reply = QMessageBox.question(self, 'Delete Component', 
                                         'Are you sure you want to delete this component?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.delete_act_component(component_id)
                self.refresh_components_list()
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a component to delete.")

    def clear_inputs(self):
        self.name_input.clear()
        self.description_input.clear()
        self.model_input.setCurrentIndex(0)