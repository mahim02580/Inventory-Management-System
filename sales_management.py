import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
class SalesFrame(tk.Frame):
    def __init__(self, parent, dbms):
        super().__init__(parent, bg="white")
        self.db = dbms

        all_radio_button = tk.Radiobutton(self, text="All",indicatoron=False, height=3)
        all_radio_button.grid(row=0, column=0, sticky=tk.NSEW)

        today_radio_button = tk.Radiobutton(self, text="Today", indicatoron=False, height=4)
        today_radio_button.grid(row=0, column=1, sticky=tk.NSEW)

        pending_radio_button = tk.Radiobutton(self, text="Pending", indicatoron=False, height=3)
        pending_radio_button.grid(row=0, column=2, sticky=tk.NSEW)

        custom_date = tk.Radiobutton(self, text="Custom Date", indicatoron=False, height=3)
        custom_date.grid(row=0, column=3, sticky=tk.NSEW)
        # date_entry = DateEntry(
        #     self,
        #     date_pattern="dd-mm-yyyy",
        #     showweeknumbers=False,
        #     background="#2c3e50",
        #     foreground="white",
        #     selectbackground="#1a252f",
        #     borderwidth=0
        # )
        # date_entry.grid(row=0, column=3)

        columns = ("Date", "Time", "Details", "Customer", "Amount")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=31)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("Date", width=195, stretch=False, anchor=tk.W)
        self.tree.column("Time", width=95, stretch=False, anchor=tk.W)
        self.tree.column("Details", width=395, stretch=False, anchor=tk.W)
        self.tree.column("Customer", width=295, stretch=False, anchor=tk.W)
        self.tree.column("Amount", width=155, stretch=False, anchor=tk.W)
        self.tree.grid(row=1, column=0, columnspan=4)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)