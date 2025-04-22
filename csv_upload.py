import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import db


def get_csv_data():
    db.create_category_table()

    def validate_data(file, entry, dropdown):
        if entry == "" and dropdown != "None":
            categorize_data(file, dropdown)
        elif entry != "" and dropdown == "None":
            categorize_data(file, entry)
        else:
            messagebox.showerror("Error", "Enter a new name or select an existing one.")

    def get_file_name(file_path):
        for widget in main_frame.winfo_children():
            widget.destroy()

        # New account label and entry
        tk.Label(main_frame, text="Enter a new bank account name:").pack(pady=(10, 0))
        tk.Label(main_frame, text="(Must be one word)").pack(pady=(10, 0))
        table_name_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=table_name_var).pack()

        # Existing account label and dropdown
        tk.Label(main_frame, text="Or select an existing account:").pack(pady=(20, 0))
        tables = db.get_account_tables()
        tables.insert(0, "None")
        table_dropdown = ttk.Combobox(main_frame, values=tables, state="readonly")
        table_dropdown.current(0)
        table_dropdown.pack(pady=10)

        # Button to categorize data
        tk.Button(
            main_frame,
            text="Categorize Data",
            command=lambda: validate_data(file_path, table_name_var.get().upper(), table_dropdown.get())
        ).pack(pady=10)

    def categorize_data(file_path, table_name):
        update_num_files()
        db.create_table(table_name)
        transaction_index = [0]

        with open(file_path) as f:
            reader = csv.reader(f)
            data = list(reader)[1:]  # Skip header

        dropdown_var = tk.StringVar()
        new_category_entry_var = tk.StringVar()

        def show_transaction():
            for widget in main_frame.winfo_children():
                widget.destroy()

            if transaction_index[0] < len(data):
                transaction = data[transaction_index[0]]
                check_if_already_exists(transaction)
            else:
                tk.Label(main_frame, text="🎉 All transactions categorized!").pack(pady=30)

        def check_if_already_exists(transaction):
            existing_data = db.return_data(table_name)
            for row in existing_data:

                ################## Change this to check row[0] and transaction_index[0], then set transaction_index[0] to the last row[0] + 1
                if str(row[1]).strip() == str(transaction[0]).strip() and str(row[5]).strip() == str(transaction[4]).strip():
                    transaction_index[0] += 1
                    show_transaction()
                    return
            ask_for_category(transaction)

        def ask_for_category(transaction):
            amount = transaction[2]
            balance = transaction[4]
            trans_type = "income" if transaction[2] == "" else "expense"
            display_amount = transaction[3] if trans_type == "income" else transaction[2]
            color = "green" if trans_type == "income" else "red"
            label_text = "INCOME" if trans_type == "income" else "EXPENSE"

            # Display info
            tk.Label(main_frame, text=label_text + ":").pack(pady=(10, 0))
            tk.Label(main_frame, text=transaction[1]).pack()
            tk.Label(main_frame, text=f"${display_amount}", fg=color).pack()

            # Dropdown for category
            options = db.get_categories_list(trans_type)
            dropdown = ttk.Combobox(main_frame, values=options, state="readonly", textvariable=dropdown_var)
            dropdown.set(options[0])
            dropdown.pack(pady=10)

            # Entry for add new category
            tk.Label(main_frame, text="Enter New Category Name:").pack(pady=(10, 0))
            tk.Label(main_frame, text="(Only if dropdown is 'Add New')").pack()

            category_entry = tk.Entry(main_frame, textvariable=new_category_entry_var)
            category_entry.pack()
            
            # Next button
            tk.Button(
                main_frame,
                text="Next",
                command=lambda: save_and_next(transaction, dropdown_var.get(), trans_type)
            ).pack(pady=20)

        def save_and_next(transaction, category, trans_type):

            if category == "Add New":

                if new_category_entry_var.get() == "":
                    messagebox.showerror("error", "Enter Category Name Into Entry Box")
                    show_transaction()
                    return

                category = new_category_entry_var.get().capitalize()
                db.add_category(trans_type, category)

            new_category_entry_var.set("")  
            ## resrt entry back to nothing

            # Format: table, date, category, type, amount, balance
            if trans_type == "income":
                amount = float(transaction[3])
            else:
                amount = float(transaction[2])

            amount = float("{:.2f}".format(amount))
            db.add_data(table_name, transaction[0], category, trans_type, amount, transaction[4])
            transaction_index[0] += 1
            show_transaction()

        # Allow pressing Enter to go to next
        window.bind("<Return>", lambda event: show_transaction())

        show_transaction()

    def get_csv_file():
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            messagebox.showerror("Error", "No CSV file was selected.")
        else:
            get_file_name(file_path)

    def run_main():
        window.destroy()

    # GUI window setup
    WIDTH, HEIGHT = 500, 400
    window = tk.Tk()
    window.title("Upload and Categorize CSV")
    window.geometry(f"{WIDTH}x{HEIGHT}")

    main_frame = tk.Frame(window)
    main_frame.pack()
    def update_num_files():
        # Show total uploaded files
        num_files = len(db.get_account_tables())
        tk.Label(window, text=f"Total Files Uploaded: {num_files}").place(x=5, y=HEIGHT - 30)

        if num_files > 0:
            tk.Button(window, text = "Continue to report", command= run_main).place(x = 5, y= HEIGHT - 60)
    update_num_files()
    # Upload button
    tk.Button(
        main_frame,
        text="Upload CSV",
        command=get_csv_file
    ).pack(pady=20)

    window.mainloop()


