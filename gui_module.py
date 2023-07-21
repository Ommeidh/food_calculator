# gui_module.py

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import nutritionix_module
import excel_module
import datetime
import os
import pandas as pd

class FoodLogger:
    def __init__(self, master):
        self.master = master
        master.title('My Nutrition Logger')
        master.geometry("800x600")  # double the size

        self.filename = None
        self.food_log = []

        tk.Label(master, text="Food Item").grid(row=0)
        self.e1 = tk.Entry(master, font=('Arial', 14), width=60)
        self.e1.grid(row=0, column=1)

        tk.Label(master, text="Quantity").grid(row=1)
        self.e2 = tk.Entry(master, font=('Arial', 14), width=60)
        self.e2.grid(row=1, column=1)

        tk.Label(master, text="Date (mm/dd/yyyy):").grid(row=2)
        self.e3 = tk.Entry(master, font=('Arial', 14), width=60)
        self.e3.grid(row=2, column=1)

        tk.Button(master, text='Log Food', command=self.log_food).grid(row=3, column=0, sticky=tk.W, pady=4)
        tk.Button(master, text='Import to Excel', command=self.import_to_excel).grid(row=3, column=1, sticky=tk.W, pady=4)

        self.text_frame = tk.Frame(master)
        self.text_frame.grid(row=4, column=0, columnspan=2)

        self.text = tk.Text(self.text_frame, height=10, width=80, font=('Arial', 14), borderwidth=0)  # Set borderwidth to 0
        self.text.pack(expand=True, fill='both')

        tk.Button(master, text='Select Excel File', command=self.select_excel_file).grid(row=5, column=0, pady=4)
        tk.Button(master, text='Create New Log', command=self.create_new_log).grid(row=5, column=1, pady=4)

    def log_food(self):
        quantity = int(self.e2.get())
        food_info = nutritionix_module.get_food_info(self.e1.get(), quantity)
        if food_info is None:
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, f"No food data found for {self.e1.get()}")
        else:
            date = self.e3.get() if self.e3.get() else datetime.datetime.now().strftime('%m/%d/%Y')
            food_info['Date'] = date
            food_info['Calories'] *= float(self.e2.get())
            food_info['Total Fat'] *= float(self.e2.get())
            food_info['Carbohydrates'] *= float(self.e2.get())
            food_info['Protein'] *= float(self.e2.get())
            food_info['Dietary Fiber'] *= float(self.e2.get())

            # Append the food_info dictionary directly
            self.food_log.append(food_info)
            self.update_food_log()

    def update_food_log(self):
        self.text.delete(1.0, tk.END)

        if not self.food_log:  # Check if food_log is empty
            return

        headers = ['Attribute', 'Value']
        table_data = [['Date:', self.food_log[-1]['Date']],
                      ['Food Name:', self.food_log[-1]['Food Name']],
                      ['Calories:', f"{self.food_log[-1]['Calories']:.2f}"],
                      ['Total Fat:', f"{self.food_log[-1]['Total Fat']:.2f}"],
                      ['Carbohydrates:', f"{self.food_log[-1]['Carbohydrates']:.2f}"],
                      ['Protein:', f"{self.food_log[-1]['Protein']:.2f}"],
                      ['Dietary Fiber:', f"{self.food_log[-1]['Dietary Fiber']:.2f}"]]

        table_df = pd.DataFrame(table_data, columns=headers)
        table_str = table_df.to_string(index=False, justify='left')

        self.text.insert(tk.INSERT, table_str)

        # Bold attribute names and column headers
        for i in range(len(headers)):
            self.text.tag_configure(f'header{i}', font=('Arial', 14, 'bold'))
            self.text.tag_add(f'header{i}', f'1.{7*i}', f'1.{7*(i+1)}')
        for i in range(len(headers)):
            self.text.tag_configure(f'column{i}', font=('Arial', 14))
            self.text.tag_add(f'column{i}', f'2.{7*i}', f'2.{7*(i+1)}')

    def import_to_excel(self):
        if self.filename is None:
            messagebox.showwarning("No Excel File", "Please select an Excel file first.")
            return
        if not self.food_log:
            messagebox.showwarning("No Data", "No food data to import.")
            return

        # Prepare data in the format that can be written to the Excel sheet
        food_data_for_excel = []
        for food_info in self.food_log:
            data_row = [
                food_info['Date'],
                food_info['Food Name'],
                round(food_info['Calories'], 2),
                round(food_info['Total Fat'], 2),
                round(food_info['Carbohydrates'], 2),
                round(food_info['Protein'], 2),
                round(food_info['Dietary Fiber'], 2)
            ]
            food_data_for_excel.append(data_row)

        excel_module.add_food_data(self.filename, food_data_for_excel)
        self.food_log = []
        self.update_food_log()
        messagebox.showinfo("Data Imported", "Food data has been imported to the Excel file successfully.")

    def select_excel_file(self):
        if self.filename:
            initial_dir = os.path.dirname(self.filename)
        else:
            initial_dir = os.getcwd()  # Use the current working directory if no file has been selected before

        self.filename = filedialog.askopenfilename(initialdir=initial_dir, title="Select file", filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
        excel_module.load_existing_workbook(self.filename)  # Use the new function instead

    def create_new_log(self):
        filename = f"nutritional_log_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.xlsx"
        excel_module.create_workbook(filename)
        self.filename = filename

def init_gui():
    master = tk.Tk()
    FoodLogger(master)
    master.mainloop()
