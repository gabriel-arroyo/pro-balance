import os
import sqlite3
import pytesseract
from pdf2image import convert_from_path
import re

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\GAARROY\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def get_or_create_product_category_id_by_material(cursor, material_name):
    # Check if the material category already exists
    query = """
    SELECT id FROM product_categories WHERE category = ?
    """
    cursor.execute(query, (material_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]  # Return the id if found
    else:
        # Insert the new material category if not found
        insert_query = """
        INSERT OR IGNORE INTO product_categories (category) VALUES (?)
        """
        cursor.execute(insert_query, (material_name,))
        
        # Get the id of the newly inserted category
        return cursor.lastrowid  # Return the last inserted row id

def add_authorized_buying_quantity(cursor, category_id, authorized_quantity, year, date):
    """Add a new authorized buying quantity to the authorized_buying_quantities table."""
    query = """
    INSERT OR IGNORE INTO authorized_buying_quantities (category_id, authorized_quantity, year, date)
    VALUES (?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (category_id, authorized_quantity, year, date))
    except Exception as e:
        print(f"Error adding authorized buying quantity: {e}")


def extract_date_from_text(text):
    """Extract the date from the line that comes after the target company line."""
    lines = text.splitlines()
    date_pattern = r"(\d{2})\s+de\s+([a-z]+)\s+de\s+(\d{4})"  # Regex to capture date format
    
    month_mapping = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 'mayo': '05', 'junio': '06',
        'julio': '07', 'agosto': '08', 'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    # Loop through lines to find the company line
    for i, line in enumerate(lines):
        if 'HOLCIM' in line:
            # Look for the date on the next line
            if i + 1 < len(lines):
                date_line = lines[i + 1]
                date_match = re.search(date_pattern, date_line.lower())
                if date_match:
                    day = date_match.group(1)
                    month_text = date_match.group(2)
                    year = date_match.group(3)

                    month = month_mapping.get(month_text, '00')  # Convert month name to number
                    formatted_date = f"{year}-{month}-{day}"
                    return formatted_date

    return None  # Return None if no date is found


def extract_table_from_text(text):
    # Split the text into lines and filter out empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Find the start of the table and extract relevant lines
    table_start = False
    table_data = []
    
    for line in lines:
        if "Número de | Material autorizado de | Cantidad máxima de almacenamiento Unidad de" in line:
            table_start = True
            continue  # Skip the header line
        
        if table_start:
            # Use regex to match the expected format, including optional trailing pipe
            match = re.match(r"(\d+)\s+(.*?)\s+([\d,]+)\s+\(.*?\)\s+(\w+)\s*\|?$", line)
            if match:
                # Extract the matched groups
                num_polvorin = match.group(1)
                material = match.group(2).strip()
                cantidad_maxima = match.group(3).replace(',', '')  # Remove commas from numbers
                unidad = match.group(4).strip()
                
                # Append extracted data as a dictionary
                table_data.append({
                    "Numero de Polvorin": num_polvorin,
                    "Material autorizado": material,
                    "Cantidad maxima de almacenamiento": int(cantidad_maxima),  # Convert to integer
                    "Unidad de medida": unidad
                })

    return table_data

def pdf_to_text_with_ocr(pdf_path):
    """Convert PDF to text using OCR."""
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image, lang='spa')
    return text

def extract_year_from_line(text, target_line):
    """Extract the year number from a line containing the target text and 'para el año'."""
    text_lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in text_lines:
        if target_line in line:
            # Check if 'para el año' is in the line
            if 'para el año' in line:
                words = line.split()
                # Find the index of 'para' and get the word after 'año'
                if 'año' in words:
                    index = words.index('año')
                    if index + 1 < len(words):  # Ensure the year follows 'año'
                        return words[index + 1]  # Return the year number
    return None
# Return None if the line is not found

def read_all_pdfs_in_folder(folder_path):
    """Read all PDF files in the specified folder and return their text."""
    pdf_data = {}
    target_text = "DEL PERMISO GENERAL"
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            try:
                extracted_text = pdf_to_text_with_ocr(pdf_path)
                year = extract_year_from_line(extracted_text, target_text)
                year = int(year.rstrip('.')) if year else None
                date = extract_date_from_text(extracted_text)
                pdf_data[filename] = {
                    'text': extracted_text,
                    'year': year,
                    'date': date
                }
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return pdf_data

# Example usage
folder_path = r'C:/Users/GAARROY/repos/excel_report/src/pdf/authorizations'
db_path = 'C:/Users/GAARROY/repos/excel_report/db/inventory.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

all_pdf_data = read_all_pdfs_in_folder(folder_path)

# Print the extracted text and year from each PDF
for pdf_file, data in all_pdf_data.items():
    print(f"--- Text from {pdf_file} ---")
    print(data['text'])
    print(f"Date extracted: {data['date']}\n")
    print(f"Year extracted: {data['year']}\n")
    
    extracted_table = extract_table_from_text(data['text'])
    
    for row in extracted_table:
        # Get the material name from the row
        material_name = row['Material autorizado']

        # Fetch the product category id by material name
        product_category_id = get_or_create_product_category_id_by_material(cursor, material_name)

        if product_category_id is not None:
            add_authorized_buying_quantity(cursor, product_category_id, row['Cantidad maxima de almacenamiento'], data['year'], data['date'])
        else:
            print(f"Category ID not found for material: {row['Material autorizado']}")

        # Add product_category_id to the row dictionary
        row['product_category_id'] = product_category_id
        
        # Print the row with product_category_id included
        print(row)

conn.commit()
conn.close()
