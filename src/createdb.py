import sqlite3
import os

def create_tables_from_sql(sql_file, db_path):
    # Check if the SQL file exists
    if not os.path.exists(sql_file):
        print(f"Error: SQL file '{sql_file}' not found.")
        return

    conn = None  # Initialize conn to None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Read the SQL file
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Execute the SQL script
        cursor.executescript(sql_script)

        # Commit changes
        conn.commit()

        print(f"Tables created successfully from {sql_file}")

    except sqlite3.Error as e:
        # Handle SQLite errors
        print(f"SQLite error: {e}")

    except Exception as e:
        # Handle other errors
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed, but only if it was successfully created
        if conn:
            conn.close()

# Get the current script directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Move one level up
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))

# Path to the file one level up
schema_path = os.path.join(parent_directory, 'db', 'schema.sql')
db_path = os.path.join(parent_directory, 'db', 'inventory.db')

# Call the function with the SQL file
create_tables_from_sql(schema_path, db_path)
