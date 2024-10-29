import os
import sys
import tkinter as tk
from ui_utils import *
from customtkinter import *
from PIL import Image
import tkinter
from tkinter import ttk
# Add parent directory to the system path for imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from queries import get_form1_table1_query, get_form1_table2_query, get_form2_table1_part1_query, get_form2_table1_part2_query, get_form2_table2_query, get_form3_table1_query, get_form3_table3_query
from fill_form_1 import *
from fill_form_2 import *
from fill_form_3 import *


# List of months in Spanish
months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

years = ["2023", "2024"]

# Map month names to their corresponding numbers
month_to_number = {month: idx + 1 for idx, month in enumerate(months)}

 # set initial value

def on_submit(month, year):
    month = get_selected_month(month)
    year = year.get()
    fill_form1(month, year, 'Juan Pérez', 'Esta es una Observación',
           'Esta es otra Observación')
    fill_form2(month, year, 'Juan Pérez')
    fill_form3(month, year)
  
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice,)

def get_selected_month(month_var):
    # Get the selected month from the OptionMenu
    selected_month = month_var.get()
    # Retrieve the corresponding month number
    month_number = month_to_number[selected_month]
    print(f"Selected month: {selected_month}, Month number: {month_number}")
    return month_number

def main():
    app = CTk()
    app.geometry("800x700")
    set_appearance_mode("ligth")
    set_default_color_theme("blue")

    input_frame = CTkFrame(app)
    input_frame.pack(side="left", padx=20, pady=20, fill="y")

    user_input = CTkEntry(input_frame, width=200, placeholder_text="Enter value here")
    user_input.pack(pady=(0, 10))  # Add some vertical padding

    month_var = StringVar(value="Septiembre") 

    month_combobox = CTkOptionMenu(master=input_frame,
                            values=months,
                            command=optionmenu_callback,
                            variable=month_var)
    month_combobox.pack(padx=20, pady=10)

    year_var = IntVar(value=2024) 

    year_combobox = CTkOptionMenu(master=input_frame,
                            values=years,
                            command=optionmenu_callback,
                            variable=year_var)
    year_combobox.pack(padx=20, pady=10)


    submit_button = CTkButton(input_frame, text="Submit", command=lambda: on_submit(month_var, year_var))
    submit_button.pack()

    tabview = CTkTabview(app, width=500, height=600, corner_radius=15)
    tabview.pack(pady=20, padx=20, fill="both", expand=True)

    tabview.add("Formato 1")
    tabview.add("Formato 2")
    tabview.add("Formato 3")
    tabview.set("")

    frame1 = CTkFrame(tabview.tab("Formato 1"), width=500, height=600, corner_radius=15)
    frame1.pack(pady=20, padx=20, fill="both", expand=True)
    frame2 = CTkFrame(tabview.tab("Formato 2"), width=500, height=600, corner_radius=15)
    frame2.pack(pady=20, padx=20, fill="both", expand=True)
    frame3 = CTkFrame(tabview.tab("Formato 3"), width=500, height=600, corner_radius=15)
    frame3.pack(pady=20, padx=20, fill="both", expand=True)

    # Define table configurations
    tables = [
        {
            "query": get_form1_table1_query,
            "params": (9, 2024),
            "headers": ["Existencia anterior", "Comprado", "Sumas", "Consumido", "Existencia final"],
            "columns": ['Concepto', 'Alto Explosivo', 'Agente Explosivo', 'Condon Detonante', 'Conductores', 'Iniciadores'],
            "title": "Form 1 - Table 1",
            "transpose": True
        },
        {
            "query": get_form1_table2_query,
            "params": (9, 2024),
            "headers": [],  # No headers for this table
            "columns": ['factura', 'fecha', 'razon social', 'No. P.G.', 'alto explosivo', 'agente explosivo', 'cordon', 'conductores', 'iniciadores'],
            "title": "Form 1 - Table 2",
            "transpose": False
        },
        {
            "query": get_form2_table1_part1_query,
            "params": (2024,),
            "headers": ["Autorizado comprar anualmente", "Autorizado en modificaciones"],
            "columns": ['Concepto', 'Alto Explosivo', 'Agente Explosivo', 'Condon Detonante', 'Conductores', 'Iniciadores'],
            "title": "Form 2 - Table 1",
            "transpose": True
        },
         {
            "query": get_form2_table1_part2_query,
            "params": (2024,),
            "headers": ["Comprado en enero", 
                        "Comprado en febrero", 
                        "Comprado en marzo", 
                        "Comprado en abril", 
                        "Comprado en mayo", 
                        "Comprado en junio", 
                        "Comprado en julio", 
                        "Comprado en agosto", 
                        "Comprado en septiembre", 
                        "Comprado en octubre", 
                        "Comprado en noviembre", 
                        "Comprado en diciembre"],
            "columns": ['Concepto', 'Alto Explosivo', 'Agente Explosivo', 'Condon Detonante', 'Conductores', 'Iniciadores'],
            "title": "Form 2 - Table 1",
            "transpose": True
        },
        {
            "query": get_form2_table2_query,
            "params": (2024,),
            "headers": ["Consumido en enero", 
                        "Consumido en febrero", 
                        "Consumido en marzo", 
                        "Consumido en abril", 
                        "Consumido en mayo", 
                        "Consumido en junio", 
                        "Consumido en julio", 
                        "Consumido en agosto", 
                        "Consumido en septiembre", 
                        "Consumido en octubre", 
                        "Consumido en noviembre", 
                        "Consumido en diciembre"],
            "columns": ['Concepto', 'Alto Explosivo', 'Agente Explosivo', 'Condon Detonante', 'Conductores', 'Iniciadores'],
            "title": "Form 2 - Table 2",
            "transpose": True
        },
        {
            "query": get_form3_table1_query,
            "params": (9, 2024),
            "headers": [],
            "columns": ['No. P.G.', 'Razon Social', 'Fecha'],
            "title": "Form 2 - Table 2",
            "transpose": False
        },
          {
            "query": get_form3_table3_query,
            "params": (9, 2024),
            "headers": [],
            "columns": ['Fecha', 'No. Voladura', 'Lugar exacto de la voladura', 'Alto explosivo', 'Agente explosivo', 'Cordon Detonante', 'Conductores', 'Iniciadores'],
            "title": "Form 2 - Table 2",
            "transpose": False
        },
    ]


    data11 = get_matrix_data(
            tables[0]["query"], 
            tables[0]["params"], 
            has_headers=True, 
            transpose=tables[0]["transpose"], 
            headers=tables[0]["headers"]
        )
    create_treeview(frame1, data11, tables[0]["columns"], tables[0]["title"])

    data12 = get_matrix_data(
            tables[1]["query"],
            tables[1]["params"],
            has_headers=False,
            transpose=tables[1]["transpose"],
            headers=tables[1]["headers"]
        )
    create_treeview(frame1, data12, tables[1]["columns"], tables[1]["title"])

    data21 = get_matrix_data(
            tables[2]["query"],
            tables[2]["params"],
            has_headers=True,
            transpose=tables[2]["transpose"],
            headers=tables[2]["headers"],
            sum_row=True,
            total_header="Total autorizado comprar por año"
        )
    data212 = get_matrix_data(
            tables[3]["query"],
            tables[3]["params"],
            has_headers=True,
            transpose=tables[3]["transpose"],
            headers=tables[3]["headers"],
            sum_row=True,
            total_header="Total comprado a la fecha"
        )
    create_treeview(frame2, data21 + data212, tables[2]["columns"], tables[2]["title"])

    data22 = get_matrix_data(
            tables[4]["query"],
            tables[4]["params"],
            has_headers=True,
            transpose=tables[4]["transpose"],
            headers=tables[4]["headers"],
            sum_row=True,
            total_header="Total autorizado comprar por año"
        )
    create_treeview(frame2, data22, tables[4]["columns"], tables[4]["title"])

    data31 = get_matrix_data(
            tables[5]["query"],
            tables[5]["params"],
            has_headers=False,
            transpose=tables[5]["transpose"],
            headers=tables[5]["headers"],
            sum_row=False,
        )
    create_treeview(frame3, data31, tables[5]["columns"], tables[5]["title"])

    data32 = get_matrix_data(
            tables[1]["query"],
            tables[1]["params"],
            has_headers=False,
            transpose=tables[1]["transpose"],
            headers=tables[1]["headers"]
        )
    create_treeview(frame3, data32, tables[1]["columns"], tables[1]["title"])

    data33 = get_matrix_data(
            tables[6]["query"],
            tables[6]["params"],
            has_headers=False,
            transpose=tables[6]["transpose"],
            headers=tables[6]["headers"],
            sum_row=False,
        )
    create_treeview(frame3, data33, tables[6]["columns"], tables[6]["title"])

    # Run the Tkinter event loop
    app.mainloop()


# Entry point for the script
if __name__ == "__main__":
    main()
