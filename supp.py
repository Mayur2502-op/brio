import mysql.connector
import tkinter as tk
import re
from tkinter import ttk
from tkinter import messagebox
import json
import sys

# Read supplier data from the temporary JSON file
if len(sys.argv) > 1:
    temp_file = sys.argv[1]
    with open(temp_file, "r") as f:
        supplier_data = json.load(f)  # Load latest data
else:  
    supplier_data = {}  # Create empty dictionary for new entries

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def save():
    company_name = entry_name.get()
    address1 = entry_address1.get()
    address2 = entry_address2.get()
    city = entry_city.get()
    pincode = entry_pincode.get()
    state = state_combobox.get()
    mobile = entry_mobile.get()
    email = entry_email.get()
    gst_no = entry_gst.get()

    # Ensure all fields are filled
    if all([company_name, address1, address2, city, pincode, state, mobile, email, gst_no]) and state != "Select State":

        if len(mobile) != 10 or not mobile.isdigit():
            messagebox.showerror("Error", "Mobile number must be 10 numeric digits!")
            return
        
        # Validate email address
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email address!")
            return

    conn = connect_db()
    cursor = conn.cursor()

     # Get the next available Bsno
    cursor.execute("SELECT MAX(Bsno) FROM supplier")
    result = cursor.fetchone()
    next_bsno = 1 if result[0] is None else result[0] + 1

    # SQL insertion statement
    sql = """
    INSERT INTO supplier ( Bsno, Name, Add1, Add2, City, Pincode, State, Mobileno, Email, GSTno)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
     Bsno=VALUES(Bsno),Name=VALUES(Name) ,Add1=VALUES(Add1), Add2=VALUES(Add2), City=VALUES(City), Pincode=VALUES(Pincode),
    State=VALUES(State), Mobileno=VALUES(Mobileno), Email=VALUES(Email), GSTno=VALUES(GSTno)
    """
    values = (
        next_bsno,entry_name.get(), entry_address1.get(), entry_address2.get(),
        entry_city.get(), entry_pincode.get(), state_combobox.get(),
        entry_mobile.get(), entry_email.get(), entry_gst.get()
    )

    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Supplier saved successfully!")
    root.quit()

def cancel():
    root.quit()
    
def enforce_lowercase(event):
    value = entry_email.get()
    entry_email.delete(0, tk.END)
    entry_email.insert(0, value.lower())  # Convert to lowercase

def filter_combobox(event, combobox, values):
    typed_select = combobox.get().upper()

    if not typed_select:
        combobox['values'] = values  # Show full list when empty
    else:
        filtered_values = [v for v in values if v.upper().startswith(typed_select)]  # Only match the beginning
        combobox['values'] = filtered_values  

    combobox.event_generate('<Down>')  # Open dropdown automatically

def back():
    root.quit()  # This could be changed to navigate back to another window

# Function to automatically clean non-numeric input for pincode
def clean_pincode(event):
    value = entry_pincode.get()
    entry_pincode.delete(0, tk.END)
    entry_pincode.insert(0, ''.join(filter(str.isdigit, value))[:6])  # Keep only digits, max 6 digits

# Function to automatically clean non-numeric input for mobile
def clean_mobile(event):
    value = entry_mobile.get()
    entry_mobile.delete(0, tk.END)
    entry_mobile.insert(0, ''.join(filter(str.isdigit, value))[:10])  # Keep only digits, max 10 digits

# Create the main window
root = tk.Tk()
root.title("Supplier")
root.geometry("1600x1200")

# Configure grid weights for centering
for i in range(20):  # Adjust the range based on the number of rows
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Title Frame with Back Button
title_frame = tk.Frame(root)
title_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

# Title Label
title_label = tk.Label(title_frame, text="Supplier", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="left", padx=10)

# Create form labels and entries
labels = [("Name",True), ("Address",True), ("Address",True), ("City",True),("Pincode",True), ("State",True),( "Mobile No.",True), ("Email",True), ("GST No",True)]

entry_name = tk.Entry(root, width=100)
entry_address1 = tk.Entry(root, width=100)
entry_address2 = tk.Entry(root, width=100)
entry_city = tk.Entry(root, width=50)
entry_pincode = tk.Entry(root, width=8)
entry_pincode.bind("<KeyRelease>", clean_pincode)
# state combobox
state_combobox = ttk.Combobox(root, width=30, state="normal")
states = ("ANDAMAN AND NICOBAR ISLANDS", "ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR", "CHANDIGARH", "CHHATTISGARH",
    "DADRA AND NAGAR HAVELI AND DIV AND DAMAN", "DAMAN AND DIV", "DELHI", "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH",
    "JAMMU AND KASHMIR", "JHARKHAND", "KARNATAKA", "KERALA", "LADAKH", "LAKSHADWEEP", "MADHYA PRADESH", "MAHARASHTRA",
    "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "ODISHA", "PONDICHERRY", "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU",
    "TELANGANA", "TIRUPATI", "TRIPURA", "UTTAR PRADESH", "UTTARAKHAND", "WEST BENGAL", "OTHER COUNTRIES"
)  # Add countries as needed
state_combobox.grid(row=6, column=1, pady=5, padx=5, sticky="w")
state_combobox.set("Select State")  # Default placeholder
# Bind filtering function to KeyRelease event
state_combobox.bind("<KeyRelease>", lambda event: filter_combobox(event, state_combobox, states))

entry_mobile = tk.Entry(root, width=12)
entry_mobile.bind("<KeyRelease>", clean_mobile)
entry_email = tk.Entry(root, width=25)
entry_email.bind("<KeyRelease>", enforce_lowercase)
entry_gst = tk.Entry(root, width=15)

entries = [entry_name, entry_address1, entry_address2, entry_city, entry_pincode, state_combobox, entry_mobile, entry_email, entry_gst]
# Pre-fill form fields if supplier data is available
if supplier_data:
    entry_name.insert(0, supplier_data["Name"])
    entry_address1.insert(0, supplier_data["Address1"])
    entry_address2.insert(0, supplier_data["Address2"])
    entry_city.insert(0, supplier_data["City"])
    entry_pincode.insert(0, supplier_data["Pincode"])
    state_combobox.insert(0, supplier_data["State"])
    entry_mobile.insert(0, supplier_data["Mobile"])
    entry_email.insert(0, supplier_data["Email"])
    entry_gst.insert(0, supplier_data["GST No"])

# Add the Back button to the first row, last column
back_btn = tk.Button(root, text="Back", command=back, width=10, fg="black")
back_btn.grid(row=0, column=0, pady=5, padx=5, sticky="w")
root.bind("<Alt-b>", lambda event: back())  # Alt + b shortcut
    
# Add labels and entries to the form
for i, (label_text, is_required) in enumerate(labels):
    frame = tk.Frame(root)  # Create a frame to contain label and asterisk
    frame.grid(row=i + 2, column=0, pady=5, padx=5, sticky="e")

    label = tk.Label(frame, text=label_text,font=("Arial", 9, "bold"))
    label.pack(side="left")

    if is_required:  # Add red asterisk for required fields
        asterisk = tk.Label(frame, text=" *", fg="red")
        asterisk.pack(side="left")
    entries[i].grid(row=i+2, column=1, pady=5, padx=5, sticky="w")

# Create buttons
button_frame = tk.Frame(root)
button_frame.grid(row=len(labels)+2, column=1, pady=10, sticky="w")

update_button =tk.Button(button_frame, text="save", command=save, width=10)
cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)

update_button.pack(side="left", padx=5)
cancel_btn.pack(side="left", padx=5)
root.bind("<Alt-s>", lambda event: save())  # Alt + s shortcut
root.bind("<Alt-c>", lambda event: cancel())  # Alt + c shortcut

# Start the main loop
root.mainloop()
