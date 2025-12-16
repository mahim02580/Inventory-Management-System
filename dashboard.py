import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from datetime import datetime
import helpers

SHOP_NAME = "M Rahman\nCeramic"


class DashboardFrame(tk.Frame):
    def __init__(self, parent, dbmanager):
        super().__init__(parent, bg="#f5f5f5")
        self.configure(padx=20, pady=20)
        self.parent = parent
        self.dbmanager = dbmanager

        # Sales Today + Revenue Today + Total Due-----------------------------------------------------------------------
        self.sales_today = tk.IntVar(value=0)
        self.revenue_today = tk.IntVar(value=0)
        self.total_due = tk.IntVar(value=0)

        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, sticky=tk.W)
        tk.Label(top_frame,
                 text="Sales Today",
                 bg="#3498db",
                 fg="white",
                 width=18,
                 height=2,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=0)
        tk.Label(top_frame,
                 textvariable=self.sales_today,
                 bg="#3498db",
                 fg="white",
                 width=18,
                 height=1,
                 font=("Arial", 18, "bold"),
                 ).grid(row=1, column=0)

        tk.Label(top_frame,
                 text=f"Revenue Today",
                 bg="#1abc9c",
                 fg="white",
                 width=18,
                 height=2,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=1, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#1abc9c",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=1, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.revenue_today,
                 bg="#1abc9c",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=2, sticky=tk.NSEW)

        tk.Label(top_frame,
                 text=f"Total Due",
                 bg="#9b59b6",
                 fg="white",
                 width=18,
                 height=2,
                 font=("Arial", 18, "bold"),
                 ).grid(row=0, column=3, columnspan=2)
        tk.Label(top_frame,
                 text="৳",
                 bg="#9b59b6",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.E,
                 ).grid(row=1, column=3, sticky=tk.NSEW)
        tk.Label(top_frame,
                 textvariable=self.total_due,
                 bg="#9b59b6",
                 fg="white",
                 font=("Arial", 18, "bold"),
                 anchor=tk.W,
                 ).grid(row=1, column=4, sticky=tk.NSEW)

        # Product Selection Frame--------------------------------------------------------------------------------------------
        ## Upper Part
        product_selection_frame = tk.Frame(self, pady=20)
        product_selection_frame.grid(row=1, column=0)

        tk.Label(product_selection_frame,
                 text="Select Product:",
                 font=("Arial", 15),
                 bg="#f5f5f5").grid(row=0, column=0, sticky=tk.W)

        self.product_name_combobox = ttk.Combobox(product_selection_frame, width=35, font=("Arial", 15))
        self.product_name_combobox.grid(row=0, column=1)

        tk.Label(product_selection_frame,
                 text="Quantity:",
                 font=Font(size=15),
                 bg="#f5f5f5").grid(row=0, column=2)

        self.quantity = tk.Spinbox(product_selection_frame, from_=1, to=100000, font=("Arial", 15), width=7)
        self.quantity.grid(row=0, column=3)

        ttk.Button(product_selection_frame, text="Add", command=self.add_product_to_bill).grid(row=0, column=4)

        ## Lower Part
        columns = ("Product ID", "Product Name", "Unit Price", "Quantity", "Subtotal")
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
        self.menu.add_command(label="Delete", command=self.delete_item)

        self.product_entry_treeview = ttk.Treeview(product_selection_frame,
                                                   columns=columns,
                                                   show="headings",
                                                   height=15,
                                                   style="Treeview")
        self.product_entry_treeview.bind("<Button-3>", self.show_menu)
        self.product_entry_treeview.tag_configure("product_entry_row", background="#f0f0f0")

        for col in columns:
            self.product_entry_treeview.heading(col, text=col)

        self.product_entry_treeview.column("Product ID", width=115, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Product Name", width=424, stretch=False, )
        self.product_entry_treeview.column("Unit Price", width=95, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Quantity", width=95, stretch=False, anchor=tk.CENTER)
        self.product_entry_treeview.column("Subtotal", width=95, stretch=False, anchor=tk.CENTER)

        self.product_entry_treeview.grid(row=1, column=0, columnspan=5, pady=20)

        scrollbar = ttk.Scrollbar(product_selection_frame, orient=tk.VERTICAL,
                                  command=self.product_entry_treeview.yview)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=20)
        self.product_entry_treeview.configure(yscrollcommand=scrollbar.set)

        # Logo Frame----------------------------------------------------------------------------------------------------
        logo_frame = tk.Frame(self, bg="black")
        logo_frame.configure(borderwidth=2)
        logo_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=(20, 0))

        tk.Label(logo_frame,
                 text=SHOP_NAME,
                 font=("Arial Black", 23, "bold"),
                 padx=36).grid(row=0, column=0, sticky=tk.NSEW)

        # Invoice Making Frame--------------------------------------------------------------------------------------------
        invoice_frame = tk.Frame(self)
        invoice_frame.grid(row=1, column=1, sticky=tk.N, padx=(20, 0), pady=(20, 0))

        tk.Label(invoice_frame,
                 text="Total Items",
                 font=("Arial", 16, "bold"),
                 bg="#f5f5f5",
                 anchor=tk.W
                 ).grid(row=0, column=0, sticky=tk.W)
        tk.Label(invoice_frame,
                 text=":",
                 font=("Arial", 16, "bold"),
                 bg="#f5f5f5",
                 anchor=tk.W
                 ).grid(row=0, column=1)
        self.total_items = tk.IntVar(value=0)

        tk.Label(invoice_frame,
                 textvariable=self.total_items,
                 fg="white",
                 bg="black",
                 font=("Arial", 16, "bold"),
                 anchor=tk.E, ).grid(row=0, column=2, sticky=tk.NSEW)

        self.mrp_total = tk.IntVar(value=0)
        self.total = tk.IntVar(value=0)

        # MRP Total
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=1, column=0, columnspan=3, pady=(20, 0),
                                                               sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="MRP Total",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=2, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=2, column=1, sticky=tk.NSEW)

        tk.Label(invoice_frame,
                 textvariable=self.mrp_total,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=2, column=2, sticky=tk.NSEW)

        # (-) Discount
        tk.Label(invoice_frame,
                 text="(-) Discount)",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W).grid(row=3, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 ).grid(row=3, column=1, sticky=tk.NSEW)

        self.discount_entry = tk.Entry(invoice_frame,
                                       width=6,
                                       highlightbackground="#2c3e50",
                                       highlightthickness=1,
                                       highlightcolor="#2c3e50",
                                       font=("Segoe UI", 12),
                                       justify=tk.RIGHT, )

        self.discount_entry.insert(tk.END, "0")
        self.discount_entry.grid(row=3, column=2, sticky=tk.EW)

        # Total Payable
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=4, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="Total Payable",
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.W,
                 fg="white").grid(row=5, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=5, column=1, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 textvariable=self.total,
                 bg="#2c3e50",
                 font=("Segoe UI", 12, "bold"),
                 anchor=tk.E,
                 fg="white").grid(row=5, column=2, sticky=tk.NSEW)

        self.payment_methods_treeview = ttk.Treeview(invoice_frame,
                                                     columns=("Payment Method", "Amount"),
                                                     show="headings",
                                                     height=1)
        data = [("Cash Received", 0), ("Bkash", 0), ("Nagad", 0), ("Card/Bank", 0)]
        for item in data:
            self.payment_methods_treeview.insert("", tk.END, values=item)
        self.payment_methods_treeview.grid(row=6, column=0, columnspan=3)
        self.payment_methods_treeview.bind("<Double-1>", self.edit_cell)

        # It has to be here because of self.update_total method.
        # In self.update_total method there is another method called self.calculate_change_due(called inside of self.update_total).
        # In self.calculate change due we referred self.payment_methods_treeview
        self.discount_entry.config(validate="key", validatecommand=(invoice_frame.register(self.update_total), "%P"))

        self.payment_methods_treeview.column("Payment Method", width=158, stretch=tk.NO)
        self.payment_methods_treeview.column("Amount", width=96, stretch=tk.NO, anchor=tk.E)
        self.payment_methods_treeview.heading("Payment Method", text="Payment Type")
        self.payment_methods_treeview.heading("Amount", text="Amount")
        # Total Paid + Change + Due-------------------------------------------------------------------------------------

        ## Total Paid
        ttk.Separator(invoice_frame, orient="horizontal").grid(row=7, column=0, columnspan=3, sticky=tk.EW)
        tk.Label(invoice_frame,
                 text="Paid",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W,
                 fg="white").grid(row=8, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 fg="white").grid(row=8, column=1, sticky=tk.NSEW)
        self.total_paid_amount = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.total_paid_amount,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E, ).grid(row=8, column=2, sticky=tk.NSEW)

        ## Change
        tk.Label(invoice_frame,
                 text="Change",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W).grid(row=9, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=9, column=1, sticky=tk.NSEW)
        self.change_amount = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.change_amount,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=9, column=2, sticky=tk.NSEW)

        ## Due
        tk.Label(invoice_frame,
                 text="Due",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.W, ).grid(row=10, column=0, sticky=tk.NSEW)
        tk.Label(invoice_frame,
                 text=":",
                 bg="#2c3e50", font=("Segoe UI", 12),
                 fg="white").grid(
            row=10, column=1, sticky=tk.NSEW)
        self.due_amount = tk.IntVar(value=0)
        tk.Label(invoice_frame,
                 textvariable=self.due_amount,
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12),
                 anchor=tk.E).grid(row=10, column=2, sticky=tk.NSEW)

        # Customer Details Frame
        customer_details_frame = tk.Frame(invoice_frame)
        customer_details_frame.grid(row=11, column=0, columnspan=3, pady=20, sticky=tk.NSEW)

        tk.Label(customer_details_frame,
                 text="Customer Phone",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12), ).grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.customer_phone_entry = tk.Entry(customer_details_frame, font=("Segoe UI", 12))
        self.customer_phone_entry.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        ttk.Button(customer_details_frame,
                   text="Search",
                   width=7,
                   command=self.search_customer).grid(row=0, column=2, rowspan=2, padx=(15, 0), sticky=tk.NS)

        tk.Label(customer_details_frame,
                 text="Customer Name",
                 bg="#2c3e50",
                 fg="white",
                 font=("Segoe UI", 12), ).grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=tk.NSEW)
        self.customer_name_entry = tk.Entry(customer_details_frame, font=("Segoe UI", 12))
        self.customer_name_entry.grid(row=3, column=0, columnspan=3, sticky=tk.EW)

        tk.Label(customer_details_frame,
                 text="Customer Address",
                 fg="white",
                 bg="#2c3e50",
                 font=("Segoe UI", 12)).grid(row=4, column=0, columnspan=3, pady=(10, 0), sticky=tk.NSEW)
        self.customer_address_entry = tk.Text(customer_details_frame, height=2, width=20, font=("Segoe UI", 12))
        self.customer_address_entry.grid(row=5, column=0, columnspan=3, sticky=tk.EW)

        ttk.Button(customer_details_frame,
                   text="PRINT",
                   command=self.print_invoice).grid(row=6, column=0, columnspan=3, pady=(30, 0), sticky=tk.EW)

        self.refresh()

    def delete_item(self, items=None):
        selected = items or self.product_entry_treeview.selection()
        if not selected:
            return

        for item in selected:
            self.product_entry_treeview.delete(item)

        self.total_items.set(len(self.product_entry_treeview.get_children()))
        self.mrp_total.set(sum(int(self.product_entry_treeview.item(item, "values")[4]) for item in
                               self.product_entry_treeview.get_children()))
        self.update_total(self.discount_entry.get())

    def show_menu(self, event):
        iid = self.product_entry_treeview.identify_row(event.y)
        if iid:
            self.product_entry_treeview.selection_set(iid)
            self.menu.tk_popup(event.x_root, event.y_root)

    def edit_cell(self, event):
        # Detect row and column
        region = self.payment_methods_treeview.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = self.payment_methods_treeview.identify_row(event.y)
        column = self.payment_methods_treeview.identify_column(event.x)

        # Column index
        col_index = int(column.replace("#", "")) - 1
        if col_index == 0:
            return
        x, y, width, height = self.payment_methods_treeview.bbox(row_id, column)

        # Current value
        value = self.payment_methods_treeview.item(row_id)["values"][col_index]

        # Overlay Entry widget
        entry = tk.Entry(self.payment_methods_treeview, font=("Segoe UI", 12), justify=tk.RIGHT)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event=None):
            new_val = entry.get()
            values = list(self.payment_methods_treeview.item(row_id)["values"])
            values[col_index] = new_val
            self.payment_methods_treeview.item(row_id, values=values)
            self.calculate_change_due()
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def add_product_to_bill(self):
        product_to_add = self.product_name_combobox.get()
        quantity = self.quantity.get()
        product = self.dbmanager.get_product_by_name(product_to_add)
        subtotal = int(product.unit_price) * int(quantity)

        self.product_entry_treeview.insert("", tk.END,
                                           values=(product.id, product.name, product.unit_price, quantity, subtotal),
                                           tags="product_entry_row")

        self.total_items.set(len(self.product_entry_treeview.get_children()))
        self.mrp_total.set(sum(int(self.product_entry_treeview.item(item, "values")[4]) for item in
                               self.product_entry_treeview.get_children()))
        self.update_total(self.discount_entry.get())

    def update_total(self, new_value):
        if new_value == "":
            new_value = "0"

        if not new_value.isdigit():
            return False  # block anything that's not a number

        discount = int(new_value)

        self.total.set(self.mrp_total.get() - discount)
        self.calculate_change_due()
        return True

    def calculate_change_due(self):
        total_amount_has_given = sum(int(self.payment_methods_treeview.item(item, "values")[1])
                                     for item in self.payment_methods_treeview.get_children())
        self.total_paid_amount.set(total_amount_has_given)
        if self.total.get() < self.total_paid_amount.get():
            self.change_amount.set(total_amount_has_given - self.total.get())
            self.due_amount.set(0)
        else:
            self.due_amount.set(self.total.get() - self.total_paid_amount.get())
            self.change_amount.set(0)

    def search_customer(self):
        customer_phone = self.customer_phone_entry.get()
        if customer_phone:
            customer = self.dbmanager.get_customer_by_phone(customer_phone)
            if customer:
                self.customer_phone_entry.config(bg="green")

                self.customer_name_entry.delete(0, tk.END)
                self.customer_name_entry.insert(tk.END, customer.name)

                self.customer_address_entry.delete("1.0", tk.END)
                self.customer_address_entry.insert(tk.END, customer.address)
            else:
                self.customer_phone_entry.config(bg="red")
                self.customer_name_entry.delete(0, tk.END)
                self.customer_address_entry.delete("1.0", tk.END)

    def refresh(self):
        # Updates amounts in Dashboard
        today_sales = self.dbmanager.get_today_sales()
        all_sales = self.dbmanager.get_all_sales()
        self.sales_today.set(len(today_sales))
        self.revenue_today.set(sum([sale.total_payable for sale in today_sales]))
        self.total_due.set(sum([sale.due_amount for sale in all_sales]))

        # Resets Product Name List
        self.product_name_combobox.config(values=self.dbmanager.get_all_products_name())
        try:
            self.product_name_combobox.current(0)
        except tk.TclError:
            pass

        # Deletes all item in the Product Entry Treeview
        self.delete_item(self.product_entry_treeview.get_children())

        # Resets Payment Methods Treeview Amounts
        for row_id in self.payment_methods_treeview.get_children():
            values = list(self.payment_methods_treeview.item(row_id, "values"))
            values[1] = "0"
            self.payment_methods_treeview.item(row_id, values=values)

        # Clears all entries
        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, "0")
        self.customer_phone_entry.config(bg="white")
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.customer_address_entry.delete("1.0", tk.END)



    def print_invoice(self):
        current_customer_phone = self.customer_phone_entry.get()
        if current_customer_phone:
            current_customer = self.dbmanager.get_customer_by_phone(current_customer_phone)
            if not current_customer:
                current_customer = self.dbmanager.Customer(
                    name=self.customer_name_entry.get(),
                    phone=self.customer_phone_entry.get(),
                    address=self.customer_address_entry.get("1.0", tk.END),
                )
                current_customer = self.dbmanager.add_customer(current_customer)
        else:
            current_customer = self.dbmanager.get_customer_by_phone("017XXXXXXXXX")

        # Adds product to invoice
        purchased_products = ""
        for row in self.product_entry_treeview.get_children():
            product_id, item, unit_price, quantity, subtotal = self.product_entry_treeview.item(row)["values"]
            # Format spacing (important for alignment)
            purchased_products += f"{item[:14]:<14}{unit_price:>5} {quantity:>6} {subtotal:>7}\n"

            # Adjusts stock while looping over through the TreeView
            self.dbmanager.adjust_stock_of_product(product_id, quantity)

        purchase = self.dbmanager.Purchase(
            date=datetime.now().strftime("%d-%m-%Y"),
            time=datetime.now().strftime("%I:%M %p"),
            details=purchased_products,
            customer_id=current_customer.id,
            mrp_total=self.mrp_total.get(),
            discount=self.discount_entry.get(),
            total_payable=self.total.get(),
            total_paid_amount=self.total_paid_amount.get(),
            change_amount=self.change_amount.get(),
            due_amount=self.due_amount.get(),
        )
        purchase = self.dbmanager.add_purchase(purchase)
        invoice = helpers.make_invoice_for_purchase(purchase)
        helpers.print_out_invoice(invoice)
        self.refresh()
