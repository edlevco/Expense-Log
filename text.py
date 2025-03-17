import tkinter as tk
from tkinter import ttk

# Sample data (replace this with your actual data)
data = [["Item 1", "Choose for Item 1"], ["Item 2", "Choose for Item 2"], ["Item 3", "Choose for Item 3"]]

# Current index tracker
current_index = 0

# Function to handle selection and move to the next item
def next_item():
    global current_index

    # Get selected value from dropdown
    selected_value = dropdown_var.get()
    print(f"User selected: {selected_value} for {data[current_index][1]}")  # Debugging output

    # Move to next item
    current_index += 1
    
    if current_index < len(data):
        update_ui()
    else:
        label.config(text="✅ All items completed!")
        dropdown.pack_forget()  # Hide dropdown
        next_button.pack_forget()  # Hide button

# Function to update UI with next item
def update_ui():
    label.config(text=data[current_index][1])  # Update label
    dropdown_var.set(options[0])  # Reset dropdown selection

# Tkinter setup
window = tk.Tk()
window.title("Dropdown Selection")
window.geometry("400x300")

# Label to show the current item
label = tk.Label(window, text="", font=("Arial", 14))
label.pack(pady=20)

# Dropdown menu
options = ["Option 1", "Option 2", "Option 3"]  # Replace with your own choices
dropdown_var = tk.StringVar(window)
dropdown = ttk.Combobox(window, textvariable=dropdown_var, values=options, state="readonly")
dropdown.pack()

# Button to move to next item
next_button = tk.Button(window, text="Next", command=next_item)
next_button.pack(pady=20)

# Start with the first item
update_ui()

# Run the Tkinter loop
window.mainloop()
