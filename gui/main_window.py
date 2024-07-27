# gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ACT Practitioner Tool')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        layout = QVBoxLayout()

        main_layout = QVBoxLayout()
        
        # Add the reload data widget at the top
        reload_data_widget = ReloadDataWidget(self.db)
        main_layout.addWidget(reload_data_widget)
        
        label = QLabel("ACT Practitioner Tool")
        layout.addWidget(label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        technique_widget = TechniqueWidget(self.db)
        tab_widget.addTab(technique_widget, "Techniques")
        
                # Create tab widget
        tab_widget = QTabWidget()
        client_widget = ClientWidget(self.db)
        act_components_widget = ACTComponentsWidget(self.db)
        session_planning_widget = SessionPlanningWidget(self.db)
        technique_widget = TechniqueWidget(self.db)

        tab_widget.addTab(client_widget, "Clients")
        tab_widget.addTab(act_components_widget, "ACT Components")
        tab_widget.addTab(session_planning_widget, "Session Planning")
        tab_widget.addTab(technique_widget, "Techniques")

        main_layout.addWidget(tab_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)