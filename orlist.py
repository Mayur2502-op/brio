import mysql.connector
import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import messagebox
import json

def open_sales(sales_data=None):
    """Opens the sales form and ensures updates replace old data in the list."""
    temp_file = "sales_temp.json"

    if sales_data:
        with open(temp_file, "w") as f:
            json.dump(sales_data, f)  # Store data in JSON format

        process = subprocess.Popen(["python", "sales.py", temp_file])
        process.wait()
    else:
        process = subprocess.Popen(["python", "sales.py"]) # Open blank form for new entry
        process.wait()

    refresh_treeview()  

def connect_db():
    """Connect to MySQL Database"""
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def fetch_sales():
    """Fetch sales data from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT  Ordno, Orddt, Sname, Sr, Item, Idesc, Unit, Quantity, Rate, Amount, Ordval FROM somst")
    
    rows = cursor.fetchall()
    conn.close()
    return rows

#def refresh_treeview():
 #   """Refresh Treeview with the latest data while keeping existing ones."""
  #  existing_entries = {tree.item(child)["values"][0]: child for child in tree.get_children()}  # Store existing rows by Orderno
    
   # for row in fetch_sales():
    #    orderno = row[0]  # Use Orderno as a unique identifier
        
     #   if orderno in existing_entries:
            # Update existing entry
      #      tree.item(existing_entries[orderno], values=row)
       # else:
            # Add new entry
        #    tree.insert("", "end", values=row)

def refresh_treeview():
    """Refresh Treeview with the latest data while keeping existing ones and calculate total order value."""
    existing_entries = {tree.item(child)["values"][0]: child for child in tree.get_children()}  # Store existing rows by Orderno
    total_order_value = 0  # Variable to accumulate the total order value

    # Clear existing rows
    for row in fetch_sales():
        orderno = row[0]  # Use Orderno as a unique identifier
        
        if orderno in existing_entries:
            # Update existing entry
            tree.item(existing_entries[orderno], values=row)
        else:
            # Add new entry
            tree.insert("", "end", values=row)

        # Add the Total Order Value to the total sum
        total_order_value += row[10]  # Assuming 'Total Order Value' is at index 10 (from the fetch_sales query)

        # Update the total value display
        total_label.config(text=f"Total Order Value: {total_order_value:.2f}")  # Display total value rounded to 2 decimal places

def on_row_double_click(event):
    """Handles double-click event to open details and update them."""
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]  # Get the selected row ID
        values = tree.item(item_id, "values")

          # Convert Orderdate to string if it isn't already
        orderdate = values[1]  # Orderdate is the second column
        sales_data = {
            "id": item_id,  # Store the Treeview item ID
            "Orderno": values[0],
            "Orderdate": orderdate,  # Make sure the date is passed
            "Supplier": values[2],
            "Sr": values[3],
            "Productitem": values[4],
            "Description": values[5],
            "Unit": values[6],
            "Quantity": values[7],  # pass quantity
            "Rate": values[8],      # pass rate
            "Amount": values[9],
            "Total Order Value": values[10],
        }
        tree.delete(item_id)  # Remove old entry before opening the edit form
        open_sales(sales_data)  # Open edit form with data

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
    for row in fetch_sales():
        if any(search_term in str(value).lower() for value in row):
            filtered.append(row)

    # Insert filtered records at the top
    for row in filtered:
        tree.insert("", "end", values=row)        

def delete_selected():
    """Delete the selected row from the Treeview and the database."""
    selected_item = tree.selection()  # Get the selected item in the Treeview
    if selected_item:
        item_id = selected_item[0]  # Get the ID of the selected item
        values = tree.item(item_id, "values")  # Get the values of the selected item

        orderno = values[0]  # Assuming Orderno is the first column, use it as the identifier
        
        # Ask the user for confirmation
        confirm = messagebox.askyesno("Confirm Deletion", f"Do you want to delete  {orderno}?")
        if confirm:
            # Delete from database
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM somst WHERE Ordno = %s", (orderno,))
            conn.commit()
            conn.close()
            
            # Remove the row from the Treeview
            tree.delete(item_id)

            # Refresh Treeview to reflect changes
            refresh_treeview()
def back():
    """Close the supplier list window."""
    list_window.quit()

def Delete():
    """Close the supplier list window."""
    list_window.quit()   

# Create the main window
list_window = tk.Tk()
list_window.title("Supplier List")
list_window.geometry("1530x800")
frame = tk.Frame(list_window)
frame.pack()

# Search Frame for input
search_frame = tk.Frame(list_window)
search_frame.pack(fill="x", pady=5)

search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
search_entry.pack(side="right", padx=5)
# Label on the left side (it will appear first)
tk.Label(search_frame, text="Search", font=("Arial", 12)).pack(side="right", padx=5)  # Label on the left side
search_entry.bind("<KeyRelease>", search_records)  # Call search on key release

# Create a top frame for the title
top_frame = tk.Frame(list_window)
top_frame.pack(fill="x", pady=10)

# "Back" button (Top-left corner)
back_btn = tk.Button(list_window, text="Back", command=back, width=10, fg="black")
back_btn.place(x=10, y=10)
list_window.bind("<Alt-b>", lambda event: back())

# Title Label (Centered)
title_label = tk.Label(top_frame, text="Order List", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="top", pady=5)

# "Delete" button (Top-right corner)
dlt_btn = tk.Button(top_frame, text="Delete", command=Delete, width=10, fg="black")
dlt_btn.pack(side="right", padx=10)
 # Bind Delete key for convenience
list_window.bind("<Alt-d>", lambda event: delete_selected())
# Update Delete button to call delete_selected
dlt_btn.config(command=delete_selected)
# "" button (Top-right corner)
add_btn = tk.Button(top_frame, text="Add", command=lambda: open_sales(), width=10, fg="black")
add_btn.pack(side="right", padx=10)
list_window.bind("<Alt-a>", lambda event: open_sales())

# TreeView Styling
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

# TreeView Setup
tree = ttk.Treeview(
    list_window,
    columns=("Orderno", "Orderdate", "Supplier","Sr","Productitem", "Description", "Unit", 
          "Quantity", "Rate", "Amount","TotalOrderValue"),
    show="headings",
    style="Treeview"
)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Define Column Headings
columns = ["Orderno", "Orderdate", "Supplier","Sr","Productitem","Description", "Unit", 
          "Quantity", "Rate",  "Amount","TotalOrderValue"]
column_widths = [5, 20, 80, 5, 80, 80, 10, 7, 7,10,10]  # Adjust column widths
numeric_columns = {"Orderno","Sr","Quantity", "Rate", "Amount", "TotalOrderValue"}  # Numeric fields that need right alignment

for col in columns:
    tree.heading(col, text=col)
    
    if col in numeric_columns:
        tree.column(col, anchor="e", width=120)  # 'e' aligns text to the right
    else:
        tree.column(col, anchor="center", width=120)  # Center align other text fields
 
# Add a label at the bottom or at the corner of the window to display the total value
total_label = tk.Label(list_window, text="Total Amount: 0.00", font=("Cambria", 12, "bold"))
total_label.pack(side="right", pady=10)  # Position it at the bottom of the window

# Bind double-click event
tree.bind("<Double-1>", on_row_double_click)

# Load initial data
refresh_treeview()

# Run tkinter event loop
list_window.mainloop() 
