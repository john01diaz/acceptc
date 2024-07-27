import sqlite3
import os

def update_techniques_table(db_path, db_name):
    full_path = os.path.join(db_path, db_name)
    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()

    # Rename the existing techniques table
    cursor.execute("ALTER TABLE techniques RENAME TO techniques_old")

    # Create the new techniques table
    cursor.execute('''
    CREATE TABLE techniques (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        instructions TEXT,
        act_component_id INTEGER,
        FOREIGN KEY (act_component_id) REFERENCES act_components (id)
    )
    ''')

    # Populate the new table with updated data
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

    cursor.executemany("INSERT INTO techniques (name, category, description, instructions, act_component_id) VALUES (?, ?, ?, ?, ?)", techniques)

    # Update other tables that reference techniques
    cursor.execute('''
    UPDATE condition_techniques
    SET technique_id = (SELECT id FROM techniques WHERE name = (SELECT name FROM techniques_old WHERE id = condition_techniques.technique_id))
    ''')

    cursor.execute('''
    UPDATE sessions
    SET technique_id = (SELECT id FROM techniques WHERE name = (SELECT name FROM techniques_old WHERE id = sessions.technique_id))
    ''')

    cursor.execute('''
    UPDATE session_techniques
    SET technique_id = (SELECT id FROM techniques WHERE name = (SELECT name FROM techniques_old WHERE id = session_techniques.technique_id))
    ''')

    # Drop the old table
    cursor.execute("DROP TABLE techniques_old")

    conn.commit()
    conn.close()

    print("Techniques table updated successfully.")

if __name__ == "__main__":
    db_path = r'C:\Users\John.J.Diaz\progs'  # Update this path to match your database location
    db_name = 'act_tool.db'
    update_techniques_table(db_path, db_name)