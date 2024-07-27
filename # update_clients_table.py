# update_clients_table.py
import sqlite3
import os

def update_clients_table(db_path, db_name):
    full_path = os.path.join(db_path, db_name)
    
    if not os.path.exists(full_path):
        print(f"Database not found at {full_path}")
        return

    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()

    try:
        # Check if the 'archived' column exists
        cursor.execute("PRAGMA table_info(clients)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'archived' not in columns:
            # Add the 'archived' column if it doesn't exist
            cursor.execute("ALTER TABLE clients ADD COLUMN archived INTEGER DEFAULT 0")
            print("Added 'archived' column to clients table.")
        else:
            print("'archived' column already exists in clients table.")

        # Ensure all existing records have the archived field set to 0
        cursor.execute("UPDATE clients SET archived = 0 WHERE archived IS NULL")
        
        conn.commit()
        print("Clients table updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = r'C:\Users\John.J.Diaz\progs'
    db_name = 'act_tool.db'
    update_clients_table(db_path, db_name)