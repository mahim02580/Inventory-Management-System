import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ProductsFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent, bg="white")
        self.configure(padx=20, pady=20)
        self.dbmanager = dbmanager

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_item)
        # Products Treeview---------------------------------------------------------------------------------------------
        columns = ("Product ID", "Product Name", "Unit Price", "Stock")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=24)
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("Product ID", width=115, stretch=False, anchor=tk.CENTER)
        self.tree.column("Product Name", width=520, stretch=False)
        self.tree.column("Unit Price", width=95, stretch=False)
        self.tree.column("Stock", width=95, stretch=False)
        self.tree.grid(row=0, column=0)
        self.tree.bind("<Button-3>", self.show_menu)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.tag_configure("evenrow", background="#f0f0f0")
        self.tree.tag_configure("oddrow", background="#FFFFFF")

        self.tree.bind("<Double-1>", self.edit_cell)
        # Right Side Frame----------------------------------------------------------------------------------------------
        right_side_frame = tk.Frame(self)
        right_side_frame.grid(row=0, column=2, sticky=tk.NSEW)

        ## Stock Entry
        stock_entry_frame = tk.Frame(right_side_frame, highlightbackground="#2c3e50", highlightthickness=2)
        stock_entry_frame.grid(row=0, column=0, padx=20, sticky=tk.N)

        tk.Label(stock_entry_frame,
                 text="Update New Stock",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18), ).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(stock_entry_frame,
                 text="Select Product",
                 fg="white",
                 bg="#2c3e50",
                 width=25,
                 font=("Segoe UI", 12)).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.product_to_update_stock = ttk.Combobox(stock_entry_frame, font=("Arial", 12))
        self.product_to_update_stock.grid(row=2, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        tk.Label(stock_entry_frame,
                 text="New Stock",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.product_new_stock_entry = tk.Entry(stock_entry_frame, font=("Segoe UI", 12))
        self.product_new_stock_entry.grid(row=4, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        ttk.Button(stock_entry_frame,
                   text="Update",
                   command=self.update_stock).grid(row=5, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)

        ## New Product Entry
        product_entry_frame = tk.Frame(right_side_frame, highlightbackground="#2c3e50", highlightthickness=2)
        product_entry_frame.grid(row=1, column=0, padx=20, pady=20, sticky=tk.N)

        tk.Label(product_entry_frame,
                 text="Add New Product",
                 fg="white",
                 bg="#2c3e50",
                 width=19,
                 font=("Segoe UI", 18)).grid(row=0, column=0, pady=(0, 20), sticky=tk.NSEW)

        tk.Label(product_entry_frame,
                 text="Product Name (with Model)",
                 bg="#2c3e50",
                 width=25,
                 fg="white", font=("Segoe UI", 12), ).grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.product_name_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12))
        self.product_name_entry.grid(row=2, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Unit Price",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12)).grid(row=3, column=0, padx=5, sticky=tk.NSEW)
        self.product_unit_price_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12), )
        self.product_unit_price_entry.grid(row=4, column=0, pady=(0, 10), padx=5, sticky=tk.EW)

        tk.Label(product_entry_frame,
                 text="Product Stock",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=5, column=0, padx=5, sticky=tk.NSEW)
        self.product_stock_entry = tk.Entry(product_entry_frame, font=("Segoe UI", 12))
        self.product_stock_entry.grid(row=6, column=0, padx=5, pady=(0, 10), sticky=tk.EW)

        ttk.Button(product_entry_frame,
                   text="Add",
                   command=self.add_product).grid(row=7, column=0, padx=5, pady=(0, 10), sticky=tk.NSEW)
        self.refresh()

    def edit_cell(self, event):
        # Detect row and column
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1

        if col_index == 0:
            return

        x, y, width, height = self.tree.bbox(row_id, column)

        # Current value
        value = self.tree.item(row_id)["values"][col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.tree, font=("Segoe UI", 12))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event=None):
            column_map = {
                0: "id",
                1: "name",
                2: "unit_price",
                3: "stock",
            }

            new_val = entry.get()
            values = list(self.tree.item(row_id)["values"])

            values[col_index] = new_val  # Implements Changes

            # Update product in the database
            self.dbmanager.update_product(product_id=values[0], changed_column=column_map[col_index], new_value=new_val)

            # Update Product in the TreeView
            self.tree.item(row_id, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            product_id_to_delete = self.tree.item(item, "values")[0]
            self.dbmanager.delete_product(product_id_to_delete)
            self.tree.delete(item)

    def show_menu(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def add_product(self):
        product_name = self.product_name_entry.get()
        product_unit_price = self.product_unit_price_entry.get()
        product_stock = self.product_stock_entry.get()
        if not all([product_name, product_unit_price, product_stock]):
            messagebox.showerror(
                title="Missing Information",
                message="Product Name, Unit Price, and Stock must all be filled in."
            )
        else:
            product_to_add = self.dbmanager.Product(name=product_name,
                                                    unit_price=product_unit_price,
                                                    stock=product_stock)
            self.dbmanager.add_product(product_to_add)
            self.refresh()

    def update_stock(self):
        product_name_to_update_stock = self.product_to_update_stock.get()
        new_stock = self.product_new_stock_entry.get()
        if not new_stock:
            messagebox.showerror(
                title="Missing Information",
                message="New Stock must be filled in."
            )
        else:
            self.dbmanager.update_stock_of_product(product_name_to_update_stock, new_stock)
            self.refresh()

    def refresh(self):
        # Clears Products Treeview
        self.tree.delete(*self.tree.get_children())

        # Gets all products(updated)
        for i, product in enumerate(self.dbmanager.get_all_products()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END,
                             values=(product.id, product.name, product.unit_price, product.stock), tags=tag)

        # Gets all products name(updated)
        self.product_to_update_stock.config(values=self.dbmanager.get_all_products_name())
        try:
            self.product_to_update_stock.current(0)
        except tk.TclError:
            pass

        # Clears all entries
        self.product_new_stock_entry.delete(0, tk.END) # from Update New Stock

        self.product_name_entry.delete(0, tk.END)
        self.product_unit_price_entry.delete(0, tk.END)
        self.product_stock_entry.delete(0, tk.END)

