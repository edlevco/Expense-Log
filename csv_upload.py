import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv

import db

def get_csv_data():

    db.create_category_table()

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

        tables = db.get_account_tables()
        tables.insert(0, "None")



        dropdown = ttk.Combobox(main_frame, values=tables, state = "readonly")
        dropdown.current(0)
        dropdown.pack(pady =10)

        categorize_btn = tk.Button(
            main_frame,
            text = "Categorize Data",
            command = lambda: validate_data(file, table_name.get().upper(), dropdown.get())

        )
        categorize_btn.pack()
        
    def categorize_data(file, table_name):

        db.create_table(table_name) ## works for both entry and dropdown

        transaction_index = [0]  # mutable index to track current position

        with open(file) as f:
            data = list(csv.reader(f))
            data = data[1:]

            dropdown_var = tk.StringVar()

            def next_transaction(data):

                data.insert(1, dropdown_var.get())
                data.insert(0, table_name)

                print(data)

                transaction_index[0] += 1
                show_transaction()

            
            def get_category(transaction):

                

                if transaction[2] == "":
                    # Income
                    tk.Label(main_frame, text="INCOME:").pack(pady=(10, 0))
                    tk.Label(main_frame, text=transaction[1]).pack()
                    tk.Label(main_frame, text="$" + str(transaction[3]), fg="green").pack()

                    options = db.get_categories_list("income")

                    data = [transaction[0], "income", transaction[3], transaction[4]]

                    

                
                else:
                    # Expense
                    tk.Label(main_frame, text="EXPENSE:").pack(pady=(10, 0))
                    tk.Label(main_frame, text=transaction[1]).pack()
                    tk.Label(main_frame, text="$" + str(transaction[2]), fg="red").pack()

                    options = db.get_categories_list("expense")

                    data = [transaction[0], "expense", transaction[2], transaction[4]]

                # Button to go to the next transaction
                dropdown = ttk.Combobox(main_frame, values=options, state = "readonly", textvariable = dropdown_var)
                dropdown.set(options[0])
                dropdown.pack()

                tk.Button(main_frame, text="Next", command= lambda: next_transaction(data)).pack(pady=20)

        
            def show_transaction():
                for widget in main_frame.winfo_children():
                    widget.destroy()

                if transaction_index[0] < len(data):
                    transaction = data[transaction_index[0]]
                    get_category(transaction)
                else:
                    tk.Label(main_frame, text="All transactions categorized!").pack()
            window.bind("<Return>", lambda event: next_transaction())
            show_transaction()

                

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

    num_files = int(len(db.get_account_tables()))

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


