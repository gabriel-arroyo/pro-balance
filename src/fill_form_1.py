from openpyxl import load_workbook
from queries import *
from utils import *


def insert_form1_table1(sheet, month, year):
    data = read_query(get_form1_table1_query(month, year))
    transposed_data = list(map(list, zip(*data)))[1:]
    write_table(sheet, data, 'D', 26, True, True, False)


def insert_form1_table2(sheet, month, year):
    data = read_query(get_form1_table2_query(month, year))
    write_table(sheet, data, 'B', 69, False, False, True)


def fill_form1(month, year, author, observations1, observations2):
    template_xlsx_path, output_xlsx_path = get_file_names(1, month, year)
    workbook = load_workbook(template_xlsx_path)
    sheet = workbook.active

    insert_cell(sheet, 'J', 19, get_month_name_spanish(month))
    insert_cell(sheet, 'L', 19, f'DEL {year}')
    insert_cell(sheet, 'B', 37, f'{format_date_spanish(date.today())}, RAMOS ARIZPE, COAHUILA')
    insert_cell(sheet, 'J', 39, author)
    insert_cell(sheet, 'D', 32, observations1)
    insert_cell(sheet, 'D', 87, observations2)
    insert_form1_table1(sheet, month, year)
    insert_form1_table2(sheet, month, year)

    workbook.save(output_xlsx_path)
    print(f"Updated .xlsx file saved as {output_xlsx_path}")

