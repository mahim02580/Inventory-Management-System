import tkinter as tk
from tkinter import ttk


class RefundFrame:
    def __init__(self, parent, invoice, dbmanager):
        self.parent = parent
        self.invoice = invoice
        self.dbmanager = dbmanager
        product_selection_frame = tk.Frame(parent)
        product_selection_frame.grid(row=0, column=0)

        columns = ("PID", "Product Name", "Unit Price", "Sold Qty", "Returned Qty", "Refund")
        product_entry_treeviewview_style = ttk.Style(product_selection_frame)
        product_entry_treeviewview_style.configure("Treeview",
                                                   font=("Segoe UI", 12),
                                                   rowheight=30,
                                                   borderwidth=0,
                                                   highlightthickness=0)
        product_entry_treeviewview_style.configure("Treeview.Heading",
                                                   background="#e0e0e0",
                                                   foreground="black",
                                                   font=("Segoe UI", 12, "bold"))

        self.menu = tk.Menu(product_selection_frame, tearoff=0)
        self.menu.add_command(label="Delete")

        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=10,
                                                   style="Treeview")
        self.product_entry_treeview.bind("<Double-1>", self.edit_cell)
        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)
        self.product_entry_treeview.column("PID", width=70, stretch=False, )
        self.product_entry_treeview.column("Product Name", width=424, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=100, stretch=False, )
        self.product_entry_treeview.column("Sold Qty", width=100, stretch=False, )
        self.product_entry_treeview.column("Returned Qty", width=130, stretch=False, )
        self.product_entry_treeview.column("Refund", width=100, stretch=False, )

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        total_items_frame = tk.Frame(product_selection_frame)
        total_items_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        tk.Label(total_items_frame, text="Total Returned Items:", font=("Arial", 16, "bold"), ).grid(row=2, column=0,
                                                                                                     sticky=tk.W)
        tk.Label(total_items_frame, text="000", font=("Arial", 16, "bold"), ).grid(row=2, column=1, sticky=tk.W)

        total_items_frame = tk.Frame(product_selection_frame)
        total_items_frame.grid(row=2, column=2, columnspan=3, sticky=tk.E)
        tk.Label(total_items_frame, text="Total Refund Amount:", font=("Arial", 16, "bold"), ).grid(row=2, column=0,
                                                                                                    sticky=tk.W)
        tk.Label(total_items_frame, text="000", font=("Arial", 16, "bold"), ).grid(row=2, column=1, sticky=tk.W)

        ttk.Button(product_selection_frame, text="Confirm", command=self.adjust_stocks_for_returned_products).grid(
            row=3, column=4, pady=(40, 0), sticky=tk.E)
        self.load_products()

    def load_products(self):
        for item in self.invoice.items:
            self.product_entry_treeview.insert("", tk.END,
                                               values=(item.product_id, item.product_name, item.unit_price,
                                                       item.quantity, 0, 0))

    def edit_cell(self, event):
        # Detect row and column
        region = self.product_entry_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.product_entry_treeview.identify_row(event.y)
        column = self.product_entry_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1

        if not col_index == 4:
            return

        x, y, width, height = self.product_entry_treeview.bbox(row_id, column)

        # Current value
        value = self.product_entry_treeview.item(row_id)["values"][col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.product_entry_treeview, font=("Segoe UI", 12))
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event=None):
            new_val = entry.get()
            values = list(self.product_entry_treeview.item(row_id, "values"))

            values[col_index] = new_val  # Implements Changes

            # Update Product in the TreeView
            self.product_entry_treeview.item(row_id, values=values)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def adjust_stocks_for_returned_products(self):
        for row_id in self.product_entry_treeview.get_children():
            values = self.product_entry_treeview.item(row_id, "values")

            # Update product stock in the database
            product_name, product_quantity = values[1], values[4]
            self.dbmanager.update_stock_of_product(product_name, product_quantity)
        self.parent.destroy()
