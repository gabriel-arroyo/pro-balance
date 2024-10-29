from openpyxl import load_workbook
from queries import *
from utils import *


def insert_form3_table1(sheet, month, year):
    data = read_query(get_form3_table1_query(month, year))
    write_table(sheet, data, 'B', 13)


def insert_form3_table2(sheet, month, year):
    data = read_query(get_form1_table2_query(month, year))
    write_table(sheet, data, 'B', 52, False, False, True)


def insert_form3_table3(sheet, month, year):
    data = read_query(get_form3_table3_query(month, year))
    write_table(sheet, data, 'B', 79)


def fill_form3(month, year):
    template_xlsx_path, output_xlsx_path = get_file_names(3, month, year)
    workbook = load_workbook(template_xlsx_path)
    sheet = workbook.active

    
    insert_form3_table1(sheet, month, year)
    insert_form3_table2(sheet, month, year)
    insert_form3_table3(sheet, month, year)

    workbook.save(output_xlsx_path)
    print(f"Updated .xlsx file saved as {output_xlsx_path}")


