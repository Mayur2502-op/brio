import tkinter as tk
import mysql.connector
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
import sys
import json

if len(sys.argv) > 1:
    temp_file = sys.argv[1]
    with open(temp_file, "r") as f:
        sales_data = json.load(f)
else:
    sales_data = {}

def connect_db():
    """Connect to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="briodata"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None
    
def fetch_suppliers():
    conn = connect_db()  # Get connection
    if not conn:
        return []  # Return empty list if connection fails

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Supplier")
        suppliers = [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching suppliers: {e}")
        suppliers = []
    finally:
        cursor.close()
        conn.close()  # Ensure connection is closed properly

    return suppliers

def fetch_products():
    conn = connect_db()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Item FROM Item")  # Ensure 'Item' is the correct column name
        products = [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching products: {e}")
        products = []
    finally:
        cursor.close()
        conn.close()  # Ensure connection is closed properly

    return products

def fetch_product_details(product_name):
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor() 
    cursor.execute("SELECT Idesc, Unit, Rate FROM Item WHERE Item = %s", (product_name,))
    product_details = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if product_details:
        return {"description": product_details[0], "unit": product_details[1], "rate": product_details[2]}
    return None

#def save():
 #   orderno = order_no_entry.get().strip()
  #  orderdate = order_date_entry.get().strip()
   # supplier = vendor_combobox.get().strip()
    #sr = sr_entry.get().strip()
#    productitem = item_combobox.get().strip()
 #   detail = detail_entry.get().strip()
  #  unit = unit_entry.get().strip()
   # quantity = quantity_entry.get().strip()
    #rate = rate_entry.get().strip()
#    amount = amount_entry.get().strip()
 #   totalvalue = total_entry.get().strip()

    # Validate mandatory fields
  #  if not all([orderno,orderdate, supplier,sr,productitem, detail, unit,quantity, rate,amount,totalvalue]):
      #  messagebox.showerror("Error", "All fields are required!")


   # conn = connect_db()
    #cursor = conn.cursor()

    # Fetch count of Bsno
#    cursor.execute("SELECT COUNT(Bsno) as stot_rows FROM somst")
 #   result = cursor.fetchone()
    
  #  total_rows = result[0]

    #If total count is 0, set it to 1, otherwise increment by 1
   # if total_rows == 0:
    #    total_rows = 1
#    else:
 #       total_rows += 1 

  #  sql = """
   #    INSERT INTO somst (Bsno, Ordno, Orddt, Sname, Sr, Item, Idesc, Unit, Quantity, Rate, Amount, Ordval) 
    #   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
     #  ON DUPLICATE KEY UPDATE 
      # Bsno=VALUES(Bsno),         
       #Orddt=VALUES(Orddt),
#       Sname=VALUES(Sname),
 #      Sr=VALUES(Sr),
  #     Item=VALUES(Item),
   #    Idesc=VALUES(Idesc),
    #   Unit=VALUES(Unit),
     #  Quantity=VALUES(Quantity),
      # Rate=VALUES(Rate),
       #Amount=VALUES(Amount),
#       Ordval=VALUES(Ordval)
 #   """
  #  orderdate = datetime.strptime(order_date_entry.get(), "%d-%m-%Y").date()  # Convert to datetime.date
   # values = (total_rows, order_no_entry.get(),orderdate,vendor_combobox.get(), sr_entry.get(), item_combobox.get(), detail_entry.get(),unit_entry.get(), quantity_entry.get(), rate.get(), amount_entry.get(), total_entry.get())

    #cursor.execute(sql, values)
#    conn.commit()
 #   conn.close()
  #  messagebox.showinfo("Success", "Sales order saved successfully!")
   # window.quit()


def save():
    orderno = order_no_entry.get().strip()
    orderdate = order_date_entry.get().strip()
    supplier = vendor_combobox.get().strip()
    sr = sr_entry.get().strip()
    productitem = item_combobox.get().strip()
    detail = detail_entry.get().strip()
    unit = unit_entry.get().strip()
    quantity = quantity_entry.get().strip()
    rate = rate_entry.get().strip()
    amount = amount_entry.get().strip()
    totalvalue = total_entry.get().strip()

    # Validate mandatory fields
    if not all([orderno, orderdate, supplier, sr, productitem, detail, unit, quantity, rate, amount, totalvalue]):
        messagebox.showerror("Error", "All fields are required!")
        #return  # Exit the save function if any required field is empty
    
    #"""Saves sales order data into MySQL."""
    #conn = connect_db()  # Ensure you have a valid database connection function
    #if not conn:
     #   return

    #cursor = conn.cursor()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT Name FROM Supplier")  # Replace 'name' with your actual column name
    cursor.fetchall()  # Fetch all results to clear buffer

    cursor.execute("SELECT Item FROM Item")  # Replace 'name' with your actual column name
    cursor.fetchall()  # Fetch all results to clear buffer

    # Fetch count of Bsno **before** entering the loop
    cursor.execute("SELECT COUNT(Bsno) as stot_rows FROM somst")
    result = cursor.fetchone()
    total_rows = result[0] if result else 0  # Ensure total_rows is initialized

    total_rows = total_rows + 1 if total_rows else 1

    try:
        # Fetch the last order number from DB (if needed)
        cursor.execute("SELECT MAX(Ordno) FROM somst")
        last_order_no = cursor.fetchone()[0]  # Get last order number
        order_no = int(last_order_no) + 1 if last_order_no and str(last_order_no).isdigit() else 1

        # Serial number starts at 1 for each order
        serial_no = 1 
        # Insert order items **inside the loop**
        for row_widgets in rows:
            product_item = row_widgets[2].get().strip()
            description = row_widgets[3].get().strip()
            unit = row_widgets[4].get().strip()

            # Convert numeric fields
            try:
                quantity = float(row_widgets[5].get().strip())
            except ValueError:
                quantity = 0.0

            try:
                rate = float(row_widgets[6].get().strip())
            except ValueError:
                rate = 0.0

            try:
                amount = float(row_widgets[7].get().strip())
            except ValueError:
                amount = 0.0
            
            # Insert into order items table
            cursor.execute(
               """INSERT INTO somst ( Bsno,Ordno, Orddt, Sname,Sr, Item, Idesc, Unit, Quantity, Rate, Amount, Ordval) 
                  VALUES (%s,%s, CURDATE(), %s,%s, %s, %s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE 
                  Bsno=VALUES(Bsno)
                     ordno=VALUES(Bsno), 
                   Orddt=VALUES(Orddt), -- MySQL will use the current date
                   Sname=VALUES(Sname),
                  Sr=VALUES(Sr),
                   Item=VALUES(Item),
                   Idesc=VALUES(Idesc), 
                   Unit=VALUES(Unit),
                   Quantity=VALUES(Quantity), 
                  Rate=VALUES(Rate),  
                   Amount=VALUES(Amount),
                   Ordval=VALUES(Ordval),""",
                    (total_rows, order_no, supplier, serial_no, product_item, description, unit, quantity, rate, amount, totalvalue)
            )
            serial_no += 1  # Increment Sr number for next item

        conn.commit()
        messagebox.showinfo("Save", "Order saved successfully!")
        window.quit()  # Close the application window

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error saving data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def auto_fill_product_details(event, item_combobox, description_entry, unit_entry, rate_entry):
    product_name = item_combobox.get()
    if not product_name:
        return
    
    details = fetch_product_details(product_name)
    if details:
        description_entry.delete(0, tk.END)
        description_entry.insert(0, details["description"])

        unit_entry.delete(0, tk.END)
        unit_entry.insert(0, details["unit"])

        rate_entry.delete(0, tk.END)
        rate_entry.insert(0, str(details["rate"]))

#def calculate_amount(event=None, quantity_widget=None, rate_widget=None, amount_widget=None):
 #   """Calculate and update the amount field when quantity or rate is changed."""
  #  try:
   #     quantity = float(quantity_widget.get().strip()) if quantity_widget else 0.0
    #    rate = float(rate_widget.get().strip()) if rate_widget else 0.0
     #   amount = quantity * rate
      #  amount_widget.config(state="normal")  # Enable editing of the amount field
       # amount_widget.delete(0, tk.END)  # Clear the current value
        #amount_widget.insert(0, f"{amount:.2f}")  # Set the new amount value
#        amount_widget.config(state="readonly")  # Make it readonly again
 #   except ValueError:
  #      amount_widget.config(state="normal")
   #     amount_widget.delete(0, tk.END)
    #    amount_widget.insert(0, "0.00")
     #   amount_widget.config(state="readonly")

def calculate_amount(event=None, quantity_entry=None, rate_entry=None, amount_entry=None):
    try:
        # Get the quantity and rate from the respective entry fields
        quantity = float(quantity_entry.get().strip())
        rate = float(rate_entry.get().strip())
        
        # Calculate the amount (Quantity * Rate)
        amount = quantity * rate
        
        # Update the amount field for this row
        amount_entry.config(state="normal")
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, str(round(amount, 2)))
        amount_entry.config(state="readonly")
        
        # Now update the total order value
        update_total_order_value()
    except ValueError:
        # If there's an error with conversion, set amount to 0
        amount_entry.config(state="normal")
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, "0.00")
        amount_entry.config(state="readonly")
        update_total_order_value()

def update_total_order_value():
    """Calculate and update the total order value by summing the amounts of all rows."""
    total_order_value = 0.0
    
    # Iterate through all rows and sum the amounts
    for row in rows:
        amount_entry = row[6]  # The 7th element is the 'amount' entry
        try:
            amount = float(amount_entry.get().strip())
            total_order_value += amount
        except ValueError:
            continue  # If there's an invalid value, skip to next row
    
    # Update the total entry field
    total_entry.config(state="normal")
    total_entry.delete(0, tk.END)
    total_entry.insert(0, str(round(total_order_value, 2)))  # Round to 2 decimal places
    total_entry.config(state="readonly")


def add_new_row():
    """Add a new row with editable fields."""
    row_index = len(rows) + 1

    new_sr_entry = tk.Entry(courses_frame, width=3, justify="right")
    new_sr_entry.grid(row=row_index, column=0)
    new_sr_entry.insert(0, str(row_index))  # Set serial number

    new_item_combobox = ttk.Combobox(courses_frame, width=70)
    new_item_combobox.grid(row=row_index, column=1)
    new_item_combobox["values"] = fetch_products()  # Populate with items from DB
    new_item_combobox.set("")  # Default empty

    new_detail_entry = tk.Entry(courses_frame, width=70)
    new_detail_entry.grid(row=row_index, column=2)

    new_unit_entry = tk.Entry(courses_frame, width=5)
    new_unit_entry.grid(row=row_index, column=3)

    new_quantity_entry = tk.Entry(courses_frame, width=7, justify="right")
    new_quantity_entry.grid(row=row_index, column=4)
    new_quantity_entry.bind("<KeyRelease>", lambda event: calculate_amount(event, new_quantity_entry, new_rate_entry, amount_entry))  # Recalculate amount when quantity changes

    new_rate_entry = tk.Entry(courses_frame, width=12, justify="right")
    new_rate_entry.grid(row=row_index, column=5)
    new_rate_entry.bind("<KeyRelease>", lambda event: calculate_amount(event, new_quantity_entry, new_rate_entry, amount_entry))  # Recalculate amount when rate changes

    amount_entry = tk.Entry(courses_frame, width=12, justify="right", state="readonly")
    amount_entry.grid(row=row_index, column=6)

    # Append widgets of the new row into the list for later reference
    rows.append(
        (
            new_sr_entry,
            new_item_combobox,
            new_detail_entry,
            new_unit_entry,
            new_quantity_entry,
            new_rate_entry,
            amount_entry,  # Ensure the amount entry is included in the row tuple
        )
    )

    new_quantity_entry.bind("<KeyRelease>", lambda event: calculate_amount(event, new_quantity_entry, new_rate_entry, amount_entry))
    new_rate_entry.bind("<KeyRelease>", lambda event: calculate_amount(event, new_quantity_entry, new_rate_entry, amount_entry))

    # Bind product selection to auto-fill fields
    new_item_combobox.bind("<FocusOut>", lambda event: auto_fill_product_details(event, new_item_combobox, new_detail_entry, new_unit_entry, new_rate_entry))

def edit_row():
    """Enables editing for the selected row."""
    selected_row_index = int() - 1  # Get row index from Sr number

    if selected_row_index < len(rows):
        row_widgets = rows[selected_row_index]
        
        # Enable editing for item, description, unit, quantity, and rate
        for i in range(1, 6):  # Ignore Sr and Amount
            row_widgets[i].config(state="normal")

        # Bind key events to recalculate amount on edit
        row_widgets[4].bind("<KeyRelease>", lambda event: calculate_amount(row_widgets[4], row_widgets[5], row_widgets[6]))
        row_widgets[5].bind("<KeyRelease>", lambda event: calculate_amount(row_widgets[4], row_widgets[5], row_widgets[6]))

        messagebox.showinfo("Edit Mode", f"Row {selected_row_index + 1} is now editable.")

def delete_row():
    """Deletes the last added row."""
    if rows:
        row_widgets = rows.pop()  # Remove last row from list

        # Destroy each widget in the row
        for widget in row_widgets:
            widget.destroy()

        # Update Sr numbers
        for i, row in enumerate(rows):
            row[0].delete(0, tk.END)
            row[0].insert(0, str(i + 1))  # Renumber Sr column

        messagebox.showinfo("Row Deleted", " row deleted .")
    else:
        messagebox.showerror("Error", "No rows left to delete!")

def Cancel():
    window.quit()

def Back():
    window.quit()
        
def validate_unit(char, current_text):
    """Allow only alphabetic characters (A-Z, a-z) with a max length of 3."""
    if not char.isalpha():  # Ensure only alphabetic characters
        return False
    if len(current_text) > 4:  # Restrict to 3 characters max
        return False
    return True
    # Validation functions
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

# Initialize an empty list for row storage before using it
rows = []

# Initialize the main window
window = tk.Tk()
window.title("Sales Order")
window.geometry("1600x1200")
frame = tk.Frame(window)
frame.pack()

# Title Frame with Back Button and Title
btn_frame = tk.Frame(frame)
btn_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

title_frame = tk.Frame(frame)
title_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

# Back Button
back_btn = tk.Button(btn_frame, text="Back", command=Back, width=10, fg="black")
back_btn.pack(side="left", padx=5)
window.bind("<Alt-b>", lambda event: Back())  # Alt + b shortcut

# Title Label
title_label = tk.Label(title_frame, text="Sales Order", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="right", padx=10)

# User Info Frame
user_info_frame = tk.LabelFrame(frame, text="")
user_info_frame.grid(row=2, column=0, padx=10, pady=10)
row_index = len(rows) + 1

order_no_label = tk.Label(user_info_frame, text="Order No",font=("Arial", 9, "bold"))
order_no_label.grid(row=0, column=0)
order_no_entry = tk.Entry(user_info_frame, width=20, justify="right")
order_no_entry.grid(row=1, column=0)

# Get the current date in DD-MM-YYYY format
current_date = datetime.now().strftime("%d-%m-%Y")

order_date_label = tk.Label(user_info_frame, text="Date",font=("Arial", 9, "bold"))
order_date_label.grid(row=0, column=1)
order_date_entry = tk.Entry(user_info_frame, width=15)
order_date_entry.grid(row=1, column=1)
# Set default value to the current date
order_date_entry.insert(0, current_date)

vendor_label = tk.Label(user_info_frame, text="Supplier",font=("Arial", 9, "bold"))
vendor_label.grid(row=0, column=2)
vendor_combobox = ttk.Combobox(user_info_frame, width=80)
vendor_combobox.grid(row=1, column=2)

# Populate Combobox with supplier names
vendor_combobox["values"] = fetch_suppliers()

# Courses Frame
courses_frame = tk.LabelFrame(frame, text="")
courses_frame.grid(row=3, column=0, padx=10, pady=10, sticky="news")
sr_entry = tk.Entry(courses_frame, width=3,justify="right")
item_combobox = ttk.Combobox(courses_frame, width=70)
detail_entry = tk.Entry(courses_frame, width=70)
vcmd_unit = courses_frame.register(validate_unit)
unit_entry = tk.Entry(courses_frame,width=5,validate="key",validatecommand=(vcmd_unit, "%S", "%P"))
quantity_entry = tk.Entry(courses_frame, width=10, justify="right")
rate_entry = tk.Entry(courses_frame, width=10, justify="right")
amount_entry = tk.Entry(courses_frame, width=12,justify="right",state="readonly")

# Headers
headers = ["Sr", "Product Item", "Description", "Unit", "Quantity", "Rate", "Amount"]
for col, text in enumerate(headers):
    tk.Label(courses_frame, text=text,font=("Arial", 9, "bold")).grid(row=0, column=col, padx=5, pady=5)

rows = []  # List to store dynamically added rows

# Add the first row
validate_unit_cmd = window.register(validate_unit)
validate_quantity_cmd = window.register(validate_quantity)
validate_rate_cmd = window.register(validate_rate)
# Add the first row
add_new_row()

action_label = tk.Label(courses_frame, text="Action",font=("Arial", 9, "bold"))
action_label.grid(row=0, column=9)
add_button = tk.Button(courses_frame, text="Add", command=add_new_row)
add_button.grid(row=1, column=8)
window.bind("<Alt-a>", lambda event: add_new_row())  # Alt + a shortcut
edit_button = tk.Button(courses_frame, text="Edit", command=edit_row)
edit_button.grid(row=1, column=9)
window.bind("<Alt-e>", lambda event: edit_row())  # Alt + e shortcut
delete_button= tk.Button(courses_frame, text="Delete", command=delete_row)
delete_button.grid(row=1, column=10)
window.bind("<Alt-d>", lambda event: delete_row())  # Alt + d shortcut

# Total Frame
total_frame = tk.LabelFrame(frame, text="")
total_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ne")

total_label = tk.Label(total_frame, text="Total Order Value",font=("Arial", 9, "bold"))
total_label.grid(row=2, column=0)
total_entry = tk.Entry(total_frame, width=20)
total_entry.grid(row=2, column=1)

# Pre-fill form fields if sales data is available
if sales_data:
    # Populate fields in your form
    order_no_entry.insert(0, sales_data.get("order_no", ""))
    order_date_entry.insert(0, sales_data.get("order_date", ""))
    vendor_combobox.insert(0, sales_data.get("supplier", ""))
    sr_entry.insert(0,sales_data.get("Sr",""))
    item_combobox.insert(0,sales_data.get("Product Item",""))
    detail_entry.insert(0,sales_data.get("Description",""))
    unit_entry.insert(0,sales_data.get("Unit",""))
    quantity_entry.insert(0, str(sales_data.get("Quantity", "0.00")))
    quantity_entry.config(validate="key", validatecommand=(validate_quantity_cmd, "%S", "%P"))
    rate_entry.insert(0, str(sales_data.get("Rate", "0.00")))
    rate_entry.config(validate="key", validatecommand=(validate_rate_cmd, "%S", "%P"))
    # entry_rate.insert(0, str(sales_data.get("Rate", "0.00")))
    amount_entry.config(state="normal")
    amount_entry.insert(0, str(sales_data.get("Amount", "0.00")))
    amount_entry.config(state="readonly")
    total_entry.config(state="normal")
    total_entry.insert(0, str(sales_data.get("Total Order Value", "0.00")))
    total_entry.config(state="readonly")
 
# Save and Cancel Buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=5, column=0, padx=10, pady=10, sticky="n")

save_button = tk.Button(button_frame, text="Save", command=save, width=10)
save_button.pack(side="left", padx=5)
window.bind("<Alt-s>", lambda event: save())  # Alt + s shortcut

cancel_button = tk.Button(button_frame, text="Cancel", command=Cancel, width=10)
cancel_button.pack(side="left", padx=5)
window.bind("<Alt-c>", lambda event: Cancel())  # Alt + c shortcut

# Mainloop
window.mainloop()