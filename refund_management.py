import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from dashboard import DashboardFrame


class RefundFrame(DashboardFrame):
    def __init__(self, parent, invoice):
        self.invoice = invoice

        product_selection_frame = tk.Frame(parent)
        product_selection_frame.grid(row=0, column=0)

        tk.Label(product_selection_frame,
                 text="Returned Product:",
                 font=("Arial", 15),
                 bg="#f5f5f5").grid(row=0, column=0, sticky=tk.W)

        self.product_name_combobox = ttk.Combobox(product_selection_frame, width=35, font=("Arial", 15))
        self.product_name_combobox.grid(row=0, column=1)

        tk.Label(product_selection_frame,
                 text="Returned Quantity:",
                 font=Font(size=15),
                 bg="#f5f5f5").grid(row=0, column=2)

        self.quantity = tk.Spinbox(product_selection_frame, from_=1, to=100000, font=("Arial", 15), width=7)
        self.quantity.grid(row=0, column=3)

        ttk.Button(product_selection_frame, text="Add", command=self.add_product_to_bill).grid(row=0, column=4)

        ## Lower Part
        columns = ("Product Name", "Unit Price", "Sold Qty", "Returned Qty", "Refund")
        treeview_style = ttk.Style(product_selection_frame)
        treeview_style.configure("Treeview",
                                 font=("Segoe UI", 12),
                                 rowheight=30,
                                 borderwidth=0,
                                 highlightthickness=0)
        treeview_style.configure("Treeview.Heading",
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
        self.product_entry_treeview.bind("<Button-3>", self.show_menu)
        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)

        self.product_entry_treeview.column("Product Name", width=424, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=130, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Sold Qty", width=130, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Returned Qty", width=130, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Refund", width=130, stretch=False, anchor=tk.CENTER)

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

        ttk.Button(product_selection_frame, text="Confirm").grid(row=3, column=4, pady=(40, 0), sticky=tk.E)
        self.load_invoice()

    def load_invoice(self):
        product_details = self.invoice.details.splitlines()
        for product_detail in product_details:
            product = product_detail.split("  ")
            product_name = product_detail.split("  ")[0]
            product_unit_price = product_detail.split("  ")[1]
            product_unit_price = product_detail.split("  ")[2]
            print(product)
