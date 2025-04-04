import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import json
import sys

# Read sales data from the temporary JSON file (if editing)
if len(sys.argv) > 1:
    temp_file = sys.argv[1]
    with open(temp_file, "r") as f:
        sales_data = json.load(f)
else:
    sales_data = {}

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="briodata"
    )

# Fetch supplier names from database
def fetch_suppliers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Supplier")  # Ensure 'Name' is correct
    suppliers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return suppliers

# Fetch product items from database
def fetch_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Item FROM Item")  # Ensure 'Item' is correct
    products = [row[0] for row in cursor.fetchall()]
    conn.close()
    return products

# Fetch product details when a product is selected
def on_product_select(event):
    selected_product = productitem_combobox.get()
    product_details = fetch_product_details(selected_product)
    if product_details:
        entry_detail.delete(0, tk.END)
        entry_detail.insert(0, product_details["description"])
        entry_unit.delete(0, tk.END)
        entry_unit.insert(0, product_details["unit"])
        entry_rate.delete(0, tk.END)
        entry_rate.insert(0, f"{product_details['rate']:.2f}")

# Fetch product details from database
def fetch_product_details(product_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Idesc, Unit, Rate FROM Item WHERE Item = %s", (product_name,))
    product_details = cursor.fetchone()
    conn.close()
    
    if product_details:
        return {"description": product_details[0], "unit": product_details[1], "rate": product_details[2]}
    return None

# Save order to database
def save():
    Orderno = entry_orderno.get()
    Orderdate = entry_orderdate.get()
    supplier = supplier_combobox.get()
    sr = entry_sr.get()
    productitem = productitem_combobox.get()
    detail = entry_detail.get()
    unit = entry_unit.get()
    quantity = entry_quantity.get()
    rate = entry_rate.get()
    amount = entry_amount.get()
    totalvalue = entry_totalvalue.get()

    # Validate mandatory fields
    if not all([Orderno,Orderdate, supplier,sr,productitem, detail, unit,quantity, rate,amount,totalvalue]):
        messagebox.showerror("Error", "All fields are required!")


    conn = connect_db()
    cursor = conn.cursor()

    # Fetch count of Bsno
    cursor.execute("SELECT COUNT(Bsno) as stot_rows FROM somst")
    result = cursor.fetchone()
    
    total_rows = result[0]

    #If total count is 0, set it to 1, otherwise increment by 1
    if total_rows == 0:
        total_rows = 1
    else:
        total_rows += 1 


    sql = """
       INSERT INTO somst (Bsno, Ordno, Orddt, Sname, Sr, Item, Idesc, Unit, Quantity, Rate, Amount, Ordval) 
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
       ON DUPLICATE KEY UPDATE 
       Bsno=VALUES(Bsno), 
        
       Orddt=VALUES(Orddt),
       Sname=VALUES(Sname),
       Sr=VALUES(Sr),
       Item=VALUES(Item),
       Idesc=VALUES(Idesc),
       Unit=VALUES(Unit),
       Quantity=VALUES(Quantity),
       Rate=VALUES(Rate),
       Amount=VALUES(Amount),
       Ordval=VALUES(Ordval)
    """
    orderdate = datetime.strptime(entry_orderdate.get(), "%d-%m-%Y").date()  # Convert to datetime.date
    values = (total_rows, entry_orderno.get(),orderdate,supplier_combobox.get(), entry_sr.get(), productitem_combobox.get(), entry_detail.get(), entry_unit.get(), entry_quantity.get(), entry_rate.get(), entry_amount.get(), entry_totalvalue.get())

    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Sales order saved successfully!")
    root.quit()

def calculate_amount(*args):
    """Calculate the amount (Quantity × Rate) and update the Amount field."""
    try:
        quantity = float(entry_quantity.get())
        rate = float(entry_rate.get())
        amount = quantity * rate

        # Update Amount field (read-only)
        entry_amount.config(state="normal")  # Enable editing
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, f"{amount:.2f}")
        entry_amount.config(state="readonly") 

        # Update Total Order Value (read-only)
        entry_totalvalue.config(state="normal")
        entry_totalvalue.delete(0, tk.END)
        entry_totalvalue.insert(0, f"{amount:.2f}")  # Same as Amount
        entry_totalvalue.config(state="readonly")
    except ValueError:
        # Reset to 0.00 if input is invalid
        entry_amount.config(state="normal")
        entry_amount.delete(0, tk.END)
        entry_amount.insert(0, "0.00")
        entry_amount.config(state="readonly")

        entry_totalvalue.config(state="normal")
        entry_totalvalue.delete(0, tk.END)
        entry_totalvalue.insert(0, "0.00")
        entry_totalvalue.config(state="readonly")

def validate_unit_input(char, current_text):
    """Allow only alphabetic characters (A-Z, a-z) and max 3 characters."""
    if not char.isalpha():  # Ensure only alphabetic characters
        return False
    if len(current_text) >= 4:  # Restrict to max 3 characters
        return False
    return True

def validate_numeric_input(char, current_text):
    """Allow only numeric input (with optional decimal)."""
    if char.isdigit() or (char == "." and "." not in current_text):
        return True
    return False

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


def back():
    root.quit()  # This could be changed to navigate back to another window

# Create the main window
root = tk.Tk()
root.title("Sales Order")
root.geometry("1600x1200")

# Configure grid weights for centering
for i in range(20):  # Adjust the range based on the number of rows
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

#validate_quantity_cmd = root.register(validate_quantity)
#validate_rate_cmd = root.register(validate_rate)
vcmd_numeric = root.register(validate_numeric_input)
# Title Frame with Back Button
title_frame = tk.Frame(root)
title_frame.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")

# Add the Back button to the first row, last column
back_btn = tk.Button(root, text="Back", command=back, width=10, fg="black")
back_btn.grid(row=0, column=0, pady=5, padx=5, sticky="w")
root.bind("<Alt-b>", lambda event: back())  # Alt + b shortcut

# Title Label
title_label = tk.Label(title_frame, text="Sales Order", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="left", padx=10)

# Labels & Entry Fields
labels = [("Order No",True),( "Order Date" ,True),( "Supplier", True), ("Sr",True),( "Product Item",True),( "Description",True),( "Unit",True), 
          ("Quantity",True),( "Rate",True), ("Amount",True), ("Total Order Value",True)]

entry_orderno = tk.Entry(root, width=5,justify="right")
entry_orderno.config(validate="key", validatecommand=(vcmd_numeric, "%S", "%P"))

entry_orderdate = tk.Entry(root, width=20)
supplier_combobox = ttk.Combobox(root, width=80)
supplier_combobox['values'] = fetch_suppliers()
supplier_combobox.set("")
entry_sr = tk.Entry(root, width=5,justify="right")
entry_sr.config(validate="key", validatecommand=(vcmd_numeric, "%S", "%P"))
productitem_combobox = ttk.Combobox(root, width=80)
productitem_combobox['values'] = fetch_products()
productitem_combobox.set("")
productitem_combobox.bind("<<ComboboxSelected>>", on_product_select)
entry_detail = tk.Entry(root, width=80)
entry_unit = tk.Entry(root, width=10)
vcmd_unit = root.register(validate_unit_input)
entry_unit.config(validate="key", validatecommand=(vcmd_unit, "%S", "%P"))
# Configure the validate command for quantity
validate_quantity_cmd = root.register(validate_quantity)
entry_quantity = tk.Entry(root, width=10, justify="right")
#entry_quantity.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
entry_quantity.bind("<KeyRelease>", calculate_amount)  # Recalculate amount when quantity is updated
#entry_quantity.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
# Configure the validate command for rate
validate_rate_cmd = root.register(validate_rate)
entry_rate = tk.Entry(root, width=10, justify="right")
#entry_rate.config(validate="key", validatecommand=(validate_rate_cmd, "%S", "%P"))
entry_rate.bind("<KeyRelease>", calculate_amount)  # Recalculate amount when rate is updated

entry_amount= tk.Entry(root, width=12, justify="right")
entry_amount.config(state="readonly")
entry_totalvalue= tk.Entry(root, width=12,justify="right")
entry_totalvalue.config(state="readonly")
       
entries = [entry_orderno, entry_orderdate, supplier_combobox, entry_sr,productitem_combobox,entry_detail, entry_unit, entry_quantity,entry_rate,entry_amount,entry_totalvalue]
for i, (label_text, is_required) in enumerate(labels):
    frame = tk.Frame(root)  # Create a frame to contain label and asterisk
    frame.grid(row=i + 2, column=0, pady=5, padx=5, sticky="e")

    label = tk.Label(frame, text=label_text,font=("Arial", 9, "bold"))
    label.pack(side="left")

    if is_required:  # Add red asterisk for required fields
        asterisk = tk.Label(frame, text=" *", fg="red")
        asterisk.pack(side="left")
    entries[i].grid(row=i + 2, column=1, pady=5, padx=5, sticky="w")
    
# Set default values
entry_orderdate.insert(0, datetime.now().strftime("%d-%m-%Y"))
# Get the current date in DD-MM-YYYY format
#current_date = datetime.now().strftime("%d-%m-%Y")

if sales_data:
    entry_orderno.insert(0, sales_data.get("Orderno", ""))
    #entry_orderdate.insert(0, datetime.now().strftime("%d-%m-%Y"))
    supplier_combobox.insert(0, sales_data.get("Supplier", ""))
    entry_sr.insert(0, sales_data.get("Sr", ""))
    productitem_combobox.insert(0, sales_data.get("Productitem", ""))
    entry_detail.insert(0, sales_data.get("Description", ""))
    entry_unit.insert(0, sales_data.get("Unit", ""))
    entry_quantity.insert(0, str(sales_data.get("Quantity", "0.00")))
    entry_quantity.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
    entry_rate.insert(0, str(sales_data.get("Rate", "0.00")))
    entry_rate.config(validate="key", validatecommand=(validate_rate_cmd, "%S", "%P"))
    # entry_rate.insert(0, str(sales_data.get("Rate", "0.00")))
    entry_amount.config(state="normal")
    entry_amount.insert(0, str(sales_data.get("Amount", "0.00")))
    entry_amount.config(state="readonly")
    entry_totalvalue.config(state="normal")
    entry_totalvalue.insert(0, str(sales_data.get("Total Order Value", "0.00")))
    entry_totalvalue.config(state="readonly")

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=len(labels) + 2, column=1, pady=10, sticky="n")

save_button = tk.Button(button_frame, text="Save", command=save, width=10)
cancel_button = tk.Button(button_frame, text="Cancel", command=root.quit, width=10)

save_button.pack(side="left", padx=5)
cancel_button.pack(side="left", padx=5)

root.mainloop()

