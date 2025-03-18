
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv


def ui(window):

    WINDOW_HEIGHT = window.winfo_height()
    

        # Define colors
    BLUE = "#2C3E50"  # Dark sidebar

    # Create sidebar frame (left panel)
    sidebar = tk.Frame(window, width=200, bg=BLUE, height=WINDOW_HEIGHT)
    sidebar.pack(side="left", fill="y")

    # Create main content frame (right panel)
    content = tk.Frame(window, width=600, height=WINDOW_HEIGHT, bg="white")
    content.pack(side="right", fill="both", expand=True)

    # **Store Image Globally to Prevent Garbage Collection**
    logo = tk.PhotoImage(file="assets/el.png")  # Make sure the path is correct
    resized_logo = logo.subsample(4,4)

    def upload_csv():
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
        messagebox.showinfo("Info", "CSV file uploaded successfully")

        with open(file_path) as file:
            
            data = list(csv.reader(file))
            data.pop(0)

            item_num = 0

            label = tk.Label(content, text = "")
            label.pack()









            
        


    # Function to change content based on button click
    def show_page(page_name):
        # Clear previous widgets in content frame
        for widget in content.winfo_children():
            widget.destroy()


        
        if page_name == "visualize":
            tk.Label(content, text="📊 Data Visualization", font=("Arial", 16)).pack(pady=20)
        elif page_name == "add_income":
            tk.Label(content, text="💰 Add Income", font=("Arial", 16)).pack(pady=20)
            tk.Entry(content, width=30).pack(pady=5)  # Input field example
        elif page_name == "add_expense":
            tk.Label(content, text="💸 Add Expense", font=("Arial", 16)).pack(pady=20)
            tk.Entry(content, width=30).pack(pady=5)  # Input field example
        elif page_name == "add_csv":
            # Create Upload Button
            btn_upload = tk.Button(content, text="Upload CSV", command=upload_csv, padx=10, pady=5)
            btn_upload.pack(pady=20)
        else:
            tk.Label(content, text="🏠 Home Page", font=("Arial", 16)).pack(pady=20)



        # **Display the Image Inside Content Frame**
        image_label = tk.Label(content, image=resized_logo, bg="white")
        image_label.place(x=10, y=10)

    # Create sidebar buttons
    buttons = [
        ("🏠 Home", "home"),
        ("📊 Visualize", "visualize"),
        ("💰 Add Income", "add_income"),
        ("💸 Add Expense", "add_expense"),
        ("➕ Upload CSV", "add_csv")
    ]

    for text, page in buttons:
        btn = tk.Button(sidebar, text=text, font=("Arial", 12), fg=BLUE,
                        activebackground="#34495E", activeforeground="white", bd=0,
                        command=lambda p=page: show_page(p))
        btn.pack(fill="x", pady=5, padx=10)

    # Show home page by default
    show_page("home")
