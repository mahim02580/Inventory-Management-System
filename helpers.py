import win32print
import win32ui


def make_invoice_for_purchase(purchase):
    invoice = f"""
========================================
            M RAHMAN CERAMIC
          Purbadhala, Netrakona
           Contact: 0170000000
              Sales Invoice
========================================
Invoice No          :      {purchase.id}
Date                :    {purchase.date}
Time                :    {purchase.time}   
----------------------------------------
Item           Unit Price  Qty  Subtotal
{purchase.details}
----------------------------------------
           MRP Total:{purchase.mrp_total}
        (-) Discount:{purchase.discount}
                     -------------------
       Total Payable:{purchase.total_payable}
                Paid:{purchase.total_paid_amount}
                     -------------------
              Change:{purchase.change_amount}
                 Due:{purchase.due_amount}
----------------------------------------

Customer ID: {purchase.customer.id}
Name: {purchase.customer.name}
Phone: {purchase.customer.phone}
Address: {purchase.customer.address}

  Thank you for your purchase!
"""
    print(invoice)
    return invoice


def print_out_invoice(invoice: str):
    printer_name = win32print.GetDefaultPrinter()

    hprinter = win32print.OpenPrinter(printer_name)
    printer_info = win32print.GetPrinter(hprinter, 2)

    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)

    # ---- SET FONT ----
    font = win32ui.CreateFont({
        "name": "Courier New",
        "height": 20,
        "weight": 4000
    })
    hdc.SelectObject(font)

    # ---- START PRINT ----
    hdc.StartDoc("Invoice")
    hdc.StartPage()

    x = 10
    y = 10
    line_height = 24

    for line in invoice.split("\n"):
        hdc.TextOut(x, y, line[:32])
        y += line_height

    hdc.EndPage()
    hdc.EndDoc()

    # ---- CLEANUP ----
    hdc.DeleteDC()
    win32print.ClosePrinter(hprinter)

