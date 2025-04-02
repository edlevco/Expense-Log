import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
import db


def ui(window):
    account_names = db.get_account_tables()
    current_account = account_names[0]

    data = db.return_data(current_account)

    total = 0

    for row in data:
        if row[2] == "Dining Out":
            print(row[4])
            total += row[4]

    print(f"total:" + str(total))


    WINDOW_HEIGHT = window.winfo_height()

    # Define colors
    BLUE = "#2C3E50"  # Dark sidebar

    # Create sidebar frame (left panel)
    sidebar = tk.Frame(window, width=200, bg=BLUE, height=WINDOW_HEIGHT)
    sidebar.pack(side="left", fill="y")

    # Create main content frame (right panel)
    content = tk.Frame(window, width=600, height=WINDOW_HEIGHT)
    content.pack(side="right", fill="both", expand=True)

    # Store image globally to prevent garbage collection
    logo = tk.PhotoImage(file="assets/el.png")  # Ensure the path is correct
    resized_logo = logo.subsample(4, 4)

    # Function to change the current account
    def change_account(new_account):
        nonlocal current_account
        current_account = new_account
        messagebox.showinfo("Account Changed", f"Current account set to: {current_account}")
        show_page("home")

    # Function to change content based on button click
    def show_page(page_name):
        # Clear previous widgets in content frame
        for widget in content.winfo_children():
            widget.destroy()

        if page_name == "visualize":
            tk.Label(content, text="📊 Data Visualization", font=("Arial", 16)).pack(pady=20)

        elif page_name == "add_csv":
            tk.Label(content, text="To create a new CSV / Account or add new data \n-> Close and re-open the app", font=("Arial", 16)).pack(pady=20)
            tk.Entry(content, width=30).pack(pady=5)




        elif page_name == "change_account":
            tk.Label(content, text="Select an Account:", font=("Arial", 14)).pack(pady=10)
            for name in account_names:
                tk.Button(content, text=name, font=("Arial", 12), command=lambda n=name: change_account(n)).pack(pady=5)

        else:
            tk.Label(content, text="🏠 Home Page", font=("Arial", 16)).pack(pady=20)
            tk.Label(content, text=f"Current account: {current_account}", font=("Arial", 12)).pack(pady=5)

            home_frame = tk.Frame(content)
            home_frame.pack(expand=True, fill="both")

            # Configure 10 rows and 10 columns to expand evenly
            for i in range(10):
                home_frame.rowconfigure(i, weight=1)
                home_frame.columnconfigure(i, weight=1)
            total = 0
            for i, account in enumerate(account_names):
                
                balance = db.get_balance(account)
                total += balance
                tk.Label(home_frame, text = account + "Balance: ").grid(row = i, column = 0, sticky="w")
                tk.Label(home_frame, text = "$" + str(balance)).grid(row = i, column = 1, sticky = "w" )

                if i == len(account_names) - 1:
                    tk.Label(home_frame, text = "Total: ").grid(row = i+1, column = 0, sticky="w")
                    tk.Label(home_frame, text = "$" + str(total)).grid(row = i+1, column = 1, sticky = "w" )









            



        # Display the logo
        image_label = tk.Label(content, image=resized_logo, bg="white")
        image_label.image = resized_logo  # Keep a reference
        image_label.place(x=10, y=10)

    # Create sidebar buttons
    buttons = [
        ("🏠 Home", "home"),
        ("📊 Visualize", "visualize"),
        ("➕ Upload CSV", "add_csv"),
        ("🔄 Change Accounts", "change_account")
    ]

    for text, page in buttons:
        btn = tk.Button(
            sidebar, text=text, font=("Arial", 12), fg="black", bg=BLUE,
            activebackground="#34495E", activeforeground="white", bd=0,
            command=lambda p=page: show_page(p)
        )
        btn.pack(fill="x", pady=5, padx=10)

    # Show home page by default
    show_page("home")
