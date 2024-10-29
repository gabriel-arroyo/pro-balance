import os
import pdfplumber
import re
from datetime import datetime
import sqlite3

# Function to extract and format the date from text
def extract_and_format_date(text):
    date_pattern = r'\d{2}/[a-zA-Z]{3}\./\d{4}'
    date_match = re.search(date_pattern, text)

    if date_match:
        date_str = date_match.group(0)
        month_mapping = {
            'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06',
            'jul': '07', 'ago': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
        }
        day, month_abbr, year = date_str.split('/')
        month_num = month_mapping[month_abbr.lower().replace('.', '')]
        formatted_date = f"{year}-{month_num}-{day}"
        return formatted_date
    return None

# Function to extract the table from the PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'

    text_lines = text.split('\n')
    text_lines = [line.strip() for line in text_lines if line.strip()]

    # Extract the order details
    supplier = text_lines[0]
    date = extract_and_format_date(text_lines[8])
    invoice_number = text_lines[4]
    permit = text_lines[13].split(f'Permiso: ')[1].strip().rstrip('.')
    address = text_lines[1]
    email = text_lines[3].split(' / ')[0].strip()
    website = email.split('@')[1].strip()
    phone = ''

    address_line1 = text_lines[1]
    address_line2 = text_lines[2]

    # Extract the last 6 digits from the first line
    phone_part1 = re.search(r'\d{3}\s?\d{3}$', address_line1)

    # Extract the first 4 digits from the second line
    phone_part2 = re.search(r'^\d{2}\s?\d{2}', address_line2)
        
    if phone_part1 and phone_part2:
        # Combine the two parts to form the full phone number
        phone = f"{phone_part1.group(0)} {phone_part2.group(0)}"
        address = address.replace(phone_part1.group(0), '').strip()
        

    # Extract the table portion
    start_keyword = "CLAVE DESCRIPCIÓN U.MED. CANTIDAD PRECIO"
    end_keyword = "Son ***"
    start_idx = text.find(start_keyword)
    end_idx = text.find(end_keyword)

    if start_idx == -1 or end_idx == -1:
        print("Table not found.")
        return None, supplier, invoice_number, date, permit
    
    table_text = text[start_idx:end_idx].strip()
    table_lines = table_text.split('\n')
    table_lines = [line for line in table_lines if line.strip()]

    # Process the table lines into structured data
    extracted_table = []
    i = 1
    while i < len(table_lines):
        product_line = table_lines[i].strip()
        description_line = table_lines[i + 1].strip() if i + 1 < len(table_lines) else ''
        parts = product_line.split()
        unit = parts[-4]
        quantity = parts[-3]
        unit_price = parts[-2]
        total_price = parts[-1]
        description = ' '.join(parts[1:-4])

        row = {
            'Product Code': parts[0],
            'Description': description,
            'Unit': unit,
            'Quantity': quantity,
            'Unit Price': unit_price,
            'Total Price': total_price
        }
        extracted_table.append(row)
        i += 2

    return extracted_table, supplier, address, phone, email, website, invoice_number, date, permit

# Function to insert data into the database
def insert_order_and_items(db_path, table_data, supplier_name, address, phone, email, website, invoice_number, date, permit):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Insert supplier if not exists
        cursor.execute(
            "INSERT OR IGNORE INTO suppliers (name, address, phone, email, website) VALUES (?, ?, ?, ?, ?)",
            (supplier_name, address, phone, email, website)
        )
        supplier_id = cursor.execute("SELECT id FROM suppliers WHERE name = ?", (supplier_name,)).fetchone()[0]

        # Insert order
        cursor.execute("INSERT OR IGNORE INTO orders (invoice, date, supplier_id, status) VALUES (?, ?, ?, ?)",
                       (invoice_number, date, supplier_id, 'completed'))
        order_id = cursor.lastrowid

        # Check if the order was inserted
        if order_id is None or order_id == 0:
            print(f"Order with invoice number '{invoice_number}' already exists. Exiting the operation.")
            return  

        # Insert supplier permit
        cursor.execute("INSERT OR IGNORE INTO supplier_permits (supplier_id, permit, issue_date, updated_date) VALUES (?, ?, ?, ?)",
                       (supplier_id, permit, date, date))

        # Insert order items
        for item in table_data:
            cursor.execute("INSERT INTO products (name, supplier_id, unit) VALUES (?, ?, ?) ON CONFLICT(name) DO NOTHING",
                           (item['Description'], supplier_id, item['Unit']))
            product_id = cursor.execute("SELECT id FROM products WHERE name = ?", (item['Description'],)).fetchone()[0]

            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                           (order_id, product_id, item['Quantity']))

    print("Order and items inserted successfully.")

# Example usage
year = '2024'
month = '09'
pdf_directory = f'C:/Users/GAARROY/repos/excel_report/src/pdf/invoice/{year}-{month}'

# Get all PDF files in the specified directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Process each PDF file
db_path = 'C:/Users/GAARROY/repos/excel_report/db/inventory.db'

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)
    print(f"Processing {pdf_path}...")
    
    table_data, supplier_name, address, phone, email, website, invoice_number, date, permit = extract_table_from_pdf(pdf_path)

    if table_data:
        insert_order_and_items(db_path, table_data, supplier_name, address, phone, email, website, invoice_number, date, permit)