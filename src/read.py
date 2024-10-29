import sqlite3
import os
from queries import *


def read_previous_existence():
    # Connect to the SQLite database
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    query = get_form1_table1_query(9, 2023)

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                row[0], row[1], row[2], row[3], row[4], row[5]))

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()


# Call the function to read previous existence
read_previous_existence()
