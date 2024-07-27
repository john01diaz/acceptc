# database/db_manager.py
import sqlite3
import os
import random  # Add this line


class DatabaseManager:
    def __init__(self, db_path, db_name, populate=False):
        self.db_path = db_path
        self.db_name = db_name
        self.full_path = os.path.join(self.db_path, self.db_name)
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        if populate:
            self.clear_all_data()
            self.populate_dummy_data()

    def connect(self):
        os.makedirs(self.db_path, exist_ok=True)
        self.conn = sqlite3.connect(self.full_path)
        self.cursor = self.conn.cursor()
        print(f"Database {'created' if not os.path.exists(self.full_path) else 'connected'} at '{self.full_path}'.")

 # Add these methods to your DatabaseManager class

    def get_all_act_components(self):
        self.cursor.execute("SELECT * FROM act_components")
        return self.cursor.fetchall()
    
    def get_act_component(self, component_id):
        self.cursor.execute("SELECT * FROM act_components WHERE id = ?", (component_id,))
        return self.cursor.fetchone()
    
    
    def add_act_component(self, name, description, model):
        self.cursor.execute("INSERT INTO act_components (name, description, model) VALUES (?, ?, ?)", 
                            (name, description, model))
        self.conn.commit()

    def update_act_component(self, component_id, name, description, model):
        self.cursor.execute("UPDATE act_components SET name = ?, description = ?, model = ? WHERE id = ?", 
                            (name, description, model, component_id))
        self.conn.commit()

    def delete_act_component(self, component_id):
        self.cursor.execute("DELETE FROM act_components WHERE id = ?", (component_id,))
        self.conn.commit()   
    
    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients WHERE archived = 0")
        return self.cursor.fetchall()

    def add_client(self, name, email, phone):
        self.cursor.execute("INSERT INTO clients (name, email, phone, archived) VALUES (?, ?, ?, 0)", 
                            (name, email, phone))
        self.conn.commit()

    def update_client(self, client_id, name, email, phone):
        self.cursor.execute("UPDATE clients SET name = ?, email = ?, phone = ? WHERE id = ?", 
                            (name, email, phone, client_id))
        self.conn.commit()

    def archive_client(self, client_id):
        self.cursor.execute("UPDATE clients SET archived = 1 WHERE id = ?", (client_id,))
        self.conn.commit()

    def delete_client(self, client_id):
        self.cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        self.conn.commit()
    
    def create_tables(self):
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS act_components (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            model TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS conditions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            classification TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS act_techniques (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            act_component_id INTEGER,
            FOREIGN KEY (act_component_id) REFERENCES act_components (id)
        );

        CREATE TABLE IF NOT EXISTS condition_techniques (
            condition_id INTEGER,
            technique_id INTEGER,
            PRIMARY KEY (condition_id, technique_id),
            FOREIGN KEY (condition_id) REFERENCES conditions (id),
            FOREIGN KEY (technique_id) REFERENCES act_techniques (id)
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            date_time TEXT,
            component_id INTEGER,
            technique_id INTEGER,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (component_id) REFERENCES act_components (id),
            FOREIGN KEY (technique_id) REFERENCES act_techniques (id)
        );
        
        CREATE TABLE IF NOT EXISTS techniques (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            instructions TEXT,
            act_component_id INTEGER,
            FOREIGN KEY (act_component_id) REFERENCES act_components (id)
        );

        CREATE TABLE IF NOT EXISTS session_techniques (
            session_id INTEGER,
            technique_id INTEGER,
            feedback TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id),
            FOREIGN KEY (technique_id) REFERENCES techniques (id)
        );
        ''')
        
        # In db_manager.py, add to the create_tables method:



        # Add methods to interact with these new tables
    def add_technique(self, name, category, description, instructions):
        self.cursor.execute('''
        INSERT INTO techniques (name, category, description, instructions) 
        VALUES (?, ?, ?, ?)
        ''', (name, category, description, instructions))
        self.conn.commit()

    def get_all_techniques(self):
        self.cursor.execute("SELECT * FROM techniques")
        return self.cursor.fetchall()

    def add_session_technique(self, session_id, technique_id, feedback):
        self.cursor.execute('''
        INSERT INTO session_techniques (session_id, technique_id, feedback) 
        VALUES (?, ?, ?)
        ''', (session_id, technique_id, feedback))
        self.conn.commit()

    def get_session_techniques(self, session_id):
        self.cursor.execute('''
        SELECT t.*, st.feedback 
        FROM techniques t 
        JOIN session_techniques st ON t.id = st.technique_id 
        WHERE st.session_id = ?
        ''', (session_id,))
        return self.cursor.fetchall()
        
        self.conn.commit()
        print("Tables created successfully.")

    def get_client(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        return self.cursor.fetchone()

    def get_client_sessions(self, client_id):
        self.cursor.execute("SELECT * FROM sessions WHERE client_id = ? ORDER BY date_time DESC", (client_id,))
        return self.cursor.fetchall()

    def get_session_techniques(self, session_id):
        self.cursor.execute('''
        SELECT t.*, st.feedback 
        FROM techniques t 
        JOIN session_techniques st ON t.id = st.technique_id 
        WHERE st.session_id = ?
        ''', (session_id,))
        return self.cursor.fetchall()
 
    def get_session(self, session_id):
        self.cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        return self.cursor.fetchone()
    

    def get_all_sessions(self):
        self.cursor.execute("SELECT * FROM sessions ORDER BY date_time DESC")
        return self.cursor.fetchall()

    def add_session(self, client_id, date_time, component_id, technique_id, notes):
        self.cursor.execute('''
        INSERT INTO sessions (client_id, date_time, component_id, technique_id, notes)
        VALUES (?, ?, ?, ?, ?)
        ''', (client_id, date_time, component_id, technique_id, notes))
        self.conn.commit()
        
    

    def update_session(self, session_id, client_id, date_time, component_id, technique_id, notes):
        self.cursor.execute('''
        UPDATE sessions
        SET client_id = ?, date_time = ?, component_id = ?, technique_id = ?, notes = ?
        WHERE id = ?
        ''', (client_id, date_time, component_id, technique_id, notes, session_id))
        self.conn.commit()

    def delete_session(self, session_id):
        self.cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        self.conn.commit()

    def get_client_name(self, client_id):
        self.cursor.execute("SELECT name FROM clients WHERE id = ?", (client_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "Unknown Client"

    def get_all_act_techniques(self):
        self.cursor.execute("SELECT * FROM act_techniques")
        return self.cursor.fetchall()
        
    def clear_all_data(self):
        tables = ['clients', 'act_components', 'conditions', 'act_techniques', 
                'condition_techniques', 'sessions', 'session_techniques']
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        print("All data cleared from the database.")
        
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

        # Populate conditions (using ICD-10 and ICD-11 codes)
        conditions = [
            ("Obsessive-Compulsive Disorder", "F42", "ICD-10"),
            ("Post-Traumatic Stress Disorder", "F43.1", "ICD-10"),
            ("Generalized Anxiety Disorder", "F41.1", "ICD-10"),
            ("Major Depressive Disorder", "F32", "ICD-10"),
            ("Social Anxiety Disorder", "F40.1", "ICD-10"),
            ("Panic Disorder", "F41.0", "ICD-10"),
            ("Specific Phobia", "F40.2", "ICD-10"),
            ("Agoraphobia", "F40.0", "ICD-10"),
            ("Separation Anxiety Disorder", "F93.0", "ICD-10"),
            ("Internet Gaming Disorder", "6C51", "ICD-11"),
            ("Social Media Addiction", "6C51", "ICD-11"),
            ("Binge Eating Disorder", "F50.2", "ICD-10"),
            ("Tobacco Use Disorder", "F17", "ICD-10"),
            ("Oppositional Defiant Disorder", "F91.3", "ICD-10"),
            ("Attention-Deficit/Hyperactivity Disorder", "F90", "ICD-10"),
            ("Bipolar Disorder", "F31", "ICD-10"),
            ("Borderline Personality Disorder", "F60.3", "ICD-10"),
            ("Schizophrenia", "F20", "ICD-10"),
            ("Anorexia Nervosa", "F50.0", "ICD-10"),
            ("Bulimia Nervosa", "F50.2", "ICD-10"),
        ]
        self.cursor.executemany("INSERT INTO conditions (name, code, classification) VALUES (?, ?, ?)", conditions)

        # Populate ACT techniques
        techniques = [
            ("Mindfulness Meditation", "Meditation", "Focusing attention on the present moment", "Sit comfortably, close your eyes, and focus on your breath. Notice thoughts without judgment.", 3),
            ("Cognitive Defusion", "Cognitive", "Separating oneself from thoughts", "Observe your thoughts as if they were leaves floating on a stream, passing by without engaging them.", 2),
            ("Values Clarification", "Values", "Identifying personal values", "Complete a values assessment questionnaire and reflect on what truly matters to you.", 5),
            ("Acceptance Exercises", "Emotional", "Practicing acceptance of difficult emotions", "Notice and name your emotions without trying to change them. Breathe into the feeling.", 1),
            ("Committed Action Planning", "Behavioral", "Setting goals based on values", "Identify a value-aligned goal and break it down into small, achievable steps.", 6),
            ("Self-as-Context Metaphors", "Perspective", "Using metaphors to explain self-as-context", "Imagine yourself as the sky, and your thoughts and feelings as passing weather.", 4),
            ("Body Scan", "Meditation", "Mindfulness technique focusing on body sensations", "Lie down and systematically focus your attention on each part of your body, noticing sensations.", 3),
            ("Leaves on a Stream", "Visualization", "Visualization exercise for cognitive defusion", "Imagine your thoughts as leaves on a stream, watching them float away.", 2),
            ("Values Card Sort", "Values", "Activity to prioritize personal values", "Sort a deck of cards with different values written on them in order of personal importance.", 5),
            ("FEAR vs. ACT Acronym", "Psychoeducation", "Contrasting avoidance with acceptance", "Learn and apply the FEAR (Fusion, Evaluation, Avoidance, Reason-giving) and ACT (Accept, Choose, Take action) acronyms.", 1),
            ("Behavioral Activation", "Behavioral", "Engaging in value-consistent activities", "Schedule and engage in activities that align with your values, regardless of mood.", 6),
            ("Observer Self Exercise", "Perspective", "Meditation to connect with the observing self", "Close your eyes and notice different aspects of your experience, recognizing the 'you' that's doing the noticing.", 4),
            ("Willingness and Avoidance", "Emotional", "Exploring the costs of avoidance", "List situations you avoid and consider the short-term benefits and long-term costs of avoidance.", 1),
            ("Physicalizing Exercise", "Visualization", "Giving physical form to thoughts or feelings", "Imagine a difficult emotion as a physical object. Describe its size, shape, color, and texture.", 2),
            ("Life Compass", "Values", "Mapping values across life domains", "Create a visual representation of your values in different life areas (e.g., work, relationships, health).", 5),
            ("Mindful Breathing", "Meditation", "Focusing attention on the breath", "Sit quietly and focus on the sensation of your breath entering and leaving your body.", 3),
            ("Cognitive Defusion Techniques", "Cognitive", "Various methods to create distance from thoughts", "Practice saying thoughts in a silly voice or repeating a word until it loses its meaning.", 2),
            ("Values-based Goal Setting", "Behavioral", "Creating specific goals aligned with values", "For each core value, set a specific, measurable goal that moves you towards living that value.", 6),
            ("Present Moment Awareness", "Mindfulness", "Exercises to increase present-focused attention", "Practice bringing your attention to the present moment throughout the day using environmental cues.", 3),
            ("Experiential Avoidance Diary", "Self-monitoring", "Tracking avoidance behaviors", "Keep a daily log of situations you avoid and the emotions or thoughts you're trying to escape.", 1),
        ]

        # Update this line in the populate_dummy_data method
        self.cursor.executemany("INSERT INTO techniques (name, category, description, instructions, act_component_id) VALUES (?, ?, ?, ?, ?)", techniques)
        # Populate condition_techniques associations
        condition_techniques = [
            (1, 1), (1, 2), (1, 4), (1, 8), (1, 14),  # OCD
            (2, 1), (2, 4), (2, 5), (2, 7), (2, 13),  # PTSD
            (3, 1), (3, 2), (3, 3), (3, 16), (3, 19),  # GAD
            (4, 3), (4, 5), (4, 6), (4, 11), (4, 18),  # Depression
            (5, 2), (5, 4), (5, 6), (5, 9), (5, 17),  # Social Anxiety
            (6, 1), (6, 4), (6, 7), (6, 16), (6, 19),  # Panic Disorder
            (7, 2), (7, 4), (7, 13), (7, 14), (7, 17),  # Specific Phobia
            (8, 1), (8, 5), (8, 11), (8, 16), (8, 18),  # Agoraphobia
            (9, 3), (9, 6), (9, 9), (9, 15), (9, 19),  # Separation Anxiety Disorder
            (10, 2), (10, 5), (10, 11), (10, 17), (10, 18),  # Internet Gaming Disorder
            (11, 1), (11, 3), (11, 9), (11, 16), (11, 19),  # Social Media Addiction
            (12, 4), (12, 7), (12, 11), (12, 15), (12, 18),  # Binge Eating Disorder
            (13, 2), (13, 5), (13, 13), (13, 16), (13, 17),  # Tobacco Use Disorder
            (14, 3), (14, 6), (14, 9), (14, 15), (14, 18),  # Oppositional Defiant Disorder
        ]
        self.cursor.executemany("INSERT INTO condition_techniques (condition_id, technique_id) VALUES (?, ?)", condition_techniques)

        self.conn.commit()
        print("Dummy data populated.")


    def close(self):
        if self.conn:
            self.conn.close()
            print(f"Connection closed for database at '{self.full_path}'.")

    def is_data_populated(self):
        self.cursor.execute("SELECT COUNT(*) FROM clients")
        return self.cursor.fetchone()[0] > 0
    
    def add_dummy_sessions(self):
        clients = self.get_all_clients()
        techniques = self.get_all_techniques()
        components = self.get_all_act_components()
        
        for client in clients:
            for i in range(3):  # Three sessions per client
                session_date = f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d} {random.randint(9,17):02d}:00:00"
                component = random.choice(components)
                technique = random.choice(techniques)
                session_id = self.add_session(
                    client[0], 
                    session_date, 
                    component[0],  # component_id
                    technique[0],  # technique_id
                    f"Sample session notes for {client[1]} using {technique[1]}"
                )
                
                # Add 2-3 techniques per session
                for _ in range(random.randint(2, 3)):
                    technique = random.choice(techniques)
                    self.add_session_technique(
                        session_id, 
                        technique[0], 
                        f"Feedback for {technique[1]}: It was {random.choice(['very effective', 'somewhat effective', 'challenging but useful'])}"
                    )
        
        print("Dummy sessions added.")

    def get_all_act_components(self):
        self.cursor.execute("SELECT * FROM act_components")
        return self.cursor.fetchall()
        def get_client_conditions(self, client_id):
            self.cursor.execute('''
            SELECT DISTINCT c.* 
            FROM conditions c
            JOIN condition_techniques ct ON c.id = ct.condition_id
            JOIN sessions s ON s.technique_id = ct.technique_id
            WHERE s.client_id = ?
            ''', (client_id,))
            return self.cursor.fetchall()
        
    def get_client_conditions(self, client_id):
        self.cursor.execute('''
        SELECT DISTINCT c.* 
        FROM conditions c
        JOIN condition_techniques ct ON c.id = ct.condition_id
        JOIN session_techniques st ON ct.technique_id = st.technique_id
        JOIN sessions s ON s.id = st.session_id
        WHERE s.client_id = ?
        ''', (client_id,))
        return self.cursor.fetchall()