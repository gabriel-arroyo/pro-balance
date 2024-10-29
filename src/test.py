def write_table(sheet, data, start_letter, start_row, has_id=False, transposed=False, formatted_zero=False, add_totals=False):
    if not data:
        print("No data to insert on form 1 table 1.")
        return

    start_col = letter_to_number(start_letter)

    if (transposed):
        p = 0
        col = start_col

        while p < len(data) + int(add_totals):
            if can_write_cell(sheet, start_row, col):
                for i in range(len(data[1])-int(has_id)):
                    if p < len(data):
                        value = data[p][i + int(has_id)]
                        formatted_value = value if isinstance(
                            value, str) or value > 0 else 'XXX'
                        sheet.cell(start_row + i, col,
                                   value=formatted_value if formatted_zero else value)
                    else:
                        total_formula = f'=SUM({number_to_letter(col)}{start_row}:{
                            number_to_letter(col)}{start_row+i-1})'
                        sheet.cell(start_row + i, col, total_formula)
                    col += 1
                    p += 1
            else:
                col += 1

    else:
        max_col = start_col
        for i in range(len(data)):
            j = 0
            col = start_col
            while j < len(data[i])-int(has_id):
                if can_write_cell(sheet, start_row + i, col):
                    if (j < len(data[i])-int(has_id)):
                        value = data[i][j + int(has_id)]
                        formatted_value = value if isinstance(
                            value, str) or value > 0 else 'XXX'
                        sheet.cell(
                            start_row + i, col, value=formatted_value if formatted_zero else value)
                    else:
                        total_formula = f'=SUM({number_to_letter(start_col)}{
                            start_row + i-1}:{number_to_letter(col)}{start_row+i-1})'
                        sheet.cell(start_row + i, col, total_formula)
                    col += 1
                    j += 1
                else:
                    col += 1
