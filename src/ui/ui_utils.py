import os
import sys
from tkinter import ttk
import tkinter as tk
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from queries import read_query


def add_sum_row(matrix):
    # Check if the matrix is empty
    if not matrix:
        return matrix
    
    # Calculate the number of columns
    num_columns = len(matrix[0])
    
    # Create a new row for sums
    sum_row = [0] * num_columns
    
    for row in matrix:
        for col_index in range(num_columns):
            sum_row[col_index] += row[col_index]
    
    matrix.append(sum_row)
    
    return matrix

# Function to retrieve and process data
def get_matrix_data(query_func, query_params, has_headers=True, transpose=True, headers=None, sum_row=False, total_header='Total'):
    try:
        # Retrieve the table data based on the query function and parameters
        table_data = read_query(query_func(*query_params))
        
        # Remove the first column if needed
        if has_headers:
            table_data = [row[1:] for row in table_data]
        else:
            table_data = [row for row in table_data]

                    
        # Transpose the matrix if required
        if transpose:
            table_data = list(map(list, zip(*table_data)))
        
        if sum_row:
            table_data = add_sum_row(table_data)
        
        if headers:
            if transpose:
                for i in range(len(table_data)):
                    # Insert the corresponding header for each row
                    # If it's the header row, use the header, else use a placeholder (e.g., "")
                    if i == len(table_data)-1:
                        table_data[i].insert(0, total_header.upper())  # or you can choose to add a specific title for the first cell
                    else:
                        table_data[i].insert(0, headers[i].upper()) 
            else:
                # Add headers as the first row
                headers = [header.upper() for header in headers]
                table_data.insert(0, headers)
        
        return table_data
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return []  # Return an empty list if there's an error

def set_column_widths(tree, columns, data):
    for col in range(len(columns)):
        if not data:  # Check if data is empty
            max_width = len(columns[col])  # If empty, set max_width to the column name length
        else:
            # Use a list comprehension to generate the lengths of the items in the column
            column_lengths = [len(str(row[col])) for row in data if len(row) > col]
            max_length_in_data = max(column_lengths) if column_lengths else 0  # Handle case where there are no lengths
            max_width = max(len(columns[col]), max_length_in_data)

        # Set the column width in the treeview
        tree.column(columns[col], width=max(max_width * 10, 100))



def create_treeview(root, data, columns, title):
    columns = [column.upper() for column in columns]
    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=columns, show="headings", height=min(len(data), 20))  # Set a max height

    # Define column headings
    for col in columns:
        tree.heading(col, text=col.capitalize())

    # Set the column widths
    set_column_widths(tree, columns, data)

    # Insert rows from the data
    for row in data:
        if len(row) == len(columns):
            tree.insert("", "end", values=row)
        else:
            print(f"Row length mismatch: expected {len(columns)}, got {len(row)} for row {row}")

    # Set the height of the Treeview dynamically
    tree.config(height=len(data))

    # Pack the Treeview into the window with a title
    label = tk.Label(root, text=title, font=("Arial", 12))
    label.pack(pady=10)
    tree.pack(pady=10)
