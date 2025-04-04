import mysql.connector
import tkinter as tk
import subprocess 
from tkinter import ttk
from tkinter import messagebox
import json

def open_product(product_data=None):
    """Opens the product item form and ensures updates replace old data in the list."""
    temp_file = "product_temp.json"

    # Save selected supplier data if editing
    if product_data:
        with open(temp_file, "w") as f:
            json.dump(product_data, f)  # Store data in JSON format

        process = subprocess.Popen(["python", "item.py", temp_file])  
        process.wait()
    else:
        process = subprocess.Popen(["python", "item.py"])  # Open blank form for new entry
        process.wait()

    refresh_treeview() # Refresh data after edit
    
# Connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name created earlier
    )

def fetch_product():
    """Fetch product data from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Item, Codeno, Idesc, Unit, Rate FROM item")
    rows = cursor.fetchall()
    conn.close()
    return rows

def refresh_treeview():
    """Refresh TreeView while preventing duplicate entries."""
    existing_products = {tree.item(child)["values"][0]: child for child in tree.get_children()}  # Use Codeno as unique key

    for row in fetch_product():
        product_item = row[0]  # Unique Identifier
        
        if product_item in existing_products:
            # Update existing entry
            tree.item(existing_products[product_item], values=row)
        else:
            # Insert new entry if it doesn't exist
            tree.insert("", "end", values=row)

def on_row_double_click(event):
    """Handles double-click event on a row to open details and update them."""
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]  # Get selected row ID
        values = tree.item(item_id, "values")

        product_data = {
            "item_name": values[0],
            "code": values[1],  # Unique Identifier (Codeno)
            "detail": values[2],
            "unit": values[3],
            "rate": values[4],            
        }
        
        # Remove old entry before opening the edit form
        tree.delete(item_id)
        open_product(product_data)  # Open edit form with data

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
    for row in fetch_product():
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

        product_item = values[0]  # Assuming Orderno is the first column, use it as the identifier
        
        # Ask the user for confirmation
        confirm = messagebox.askyesno("Confirm Deletion",
                                       f" {product_item}exit?")
    if confirm:
        try:
            # Delete from database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM somst WHERE Item = %s", (product_item,))
            conn.commit()

            cursor.execute("DELETE FROM item WHERE Item = %s", (product_item,))
            conn.commit()
            conn.close()
            
            # Remove the row from the Treeview

            tree.delete(item_id)

            # Refresh Treeview to reflect changes
            refresh_treeview() 

            messagebox.showinfo("Deletion Success", f" Do you want to delete {product_item}.")
        except Exception as e:
                conn.rollback()
                messagebox.showerror("Deletion Error", f"Error deleting supplier {product_item}: {str(e)}")       

def back():
    list_window.quit()  # This could be changed to navigate back to another window

def add():
    list_window.quit()

def Delete():
    """Close the supplier list window."""
    delete_selected()   

# Create the main list window
list_window = tk.Tk()
list_window.title("Product Item List")
list_window.geometry("1600x1200")
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

# Add "Back" button in the **top-left corner** using `.place()`
back_btn = tk.Button(list_window, text="Back", command=back, width=10, fg="black")
back_btn.place(x=10, y=10)  # Top-left corner placement

# Bind Alt+B shortcut to Back button
list_window.bind("<Alt-b>", lambda event: back())

# Title Label (Centered)
title_label = tk.Label(top_frame, text="Product item List", font=("Cambria", 25, "bold"), fg="blue")
title_label.pack(side="top", pady=5)

# "Delete" button (Top-right corner)
dlt_btn = tk.Button(top_frame, text="Delete", command=Delete, width=10, fg="black")
dlt_btn.pack(side="right", padx=10)
 # Bind Delete key for convenience
list_window.bind("<Alt-d>", lambda event: delete_selected())
# "Add" button (Top-right corner)
add_btn = tk.Button(top_frame, text="Add", command=open_product, width=10, fg="black")
add_btn.pack(side="right", padx=10)
list_window.bind("<Alt-a>", lambda event: open_product())

# Create a TreeView with a bold heading style
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial",11, "bold"))

tree = ttk.Treeview(
    list_window,
    columns=("item_name", "code", "detail", "unit", "rate"),
    show="headings",
    style="Treeview"
)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Define column headings
columns = ["item_name", "code", "detail", "unit", "rate"]
for col in columns:
    tree.heading(col, text=col)
    if col == "rate":
        tree.column(col, anchor="e", width=120)  # 'e' (east) aligns text to the right
    else:
        tree.column(col, anchor="center", width=120)

# Bind double-click event to open product form with selected data
tree.bind("<Double-1>", on_row_double_click)
# Load initial data into TreeView
refresh_treeview()

# Run tkinter event loop
list_window.mainloop()