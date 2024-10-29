from openpyxl import load_workbook
from queries import *
from utils import *


def insert_form2_table1(sheet, year):
    data1 = read_query(get_form2_table1_part1_query(year))
    write_table(sheet, data1, 'C', 23, has_id=True,
                transposed=True)
    # add_results(sheet, start_letter='C', start_row=23, num_rows=2,
    #             num_cols=5, transposed=True, result_formula=None)

    data2 = read_query(get_form2_table1_part2_query(year))
    write_table(sheet, data2, 'C', 26, has_id=True,
                transposed=True)
    # add_results(sheet, start_letter='C', start_row=26, num_rows=12,
    #             num_cols=5, transposed=True, result_formula=None)


def insert_form2_table2(sheet, year):
    data = read_query(get_form2_table2_query(year))
    write_table(sheet, data, 'C', 51, has_id=True,
                transposed=True)


def fill_form2(month, year, author):
    template_xlsx_path, output_xlsx_path = get_file_names(2, month, year)
    workbook = load_workbook(template_xlsx_path)
    sheet = workbook.active

    insert_cell(sheet, 'A', 68, f'{format_date_spanish(date.today())}, RAMOS ARIZPE, COAHUILA')
    insert_cell(sheet, 'I', 70, author)
    insert_form2_table1(sheet, year)
    insert_form2_table2(sheet, year)

    workbook.save(output_xlsx_path)
    print(f"Updated .xlsx file saved as {output_xlsx_path}")

