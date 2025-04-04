import tkinter as tk
import mysql.connector
import os
import sys
from PIL import Image ,ImageTk
from datetime import datetime
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def cancel():
    root.quit()

def back():
    root.quit()

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def create_custom_size_pdf(filename):
    order_no = order_no_entry.get()
    order_date = order_date_entry.get()
    order_name = order_name_entry.get()  # Customer Name
    sr = sr_entry.get()
    product_item = product_entry.get()
    description = detail_entry.get()
    unit = unit_entry.get()
    quantity = quantity_entry.get()
    rate = rate_entry.get()
    amount = amount_entry.get()
    total_amount = amount_entry.get()  # Total amount field

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert order details into somst table
        cursor.execute("""
            INSERT INTO somst (ordno, orddt, sname, sr, item, Idesc, unit, quantity, rate, amount, Ordval)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (order_no, order_date, order_name, sr, product_item, description, unit, quantity, rate, amount, total_amount))
        
        conn.commit()

        # Fetch supplier details from supplier table
        cursor.execute("""
            SELECT Bsno, Name, Add1, Add2, City, Pincode, State, Mobileno, Email, GSTno
            FROM supplier WHERE Name = %s
        """, (order_name,))
        
        supplier_data = cursor.fetchone()
        
        if not supplier_data:
            messagebox.showerror("Error", "Supplier details not found!")
            return

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return
    finally:
        conn.close()

    # PDF Generation
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y_pos = height - 150

    try:
        c.drawImage(image_path, 50, height - 100, width=70, height=70)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Briosoft")
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width / 2, height - 70, "BRIO SOFT, PRANAM COMPLEX, AKOTA")
    c.drawCentredString(width / 2, height - 85, "VADODARA, 390017, GUJARAT, INDIA, 2147483647, brio3@gmail.com")

    # Order Details
    order_details = {
        "Order No:": order_no,
        "Order Date:": order_date,
        "Customer Name:": order_name
    }

    for label, value in order_details.items():
        c.drawString(50, y_pos, label)
        text_width = c.stringWidth(value, "Helvetica", 12)
        c.drawString(540 - text_width, y_pos, value)
        y_pos -= 20

    # Supplier Details
    supplier_labels = ["Supplier Name:", "Address Line 1:", "Address Line 2:", "City:", "Pincode:", "State:", "Mobile No:", "Email:", "GST No:"]
    for label, data in zip(supplier_labels, supplier_data[1:]):
        c.drawString(50, y_pos, label)
        text_width = c.stringWidth(str(data), "Helvetica", 12)
        c.drawString(540 - text_width, y_pos, str(data))
        y_pos -= 20

    y_pos -= 20

    headers = ["SR", "Item", "Description", "Unit", "Quantity", "Rate", "Amount"]
    x_positions = [50, 100, 250, 350, 400, 480, 540]

# Draw a line above headers
    c.line(50, y_pos, 550, y_pos)
    y_pos -= 15  # Adjust for header text

    c.setFont("Helvetica-Bold", 12)
    for x_pos, header in zip(x_positions, headers):
        c.drawString(x_pos, y_pos, header)

    y_pos -= 15
# Draw a line below headers
    c.line(50, y_pos, 550, y_pos)
    y_pos -= 20

# Order items details
    details = [sr, product_item, description, unit, quantity, rate, amount]
    c.setFont("Helvetica", 12)

    for x_pos, detail in zip(x_positions, details):
        c.drawString(x_pos, y_pos, str(detail))
    
    y_pos -= 20

# Total Amount
    total_text = f"Total Amount: {total_amount}"
    text_width = c.stringWidth(total_text, "Helvetica-Bold", 12)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(540 - text_width, y_pos, total_text)

    c.showPage()
    c.save()

    # Open the generated PDF
    try:
        os.startfile(filename)
    except AttributeError:
        os.system(f"open {filename}" if sys.platform == "darwin" else f"xdg-open {filename}")

    messagebox.showinfo("Success", f"PDF '{filename}' created and order details saved to the database!")

#def add_new_row(event=None):
    # Get the current row count (it will increment each time you add a new row)
 #   row_count = len(product_entries) + 1

    # Create new entry widgets for the next row
  #  sr_entry_new = tk.Entry(product_frame, width=5, justify="right")
   # product_item_entry_new = tk.Entry(product_frame, width=40)
    #description_entry_new = tk.Entry(product_frame, width=40)
#    unit_entry_new = tk.Entry(product_frame, width=5)
 #   quantity_entry_new = tk.Entry(product_frame, width=12, justify="right")
  #  rate_entry_new = tk.Entry(product_frame, width=12, justify="right")
   # amount_entry_new = tk.Entry(product_frame, width=12, justify="right")
    
    # Place these widgets in a new row dynamically
    #sr_entry_new.grid(row=row_count, column=0, padx=5)
#    product_item_entry_new.grid(row=row_count, column=1, padx=5)
 #   description_entry_new.grid(row=row_count, column=2, padx=5)
  #  unit_entry_new.grid(row=row_count, column=3, padx=5)
   # quantity_entry_new.grid(row=row_count, column=4, padx=5)
    #rate_entry_new.grid(row=row_count, column=5, padx=5)
#    amount_entry_new.grid(row=row_count, column=6, padx=5)

    # Store the new entry widgets in a list so we can access them later
 #   product_entries.append([sr_entry_new, product_item_entry_new, description_entry_new, 
  #                          unit_entry_new, quantity_entry_new, rate_entry_new, amount_entry_new])

    # Bind the new row quantity and rate fields to update the amount
  #  quantity_entry_new.bind("<KeyRelease>", calculate_amount)
 #   rate_entry_new.bind("<KeyRelease>", calculate_amount)


# Initialize an empty list to keep track of product rows dynamically
#product_entries = []


def calculate_amount(*args):
    """Calculate the amount (Quantity × Rate) and update the Amount field."""
    try:
        quantity = float(quantity_entry.get())
        rate = float(rate_entry.get())
        amount = quantity * rate

        # Update Amount field (read-only)
        amount_entry.config(state="normal")  # Enable editing
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, f"{amount:.2f}")
        amount_entry.config(state="readonly") 
      
    except ValueError:
        # Reset to 0.00 if input is invalid
        amount_entry.config(state="normal")
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, "0.00")
        amount_entry.config(state="readonly")

def validate_quantity(char, current_text):
    """Allow only valid floating-point numbers for Quantity."""
    if char in "0123456789.":
        # Check for multiple dots or empty text starting with '.'
        if current_text.count(".") > 1 or (char == "." and not current_text):
            return False
        return True
    return False

def validate_rate(char, current_text):
    """Allow only valid floating-point numbers for Rate."""
    if char in "0123456789.":
        # Check for multiple dots or empty text starting with '.'
        if current_text.count(".") > 1 or (char == "." and not current_text):
            return False
        return True
    return False    

# Create the main Tkinter window
root = tk.Tk()
root.title("Briosoft")
root.geometry("1600x1200")

# Title Frame with Back Button
title_frame = tk.Frame(root)
title_frame.grid(row=0, column=0, pady=10, sticky="n")

image_path = r"c:\Users\patel\OneDrive\Desktop\png\brio.jpg"

back_btn = tk.Button(root, text="Back", command=back, width=10)
back_btn.grid(row=0, column=0, pady=5, padx=5, sticky="w")

title_label1 = tk.Label(title_frame, text="Briosoft", font=("Cambria", 20, "bold"), fg="blue")
title_label1.grid(row=0, column=0, padx=10, sticky="n")

title_label2 = tk.Label(title_frame, text="BRIO SOFT, PRANAM COMPLEX, AKOTA", font=("Cambria", 10, "bold"), fg="black")
title_label2.grid(row=1, column=0, padx=10, sticky="n")

title_label3 = tk.Label(title_frame, text="VADODARA, 390017, GUJARAT, INDIA, 2147483647, brio3@gmail.com", font=("Cambria", 10, "bold"), fg="black")
title_label3.grid(row=2, column=0, padx=10, sticky="n")

# Order Details Frame
order_frame = tk.LabelFrame(root, text="", padx=10, pady=10)
order_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Center the "Sales Order" label across the frame
sales_label = tk.Label(order_frame, text="Sales Order", font=("Cambria", 15, "bold"), fg="blue")
sales_label.grid(row=0, column=0, columnspan=6, pady=10, sticky="n")

tk.Label(order_frame, text="Order No:", width=15).grid(row=3, column=0, sticky="w")
order_no_entry = tk.Entry(order_frame,justify="right")
order_no_entry.grid(row=3, column=1)

tk.Label(order_frame, text="Order Date:", width=15).grid(row=3, column=4, sticky="e")
order_date_entry = tk.Entry(order_frame)
order_date_entry.grid(row=3, column=5)
order_date = order_date_entry.get() or datetime.today().strftime('%Y-%m-%d')

tk.Label(order_frame, text="PartyName:", width=15).grid(row=5, column=0, sticky="w")
order_name_entry = tk.Entry(order_frame)
order_name_entry.grid(row=5, column=1)

# Product Details Frame
product_frame = tk.LabelFrame(root, text="", padx=10, pady=10)
product_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

tk.Label(product_frame, text="SR:", width=5).grid(row=0, column=0, padx=5)
sr_entry = tk.Entry(product_frame, width=5,justify="right")
sr_entry.grid(row=1, column=0, padx=5)

tk.Label(product_frame, text="Product Item:", width=12).grid(row=0, column=1, padx=5)
product_entry = tk.Entry(product_frame, width=40)
product_entry.grid(row=1, column=1, padx=5)

tk.Label(product_frame, text="Description:", width=8).grid(row=0, column=2, padx=5)
detail_entry = tk.Entry(product_frame, width=40)
detail_entry.grid(row=1, column=2, padx=5)

tk.Label(product_frame, text="Unit:", width=8).grid(row=0, column=3, padx=5)
unit_entry = tk.Entry(product_frame, width=5)
unit_entry.grid(row=1, column=3, padx=5)


tk.Label(product_frame, text="Quantity:", width=8).grid(row=0, column=4, padx=5)
validate_quantity_cmd = root.register(validate_quantity)
quantity_entry = tk.Entry(product_frame, width=12,justify="right")
quantity_entry.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
quantity_entry.grid(row=1, column=4, padx=5)
quantity_entry.bind("<KeyRelease>", calculate_amount)

tk.Label(product_frame, text="Rate:", width=8).grid(row=0, column=5, padx=5)
validate_rate_cmd = root.register(validate_quantity)
rate_entry = tk.Entry(product_frame, width=12,justify="right")
rate_entry.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
rate_entry.grid(row=1, column=5, padx=5)
rate_entry.bind("<KeyRelease>", calculate_amount)


tk.Label(product_frame, text="Amount:", width=8).grid(row=0, column=6, padx=5)
amount_entry = tk.Entry(product_frame, width=12,justify="right")
amount_entry.grid(row=1, column=6, padx=5)
amount_entry.config(state="readonly")

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, pady=20)

tk.Button(button_frame, text=" PDF", command=lambda: create_custom_size_pdf("Billing_Report.pdf")).pack(side="left", padx=10)
tk.Button(button_frame, text="Cancel", command=cancel).pack(side="left", padx=10)

# Add the initial row (row 1)
#add_new_row()

# Bind the Enter key to add a new row
#root.bind("<Return>", add_new_row)

root.mainloop()

