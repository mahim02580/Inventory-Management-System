import tkinter as tk
from tkinter import ttk

class CustomersFrame(tk.Frame):
    def __init__(self, parent, dbms):
        super().__init__(parent, bg="white")
        self.db = dbms
        columns = ("Customer ID", "Customer Name", "Customer Phone", "Customer Address")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=35)
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Customer ID", width=122, stretch=False, anchor=tk.CENTER)
        self.tree.column("Customer Name", width=524, stretch=False, )
        self.tree.column("Customer Phone", width=195, stretch=False, anchor=tk.CENTER)
        self.tree.column("Customer Address", width=295, stretch=False, anchor=tk.CENTER)
        self.tree.grid(row=0, column=0)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.products_data = [
            {"id": "P001", "name": "Basin", "price": 2000, "stock": 10},
            {"id": "P002", "name": "Tiles 1'", "price": 5000, "stock": 5},
            {"id": "P003", "name": "Commode", "price": 10000, "stock": 8}
        ]
        for _ in range(20):
            for i, prod in enumerate(self.products_data):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=(prod["id"], prod["name"], prod["price"], prod["stock"]), tags=tag)

