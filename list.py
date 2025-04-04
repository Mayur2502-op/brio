import mysql.connector
import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import messagebox
import json

def open_supplier(supplier_data=None):
    """Opens the supplier form and ensures updates replace old data in the list."""
    temp_file = "supplier_temp.json"

    # Save selected supplier data if editing
    if supplier_data:
        with open(temp_file, "w") as f:
            json.dump(supplier_data, f)  

        process = subprocess.Popen(["python", "supp.py", temp_file])
        process.wait()
    else:
        process = subprocess.Popen(["python", "supp.py"])
        process.wait()

    refresh_treeview()  # Refresh data after edit

def connect_db():
    """Connect to MySQL Database"""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )
    

def fetch_suppliers():
    """Fetch supplier data from the database."""
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Add1, Add2, City, Pincode, State, Mobileno, Email, GSTno FROM supplier")
    rows = cursor.fetchall()
    conn.close()
    return rows

def refresh_treeview():
    """Refresh Treeview with the latest data while keeping existing ones."""
    existing_entries = {tree.item(child)["values"][0]: child for child in tree.get_children()}  # Store existing rows by Name
    
    for row in fetch_suppliers():
        name = row[0]  # Use Name as a unique identifier
        
        if name in existing_entries:
            # Update existing entry
            tree.item(existing_entries[name], values=row)
        else:
            # Add new entry
            tree.insert("", "end", values=row)

def search_records(event=None):
    """Filter and display matching supplier records based on search input."""
    search_term = search_entry.get().strip().lower()  # Get search input

    # Clear current Treeview entries
    for item in tree.get_children():
        tree.delete(item)

    if not search_term:
        # If search is empty, show all records
        refresh_treeview()
        return

    # Fetch all suppliers and filter
    filtered = []
    for row in fetch_suppliers():
        if any(search_term in str(value).lower() for value in row):
            filtered.append(row)

    # Insert filtered records at the top
    for row in filtered:
        tree.insert("", "end", values=row)


def on_row_double_click(event):
    """Handles double-click event on a row to open details and update them."""
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]  # Get the selected row ID
        values = tree.item(item_id, "values")
        supplier_data = {
            "id": item_id,  # Store the Treeview item ID
            "Name": values[0],
            "Address1": values[1],
            "Address2": values[2],
            "City": values[3],
            "Pincode": values[4],
            "State": values[5],
            "Mobile": values[6],
            "Email": values[7],
            "GST No": values[8],
        }

        tree.delete(item_id)  # Remove old entry before opening the edit form
        open_supplier(supplier_data)  # Open edit form with data

def delete_selected():
    """Delete the selected row from the Treeview and the database."""
    selected_item = tree.selection()  # Get the selected item in the Treeview
    if selected_item:
        item_id = selected_item[0]  # Get the ID of the selected item
        values = tree.item(item_id, "values")  # Get the values of the selected item

        supplier_name = values[0]  # Assuming Name is the first column, use it as the identifier

        #try:
         #   conn = connect_db()
          #  cursor = conn.cursor()

            # SELECT count(bsno)as totrec FROM `supplier` 
            # Check if supplier exists in 'somst'
           # cursor.execute("SELECT COUNT(*) FROM somst WHERE Sname = %s", (supplier_name,))
            #count = cursor.fetchone()[0]
        #if count > 0:
        # Confirm the deletion with the user
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"  {supplier_name} exit?")
        
        if confirm:
            try:
                # Step 1: Delete entries in the 'somst' table related to this supplier
                conn = connect_db()
                cursor = conn.cursor()

               # conn = connect_db()  # Function to connect to the database
                #cursor = conn.cursor()
                
                # Step 1: Update the count in 'somst' table
                #cursor.execute("""
                 #   SELECT somst
                  ## WHERE Sname = %s AND count > 0
                #""", (supplier_name,))

                cursor.execute("DELETE FROM somst WHERE Sname = %s", (supplier_name,))
                conn.commit()
                
                # Step 2: Delete the supplier from the 'supplier' table
                cursor.execute("DELETE FROM supplier WHERE Name = %s", (supplier_name,))
                conn.commit()
                conn.close()

                # Remove the row from the Treeview (supplier list)
                tree.delete(item_id)

                # Refresh Treeview to reflect changes
                refresh_treeview()

                messagebox.showinfo("Deletion Success", f"Do you want to delete {supplier_name}.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Deletion Error", f"Error deleting supplier {supplier_name}: {str(e)}")
       
def back():
    """Close the supplier list window."""
    list_window.quit()

def Delete():
    """Close the supplier list window."""
    delete_selected()   

# Create the main window
list_window = tk.Tk()
list_window.title("Supplier List")
list_window.geometry("1600x1200")

# Search Frame for input
search_frame = tk.Frame(list_window)
search_frame.pack(fill="x", pady=5)

# Entry box on the right side
search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
search_entry.pack(side="right", padx=5)  # Entry box on the right side (next to the label)
# Label on the left side (it will appear first)
tk.Label(search_frame, text="Search", font=("Arial", 12)).pack(side="right", padx=5)  # Label on the left side

search_entry.bind("<KeyRelease>", search_records)  # Call search on key release

# Top Frame for Title & Buttons
top_frame = tk.Frame(list_window)
top_frame.pack(fill="x", pady=10)

# "Back" button (Top-left corner)
back_btn = tk.Button(list_window, text="Back", command=back, width=10, fg="black")
back_btn.place(x=10, y=10)
list_window.bind("<Alt-b>", lambda event: back())

# Title Label (Centered)
title_label = tk.Label(top_frame, text="Supplier List", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="top", pady=5)

# "Delete" button (Top-right corner)
dlt_btn = tk.Button(top_frame, text="Delete", command=Delete, width=10, fg="black")
dlt_btn.pack(side="right", padx=10)
 # Bind Delete key for convenience
list_window.bind("<Alt-d>", lambda event: delete_selected())

# "Add" button (Top-right corner)
add_btn = tk.Button(top_frame, text="Add", command=lambda: open_supplier(), width=10, fg="black")
add_btn.pack(side="right", padx=10)
list_window.bind("<Alt-a>", lambda event: open_supplier())

# TreeView Styling
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# TreeView Setup
tree = ttk.Treeview(
    list_window,
    columns=("Name", "Address1", "Address2", "City", "Pincode", "State", "Mobile", "Email", "GST No"),
    show="headings",
    style="Treeview"
)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Define Column Headings
columns = ["Name", "Address1", "Address2", "City", "Pincode", "State", "Mobile", "Email", "GST No"]
column_widths = [150, 120, 120, 100, 80, 100, 120, 180, 120]  # Adjust column widths

for col, width in zip(columns, column_widths):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=width)

# Bind double-click event
tree.bind("<Double-1>", on_row_double_click)

# Load initial data
refresh_treeview()

# Run tkinter event loop
list_window.mainloop() 