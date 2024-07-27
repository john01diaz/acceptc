# main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from database.db_manager import DatabaseManager
from gui.client_widget import ClientWidget
from gui.act_components_widget import ACTComponentsWidget
from gui.session_planning_widget import SessionPlanningWidget
from gui.technique_widget import TechniqueWidget
from gui.reload_data_widget import ReloadDataWidget

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ACT Practitioner Tool')
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Add the reload data widget at the top
        reload_data_widget = ReloadDataWidget(self.db)
        main_layout.addWidget(reload_data_widget)

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

def main():
    app = QApplication(sys.argv)
    
    db_path = r'C:\Users\John.J.Diaz\progs'
    db_name = 'act_tool.db'
    
    try:
        db = DatabaseManager(db_path, db_name)
        window = MainWindow(db)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()