import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv

import db

def get_csv_data():
    def validate_data(file, entry, dropdown):
        if entry == "" and not dropdown == "None":
            categorize_data(file, dropdown)
        elif not entry == "" and dropdown == "None":
            categorize_data(file, entry)
        else:
            messagebox.showerror("Error", "Enter a new name or select existing")

    def get_file_name(file):

        for widget in main_frame.winfo_children():
            widget.destroy()

        label = tk.Label(
        main_frame,
        text = "Enter bank account name (new CSV):"
        )
        label.pack()
        
        table_name = tk.StringVar()
        name_entry = tk.Entry(
            main_frame,
            textvariable = table_name
            
        )
        name_entry.pack()

        label = tk.Label(
        main_frame,
        text = "Enter bank account name (Existing CSV):"
        )
        label.pack(pady = 20)

        tables = db.get_tables_with_balance_column()
        tables.insert(0, "None")

        print(tables)

        dropdown = ttk.Combobox(main_frame, values=tables)
        dropdown.current(0)
        dropdown.pack(pady =10)

        categorize_btn = tk.Button(
            main_frame,
            text = "Categorize Data",
            command = lambda: validate_data(file, table_name.get().upper(), dropdown.get())

        )
        categorize_btn.pack()
        
    def categorize_data(file, table_name):
        print(table_name)
        
        

        with open(file) as f:
            data = list(csv.reader(f))
            data.pop(0)

            for transaction in data:
                for widget in main_frame.winfo_children():
                    widget.destroy()
                


    def get_csv_file():
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

        if file_path == "":
            messagebox.showerror("Error", "No CSV file was uploaded")
        else:
            get_file_name(file_path)

            
        
        
    has_csv = False

    WIDTH = 500
    HEIGHT = 400

    window = tk.Tk()
    window.title("Upload CSVs")
    window.geometry(f"{WIDTH}x{HEIGHT}")

    main_frame = tk.Frame(window)
    main_frame.pack()

    num_files = 0

    ## Shows how many files user has in the app
    file_label = tk.Label(
        window,
        text = "Total Files Uploaded: "+str(num_files)
    )
    file_label.place(x=5, y = HEIGHT - 30)

    csv_btn = tk.Button(
        main_frame,
        text = "Upload CSV",
        command= get_csv_file
    )
    csv_btn.pack()

    window.mainloop()
get_csv_data()


