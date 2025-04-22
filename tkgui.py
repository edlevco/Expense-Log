import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime, timedelta

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

def ui(window):
    account_names = db.get_account_tables()
    current_account = account_names[0]

    dates, balances = db.get_plot_data(current_account)
    WINDOW_HEIGHT = window.winfo_height()

    BLUE = "#2C3E50"

    sidebar = tk.Frame(window, width=200, bg=BLUE, height=WINDOW_HEIGHT)
    sidebar.pack(side="left", fill="y")

    content = tk.Frame(window, width=600, height=WINDOW_HEIGHT)
    content.pack(side="right", fill="both", expand=True)

    logo = tk.PhotoImage(file="assets/el.png")
    resized_logo = logo.subsample(4, 4)

    def change_account(new_account):
        nonlocal current_account
        current_account = new_account
        messagebox.showinfo("Account Changed", f"Current account set to: {current_account}")
        show_page("home")

    def show_page(page_name):
        for widget in content.winfo_children():
            widget.destroy()

        if page_name == "scat_plot":
            tk.Label(content, text="📈 Scatter Plot", font=("Arial", 16)).pack(pady=20)

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            ax.set_title("Balance Plot")
            ax.set_xlabel("Date")
            ax.set_ylabel("Balance $")

            ax.plot(dates, balances, marker='o')
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            fig.autofmt_xdate()

            canvas = FigureCanvasTkAgg(fig, master=content)
            canvas.draw()
            canvas.get_tk_widget().pack()

        elif page_name == "bar_graph":
            tk.Label(content, text="📊 Bar Graph", font=("Arial", 16)).pack(pady=10)

            # Frame to hold dropdown and graph
            graph_frame = tk.Frame(content)
            graph_frame.pack()

            selection_var = tk.StringVar(value="expense")  # default

            def update_graph(selection):
                # Clear any existing widgets in graph_frame
                for widget in graph_frame.winfo_children():
                    widget.destroy()

                # Get top 5 for selected type
                data_dict = db.get_total_dict(current_account, selection)
                bar_data = db.get_top_5(data_dict)

                labels = bar_data[0]
                values = bar_data[1]

                fig = Figure(figsize=(5, 4), dpi=100)
                ax = fig.add_subplot(111)

                ax.bar(labels, values)
                ax.set_title(f"Top 5 {selection.capitalize()} Categories")
                ax.set_xlabel("Category")
                ax.set_ylabel("$")
                ax.set_xticklabels(labels, rotation=2, fontsize=7)
                
                canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()

            # Dropdown menu to choose "income" or "expense"
            dropdown = ttk.Combobox(content, textvariable=selection_var, values=["income", "expense"], state="readonly")
            dropdown.pack(pady=5)
            dropdown.bind("<<ComboboxSelected>>", lambda event: update_graph(selection_var.get()))

            # Initialize with default selection
            update_graph(selection_var.get())


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

            for i in range(10):
                home_frame.rowconfigure(i, weight=1)
                home_frame.columnconfigure(i, weight=1)

            total = 0
            for i, account in enumerate(account_names):
                balance = db.get_balance(account)
                total += balance
                tk.Label(home_frame, text=f"{account} Balance: ").grid(row=i, column=0, sticky="w")
                tk.Label(home_frame, text=f"${balance}").grid(row=i, column=1, sticky="w")

                if i == len(account_names) - 1:
                    tk.Label(home_frame, text="Total: ").grid(row=i+1, column=0, sticky="w")
                    tk.Label(home_frame, text=f"${total}").grid(row=i+1, column=1, sticky="w")

            current_date = datetime.now()
            seven_days_ago = current_date - timedelta(days=7)
            start_month = current_date.replace(day=1)

            past_7 = db.get_total_transactions(current_account, seven_days_ago, current_date)
            past_month = db.get_total_transactions(current_account, start_month, current_date)

            tk.Label(home_frame, text="Past 7 Days: ").grid(row=0, column=2, sticky="w")
            tk.Label(home_frame, text=f"${past_7[1]}", fg="green").grid(row=0, column=3, sticky="w")
            tk.Label(home_frame, text=f"${past_7[0]}", fg="red").grid(row=0, column=4, sticky="w")
            tk.Label(home_frame, text=f"-> {past_7[1] - past_7[0]}").grid(row=0, column=5, sticky="w")

            tk.Label(home_frame, text="This Month: ").grid(row=1, column=2, sticky="w")
            tk.Label(home_frame, text=f"${past_month[1]}", fg="green").grid(row=1, column=3, sticky="w")
            tk.Label(home_frame, text=f"${past_month[0]}", fg="red").grid(row=1, column=4, sticky="w")
            tk.Label(home_frame, text=f"-> {past_month[1] - past_month[0]}").grid(row=1, column=5, sticky="w")

        image_label = tk.Label(content, image=resized_logo)
        image_label.image = resized_logo
        image_label.place(x=1, y=1)

    buttons = [
        ("🏠 Home", "home"),
        ("📈 Scatter Plot", "scat_plot"),
        ("📊 Bar Graph", "bar_graph"),
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

    show_page("home")
