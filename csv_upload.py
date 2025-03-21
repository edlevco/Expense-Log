import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv

def get_csv_data():

    def categorize_data(file):
        with open(file) as f:
            data = list(csv.reader(f))
            data.pop(0)

            for transaction in data:



            

    def get_csv_file():
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

        if file_path == "":
            messagebox.showerror("Error", "No CSV file was uploaded")
        else:
            messagebox.showinfo("Info", "Categorize each income and expense")
            categorize_data(file_path)
        
        
    has_csv = False

    WIDTH = 500
    HEIGHT = 400

    window = tk.Tk()
    window.title("Upload CSVs")
    window.geometry(f"{WIDTH}x{HEIGHT}")

    num_files = 0

    
    label = tk.Label(
        window,
        text = "Enter bank account name:"
    )
    label.pack()
    

    name_entry = tk.Entry(
        window,
        
    )


    ## Shows how many files user has in the app
    file_label = tk.Label(
        window,
        text = "Total Files Uploaded: "+str(num_files)
    )
    file_label.place(x=5, y = 5)

    csv_btn = tk.Button(
        window,
        text = "Upload CSV",
        command= get_csv_file
    )
    csv_btn.pack()


    window.mainloop()

get_csv_data()


