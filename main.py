
from tkgui import ui
import tkinter as tk
import csv_upload



# Call the function to run the app
csv_upload.get_csv_data()

# Create the main window
window = tk.Tk()
window.title("Expense Log")
window.geometry("800x500")  # Adjust size as needed

ui(window)

# Run the Tkinter loop
window.mainloop()


