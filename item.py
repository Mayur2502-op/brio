import mysql.connector
import tkinter as tk
from tkinter import messagebox
import json
import sys

# Read product data from the temporary JSON file
if len(sys.argv) > 1:
    temp_file = sys.argv[1]
    with open(temp_file, "r") as f:
        product_data = json.load(f)  # Load latest data
else:
    product_data = {}  # Create empty dictionary for new entries

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def Save():
    # Retrieve inputs
    item_name = entry_item_name.get()
    code = entry_code.get()
    detail = entry_detail.get()
    unit = entry_unit.get()
    rate = entry_rate.get()

    # Validate mandatory fields
    if not all([item_name, code, detail, unit, rate]):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Validate rate format
    try:
        rate_value = float(rate)  # Convert to float to ensure valid number
    except ValueError:
        messagebox.showerror("Invalid Input", "Rate must be a valid number.")
        return

    messagebox.showinfo("Save", "Done successfully!")

    conn = connect_db()
    cursor = conn.cursor()

    # Fetch count of Bsno
    cursor.execute("SELECT COUNT(Bsno) as stot_rows FROM item")
    result = cursor.fetchone()
    
    total_rows = result[0]

    #If total count is 0, set it to 1, otherwise increment by 1
    if total_rows == 0:
        total_rows = 1
    else:
        total_rows += 1 

    sql = """
    INSERT INTO item (Item, Codeno, Idesc, Unit, Rate, Bsno)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
    Item = VALUES(Item),
    Codeno = VALUES(Codeno), 
    Idesc = VALUES(Idesc), 
    Unit = VALUES(Unit), 
    Rate = VALUES(Rate),  
    Bsno = VALUES(Bsno)
    """
    
    values = (item_name, code, detail, unit, rate, total_rows)

    try:
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Product item saved successfully!")
        root.quit()  # Close form after saving
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        conn.close()

def Cancel():
    root.quit()

def back():
    root.quit()

def validate_unit(char, current_text):
    """Allow only alphabetic characters (A-Z, a-z) with a max length of 3."""
    if not char.isalpha():  # Ensure only alphabetic characters
        return False
    if len(current_text) > 4:  # Restrict to 3 characters max
        return False
    return True

def validate_numeric_input(char, current_text):
    """Allow only numeric input (with optional decimal)."""
    if char.isdigit() or (char == "." and "."  in current_text):
        return True
    return False    

# Create the main window
root = tk.Tk()
root.title("Product Item")
root.geometry("1600x1200")

# Configure grid weights for centering
for i in range(20):  # Adjust the range based on the number of rows
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
# Title Frame with Back Button
title_frame = tk.Frame(root)
title_frame.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")

# Add the Back button
back_btn = tk.Button(root, text="Back", command=back, width=10, fg="black")
back_btn.grid(row=0, column=0, pady=5, padx=5, sticky="w")
root.bind("<Alt-b>", lambda event: back())  # Alt + B shortcut

# Title Label
title_label = tk.Label(title_frame, text="Product Item", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="left", padx=10)

# Create form labels and entries
labels = [("Product Item ",True), ("Code ",True), ("Description",True), ("Unit",True), ("Rate",True)]

# Entry fields
entry_item_name = tk.Entry(root, width=40)
entry_code = tk.Entry(root, width=15)
entry_detail = tk.Entry(root, width=40)
validate_unit_cmd = root.register(validate_unit)

entry_unit = tk.Entry(
    root,
    width=5,
    validate="key",
    validatecommand=(validate_unit_cmd, "%S", "%P"),
    )

vcmd_numeric = root.register(validate_numeric_input)
entry_rate = tk.Entry(root, width=12,justify="right")
#entry_rate.config(validate="key", validatecommand=(vcmd_numeric, "%S", "%P"))

entries = [entry_item_name, entry_code, entry_detail, entry_unit, entry_rate]

# Pre-fill form fields if supplier data is available
if product_data:
    entry_item_name.insert(0, product_data["item_name"])
    entry_code.insert(0, product_data["code"])
    entry_detail.insert(0, product_data["detail"])
    entry_unit.insert(0, product_data["unit"])
    entry_rate.insert(0, product_data["rate"])
    entry_rate = tk.Entry(root, width=12,justify="right")
entry_rate.config(validate="key", validatecommand=(vcmd_numeric, "%S", "%P"))
       
# Place labels and entries
for i, (label_text, is_required) in enumerate(labels):
    frame = tk.Frame(root)  # Create a frame to contain label and asterisk
    frame.grid(row=i + 2, column=0, pady=5, padx=5, sticky="e")

    label = tk.Label(frame, text=label_text,font=("Arial", 9, "bold"))
    label.pack(side="left")

    if is_required:  # Add red asterisk for required fields
        asterisk = tk.Label(frame, text=" *", fg="red")
        asterisk.pack(side="left")
    entries[i].grid(row=i + 2, column=1, pady=5, padx=5, sticky="w")

# Create buttons
button_frame = tk.Frame(root)
button_frame.grid(row=len(labels) + 3, column=1, pady=10, sticky="w")

save_btn = tk.Button(button_frame, text="Save", command=Save, width=10)
cancel_btn = tk.Button(button_frame, text="Cancel", command=Cancel, width=10)

save_btn.pack(side="left", padx=5)
cancel_btn.pack(side="left", padx=5)

# Bind shortcuts
root.bind("<Alt-s>", lambda event: Save())  # Alt + S shortcut
root.bind("<Alt-c>", lambda event: Cancel())  # Alt + C shortcut

# Start the main loop
root.mainloop()