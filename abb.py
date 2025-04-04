import mysql.connector
import tkinter as tk
import re
from tkinter import ttk
from tkinter import messagebox

# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def update_user():
    new_name = entry_name.get()
    new_address1 = entry_address1.get()
    new_address2 = entry_address2.get()
    new_city = entry_city.get()
    new_pincode = entry_pincode.get()
    new_state = state_combobox.get()
    new_country = country_combobox.get()
    new_mobile = entry_mobile.get()
    new_email = entry_email.get()

    if new_name == "" or new_address1 == "" or new_address2 == "" or new_city == "" or new_pincode == "" or new_state == "" or new_country == "" or new_mobile == "" or new_email == "":
        messagebox.showerror("Input Error", "Please fill in all fields")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Ensure you have a unique identifier (e.g., company_id) to update a specific row
          # Replace this with the actual ID, maybe from a selected record

        # Corrected Update query with WHERE condition
        query = """UPDATE company 
                   SET  name=%s, add1=%s, add2=%s, city=%s, 
                       pincode=%s, state=%s, country=%s, mobileno=%s, email=%s 
                   """
        
        cursor.execute(query, (new_name, new_address1, new_address2, new_city, new_pincode, new_state, new_country, new_mobile, new_email))

        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Update Successful", "Company Data Updated Successfully!")
            root.destroy()
        else:
            messagebox.showwarning("Update Failed", "No company found with the given ID.")
            root.destroy()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        cursor.close()
        conn.close()        

# Function to fetch and display the last entered record
def fetch_last_entry():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Fetch the last entered record based on ID (assuming company_id is auto-incremented)
        query = "SELECT * FROM company "
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            entry_name.insert(0, result[1])       # Name
            entry_address1.insert(0, result[2])   # Address1
            entry_address2.insert(0, result[3])   # Address2
            entry_city.insert(0, result[4])       # City
            entry_pincode.insert(0, result[5])    # Pincode
            state_combobox.set(result[6])         # State
            country_combobox.set(result[7])       # Country
            entry_mobile.insert(0, result[8])     # Mobile No.
            entry_email.insert(0, result[9])      # Email

        else:
            messagebox.showinfo("Info", "No previous data found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

def save():
    name = entry_name.get()
    address1 = entry_address1.get()
    address2 = entry_address2.get()
    city = entry_city.get()
    pincode = entry_pincode.get()
    state = state_combobox.get()
    country = country_combobox.get()
    mobile = entry_mobile.get()
    email = entry_email.get()

    if all([name, address1, address2, city,pincode, state, country,  mobile, email]) and \
       state != "Select State" and country != "Select Country": 

        if len(mobile) != 10 or not mobile.isdigit():
            messagebox.showerror("Error", "Mobile number must be 10 numeric digits!")
            return

        if len(pincode) != 6 or not pincode.isdigit():
            messagebox.showerror("Error", "Pincode must be 6 numeric digits!")
            return

        # Validate email address
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email address!")
            return

        messagebox.showinfo("Save", "Done successfully!")
    else:
        messagebox.showerror("Error", "check for mandatory input!")
       
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
    root.quit()

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
root.title("Company")
root.geometry("1600x1200")

# Configure grid weights for centering
for i in range(20):  # Adjust the range based on the number of rows
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Title Frame with Back Button
title_frame = tk.Frame(root)
title_frame.grid(row=1, column=1, columnspan=2, pady=10, sticky="w")

# Add the Back button to the first row, last column
back_btn = tk.Button(root, text="Back", command=back, width=10, fg="black")
back_btn.grid(row=0, column=0, pady=5, padx=5, sticky="w")
root.bind("<Alt-b>", lambda event: back())  # Alt + b shortcut

# Title Label
title_label = tk.Label(title_frame, text="Company", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="left", padx=10)

# Create form labels and entries with asterisks for required fields
labels = [("Name", True), ("Address ", True), ("Address ", True), ("City", True), 
          ("Pincode", True),("State", True),  ("Country", True), ("Mobile No.", True), ("Email", True)]

entry_name = tk.Entry(root, width=80)
entry_address1 = tk.Entry(root, width=80)
entry_address2 = tk.Entry(root, width=80)
entry_city = tk.Entry(root, width=30)

entry_pincode = tk.Entry(root, width=10)
entry_pincode.bind("<KeyRelease>", clean_pincode)  # Bind to clean pincode input dynamically
# state combobox
state_combobox = ttk.Combobox(root, width=30, state="normal")
states =sorted (["ANDAMAN AND NICOBAR ISLANDS", "ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR", "CHANDIGARH", "CHHATTISGARH",
    "DADRA AND NAGAR HAVELI AND DIV AND DAMAN", "DAMAN AND DIV", "DELHI", "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH",
    "JAMMU AND KASHMIR", "JHARKHAND", "KARNATAKA", "KERALA", "LADAKH", "LAKSHADWEEP", "MADHYA PRADESH", "MAHARASHTRA",
    "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "ODISHA", "PONDICHERRY", "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU",
    "TELANGANA", "TIRUPATI", "TRIPURA", "UTTAR PRADESH", "UTTARAKHAND", "WEST BENGAL", "OTHER COUNTRIES"
])  # Add countries as needed
state_combobox.grid(row=6, column=1, pady=5, padx=5, sticky="w")
state_combobox['values'] = states
state_combobox.set("Select State")  # Default placeholder

# Bind filtering function to KeyRelease event
state_combobox.bind("<KeyRelease>", lambda event: filter_combobox(event, state_combobox, states))

# Country combobox
country_combobox = ttk.Combobox(root, width=30, state="normal")
countries= sorted ([ "ANDORRA", "UNITED ARAB EMIRATES","AFGHANISTAN","ANTIGUA AND BARBUDA","ANDUILLA","ALBANIA","ARMENIA","ANGOLA","ANTARCTICA","AMERICAN SAMOA","AUSTRIA","AUSTRALIA","ARUBA","ALAND","AZERBAIJAN","BOSNIA AND HERZEGOVINA","BARBADOS","BANGLADESH","BELGIUM","BURKINA FASO","BULGARIA","BAHRAIN","BENIN","BURUNDI","BRAZIL","BOLIVIA","BAHAMAS","BRUNEI","BRAZIL","BHUTAN","BOUVET ISLAND","BOTSWANA","BELARUS","BELIZE","CANADA","COCOS ISLAND","CENTRAL AFRICAN REPUBLIC","REPUBLIC OF THE CONGO","SWITZELAND","IVOTY COAST","COOK ISLAND","CHILE","CAMEROON","CHINA","CHILE","COSTA RICA","CUBA","CAPE VERDE","CURACAO","CYPRUS","CYPRUS","CZECH REPUBLIC","DENMARK","DJIBOUTI","DOMINICA","DOMINICAN REPUBLIC""ECUADOR", "EGYPT", "EL SALVADOR", "EQUATORIAL GUINEA", "ERITREA", "ESTONIA", 
    "ESWATINI", "ETHIOPIA", "FIJI", "FINLAND", "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA", 
    "GREECE", "GRENADA", "GUATEMALA", "GUINEA", "GUINEA-BISSAU", "GUYANA", "HAITI", "HONDURAS", "HUNGARY", 
    "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND", "ISRAEL", "ITALY", "JAMAICA", "JAPAN", 
    "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KOREA (NORTH)", "KOREA (SOUTH)", "KUWAIT", "KYRGYZSTAN", 
    "LAOS", "LATVIA", "LEBANON", "LESOTHO", "LIBERIA", "LIBYA", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG", 
    "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES", "MALI", "MALTA", "MARSHALL ISLANDS", "MAURITANIA", 
    "MAURITIUS", "MEXICO", "MICRONESIA", "MOLDOVA", "MONACO", "MONGOLIA", "MONTENEGRO", "MOROCCO", 
    "MOZAMBIQUE", "MYANMAR", "NAMIBIA", "NAURU", "NEPAL", "NETHERLANDS", "NEW ZEALAND", "NICARAGUA", 
    "NIGER", "NIGERIA", "NORTH MACEDONIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PALESTINE", "PANAMA", 
    "PAPUA NEW GUINEA", "PARAGUAY", "PERU", "PHILIPPINES", "POLAND", "PORTUGAL", "QATAR", "ROMANIA", "RUSSIA", 
    "RWANDA", "SAINT KITTS AND NEVIS", "SAINT LUCIA", "SAINT VINCENT AND THE GRENADINES", "SAMOA", 
    "SAN MARINO", "SAO TOME AND PRINCIPE", "SAUDI ARABIA", "SENEGAL", "SERBIA", "SEYCHELLES", "SIERRA LEONE", 
    "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOLOMON ISLANDS", "SOMALIA", "SOUTH AFRICA", "SOUTH SUDAN", 
    "SPAIN", "SRI LANKA", "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND", "SYRIA", "TAJIKISTAN", "TANZANIA", 
    "THAILAND", "TIMOR-LESTE", "TOGO", "TONGA", "TRINIDAD AND TOBAGO", "TUNISIA", "TURKEY", "TURKMENISTAN", 
    "TUVALU", "UGANDA", "UKRAINE", "UNITED ARAB EMIRATES", "UNITED KINGDOM", "UNITED STATES", "URUGUAY", 
    "UZBEKISTAN", "VANUATU", "VATICAN CITY", "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE"])  # Add countries as needed
country_combobox.grid(row=6, column=1, pady=5, padx=5, sticky="w")
country_combobox['values'] = countries
country_combobox.set("Select Country")  # Default placeholder
country_combobox.bind("<KeyRelease>", lambda event: filter_combobox(event, country_combobox, countries))

entry_mobile = tk.Entry(root, width=15)
entry_mobile.bind("<KeyRelease>", clean_mobile)  # Bind to clean mobile input dynamically

entry_email = tk.Entry(root, width=30)
entry_email.bind("<KeyRelease>", enforce_lowercase)

entries = [entry_name, entry_address1, entry_address2, entry_city,entry_pincode, state_combobox, country_combobox, entry_mobile, entry_email]

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
button_frame.grid(row=len(labels) + 2, column=1, pady=10, sticky="w")

update_button =tk.Button(button_frame, text="save", command=update_user, width=10)
cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel, width=10)

update_button.pack(side="left", padx=5)
cancel_btn.pack(side="left", padx=5)
root.bind("<Alt-s>", lambda event: save())  # Alt + s shortcut
root.bind("<Alt-c>", lambda event: cancel())  # Alt + c shortcut

# Call fetch_last_entry() when the program starts
fetch_last_entry()
# Start the main loop
root.mainloop() 