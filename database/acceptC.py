# database/db_manager.py
import sqlite3

import os

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        db_exists = os.path.exists(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        if not db_exists:
            print(f"Database '{self.db_name}' created.")
            self.populate_dummy_data()

    def create_tables(self):
        # ... (keep the existing table creation code)

    def populate_dummy_data(self):
        # ... (keep the existing populate_dummy_data code)
        print("Dummy data populated.")

    def close(self):
        if self.conn:
            self.conn.close()

# ... (keep other methods)


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Previous tables (clients, act_components, techniques, sessions, progress_tracking)
        # ... (keep the existing table creations)

        # New tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS conditions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            classification TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS act_techniques (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            act_component_id INTEGER,
            FOREIGN KEY (act_component_id) REFERENCES act_components (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS condition_techniques (
            condition_id INTEGER,
            technique_id INTEGER,
            PRIMARY KEY (condition_id, technique_id),
            FOREIGN KEY (condition_id) REFERENCES conditions (id),
            FOREIGN KEY (technique_id) REFERENCES act_techniques (id)
        )
        ''')

        self.conn.commit()

    def populate_dummy_data(self):
        # Populate clients
        clients = [
            ("John Doe", "john@example.com", "555-1234"),
            ("Jane Smith", "jane@example.com", "555-5678"),
            ("Bob Johnson", "bob@example.com", "555-9012")
        ]
        self.cursor.executemany("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", clients)

        # Populate ACT components
        components = [
            ("Acceptance", "Embracing thoughts and feelings without trying to change them", "Hexaflex"),
            ("Cognitive Defusion", "Learning to perceive thoughts, images, memories and other cognitions as what they are", "Hexaflex"),
            ("Being Present", "Connecting with the present moment", "Hexaflex"),
            ("Self as Context", "Accessing a transcendent sense of self", "Hexaflex"),
            ("Values", "Discovering what is most important to oneself", "Hexaflex"),
            ("Committed Action", "Setting goals according to values and carrying them out responsibly", "Hexaflex"),
            ("Open", "Being open to inner experiences", "Triflex"),
            ("Aware", "Being aware of the present moment", "Triflex"),
            ("Engaged", "Doing what matters", "Triflex")
        ]
        self.cursor.executemany("INSERT INTO act_components (name, description, model) VALUES (?, ?, ?)", components)

        # Populate conditions (using ICD-10 codes)
        conditions = [
            ("Obsessive-Compulsive Disorder", "F42", "ICD-10"),
            ("Post-Traumatic Stress Disorder", "F43.1", "ICD-10"),
            ("Generalized Anxiety Disorder", "F41.1", "ICD-10"),
            ("Major Depressive Disorder", "F32", "ICD-10"),
            ("Social Anxiety Disorder", "F40.1", "ICD-10"),
            ("Panic Disorder", "F41.0", "ICD-10")
        ]
        self.cursor.executemany("INSERT INTO conditions (name, code, classification) VALUES (?, ?, ?)", conditions)

        # Populate ACT techniques
        techniques = [
            ("Mindfulness Meditation", "Focusing on the present moment", 3),
            ("Cognitive Defusion Exercises", "Separating oneself from thoughts", 2),
            ("Values Clarification", "Identifying personal values", 5),
            ("Acceptance Exercises", "Practicing acceptance of difficult emotions", 1),
            ("Committed Action Planning", "Setting goals based on values", 6),
            ("Self-as-Context Metaphors", "Using metaphors to explain self-as-context", 4)
        ]
        self.cursor.executemany("INSERT INTO act_techniques (name, description, act_component_id) VALUES (?, ?, ?)", techniques)

        # Populate condition_techniques (example associations)
        condition_techniques = [
            (1, 1), (1, 2), (1, 4),  # OCD
            (2, 1), (2, 4), (2, 5),  # PTSD
            (3, 1), (3, 2), (3, 3),  # GAD
            (4, 3), (4, 5), (4, 6),  # Depression
            (5, 2), (5, 4), (5, 6)   # Social Anxiety
        ]
        self.cursor.executemany("INSERT INTO condition_techniques (condition_id, technique_id) VALUES (?, ?)", condition_techniques)

        self.conn.commit()

    def close(self):
        self.conn.close()

    # Add other CRUD methods here as needed
    
    # main.py


def main():
    app = QApplication(sys.argv)
    db = DatabaseManager('act_tool.db')
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()