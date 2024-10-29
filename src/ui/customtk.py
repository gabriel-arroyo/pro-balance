from customtkinter import *
from PIL import Image
import tkinter
from tkinter import ttk

app = CTk()
app.geometry("600x700")
set_appearance_mode("dark")

set_default_color_theme("green")

tabview = CTkTabview(app, width=500, height=600, corner_radius=15)
tabview.pack(pady=20, padx=20)

tabview.add("Tab 1")
tabview.add("Tab 2")
tabview.add("Tab 3")

# Create a Frame to hold all the widgets
frame = CTkFrame(tabview.tab("Tab 1"), width=500, height=600, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)
frame2 = CTkFrame(tabview.tab("Tab 2"), width=500, height=600, corner_radius=15)
frame2.pack(pady=20, padx=20, fill="both", expand=True)


optionmenu_var = StringVar(value="option 2")  # set initial value

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

combobox = CTkOptionMenu(master=frame2,
                                       values=["option 1", "option 2"],
                                       command=optionmenu_callback,
                                       variable=optionmenu_var)
combobox.pack(padx=20, pady=10)


def change_handler(value):
    print(f"Selected value: {value}")


def click_handler():
    print(f"Entered value: {entry.get()}")


# Create widgets inside the frame
label = CTkLabel(frame, text="Hello World", font=("Arial", 20, "bold"))
label.pack(pady=10)

combobox = CTkComboBox(frame, values=["Option 1", "Option 2", "Option 3"], font=(
    "Arial", 14, "bold"), command=change_handler)
combobox.pack(pady=10)

img = Image.open("./src/ui/message.png")
btn = CTkButton(frame, text="Click Me", corner_radius=32, fg_color="#FF2234", hover_color="#BB2253",
                image=CTkImage(dark_image=img, light_image=img), border_color="#6F2234",
                border_width=3, command=click_handler)
btn.pack(pady=10)

checkbox = CTkCheckBox(frame, text="Remember Me", font=("Arial", 16, "bold"),
                       fg_color="#FF2234", checkbox_height=30, checkbox_width=30, corner_radius=36)
checkbox.pack(pady=10)

switch = CTkSwitch(frame, text="Dark Mode", font=("Arial", 16, "bold"),
                   button_color="#FF2234", button_hover_color="#BB2253", progress_color="#6F2234", corner_radius=36)
switch.pack(pady=10)

slider = CTkSlider(frame, from_=0, to=100, orientation=HORIZONTAL,
                   button_color="#FF2234", button_hover_color="#BB2253", progress_color="#6F2234", corner_radius=36)
slider.pack(pady=10)

entry = CTkEntry(frame, placeholder_text="Enter your name", font=("Arial", 16, "bold"),
                 fg_color="#FF2234", border_color="#6F2234", border_width=3, corner_radius=36, width=300)
entry.pack(pady=10)

textbox = CTkTextbox(frame, font=("Arial", 16, "bold"), fg_color="#FF2234",
                     border_color="#6F2234", border_width=2, corner_radius=12, width=300, height=100)
textbox.pack(pady=10)

treeview = ttk.Treeview(frame, columns=('concepto', 'altoexplosivo', 'agenteexplosivo',
                        'condondetonante', 'conductores', 'iniciadores'), show="headings")
treeview.heading("concepto", text="Concepto")
treeview.heading("altoexplosivo", text="Alto Explosivo")
treeview.heading("agenteexplosivo", text="Agente Explosivo")
treeview.heading("condondetonante", text="Conductor Detonante")
treeview.heading("conductores", text="Conductores")
treeview.heading("iniciadores", text="Iniciadores")
treeview.insert("", 0, values=(
    "Existencia Anterior", 125, 50, 200, 75, 300))
treeview.pack(pady=10)

app.mainloop()
