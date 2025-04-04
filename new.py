import tkinter as tk
from tkinter import messagebox, ttk
import datetime


def calculate_amount(event=None):
    """Calculate Amount when Quantity or Rate is changed."""
    try:
        quantity = float(quantity_entry.get())
        rate = float(rate_entry.get())
        amount = quantity * rate
        amount_entry.delete(0, tk.END)  # Clear existing amount
        amount_entry.insert(0, f"{amount:.2f}")  # Insert the calculated amount
    except ValueError:
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, "0.00")

def add_row():
    """Add a new row to the Treeview."""
    orderno = orderno_entry.get()
    orderdate = orderdate_entry.get()
    supplier = supplier_entry.get()
    sr = sr_entry.get()
    productitem = productitem_entry.get()
    description = description_entry.get()
    unit = unit_entry.get()
    quantity = quantity_entry.get()
    rate = rate_entry.get()
    amount = amount_entry.get()

    # Validate inputs before adding
    if not (orderno and orderdate and supplier and sr and productitem and description and unit and quantity and rate and amount):
        messagebox.showwarning("Input Error", "All fields must be filled out.")
        return
    
    # Add row to Treeview
    tree.insert("", "end", values=(orderno, orderdate, supplier, sr, productitem, description, unit, quantity, rate, amount))
    update_total_order_value()

def edit_row():
    """Edit the selected row in the Treeview."""
    selected_item = tree.selection()
    if selected_item:
        item_id = selected_item[0]
        values = tree.item(item_id, "values")
        
        # Pre-fill entry fields with the selected row data
        orderno_entry.delete(0, tk.END)
        orderno_entry.insert(0, values[0])
        orderdate_entry.delete(0, tk.END)
        orderdate_entry.insert(0, values[1])
        supplier_entry.delete(0, tk.END)
        supplier_entry.insert(0, values[2])
        sr_entry.delete(0, tk.END)
        sr_entry.insert(0, values[3])
        productitem_entry.delete(0, tk.END)
        productitem_entry.insert(0, values[4])
        description_entry.delete(0, tk.END)
        description_entry.insert(0, values[5])
        unit_entry.delete(0, tk.END)
        unit_entry.insert(0, values[6])
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, values[7])
        rate_entry.delete(0, tk.END)
        rate_entry.insert(0, values[8])
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[9])

        # Update the button to save the edited data
        def save_edited_row():
            new_values = (
                orderno_entry.get(),
                orderdate_entry.get(),
                supplier_entry.get(),
                sr_entry.get(),
                productitem_entry.get(),
                description_entry.get(),
                unit_entry.get(),
                quantity_entry.get(),
                rate_entry.get(),
                amount_entry.get()
            )
            tree.item(item_id, values=new_values)  # Update the treeview row
            update_total_order_value()

        save_btn.config(command=save_edited_row)  # Update save button's functionality

def delete_row():
    """Delete the selected row from the Treeview."""
    selected_item = tree.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected row?")
        if confirm:
            tree.delete(selected_item)
            update_total_order_value()

def update_total_order_value():
    """Update the total order value by summing all amounts."""
    total_order_value = 0
    for row in tree.get_children():
        values = tree.item(row)["values"]
        try:
            total_order_value += float(values[9])  # Amount is in the 10th column (index 9)
        except ValueError:
            continue
    total_label.config(text=f"Total Order Value: {total_order_value:.2f}")  # Update total value display

# Initialize the main window
root = tk.Tk()
root.title("Sales Order Form")
root.geometry("900x600")

# Frame 1: Order Info
frame1 = tk.Frame(root)
frame1.pack(fill="x", pady=10)

tk.Label(frame1, text="Order No:", width=15, anchor="w").grid(row=0, column=0, padx=10)
orderno_entry = tk.Entry(frame1, width=20)
orderno_entry.grid(row=0, column=1)

tk.Label(frame1, text="Order Date:", width=15, anchor="w").grid(row=0, column=2, padx=10)
orderdate_entry = tk.Entry(frame1, width=20)
orderdate_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
orderdate_entry.grid(row=0, column=3)

tk.Label(frame1, text="Supplier:", width=15, anchor="w").grid(row=1, column=0, padx=10)
supplier_entry = tk.Entry(frame1, width=20)
supplier_entry.grid(row=1, column=1)

# Frame 2: Item Info
frame2 = tk.Frame(root)
frame2.pack(fill="x", pady=10)

tk.Label(frame2, text="Sr:", width=15, anchor="w").grid(row=0, column=0, padx=10)
sr_entry = tk.Entry(frame2, width=20)
sr_entry.grid(row=0, column=1)

tk.Label(frame2, text="Product Item:", width=15, anchor="w").grid(row=0, column=2, padx=10)
productitem_entry = tk.Entry(frame2, width=20)
productitem_entry.grid(row=0, column=3)

tk.Label(frame2, text="Description:", width=15, anchor="w").grid(row=1, column=0, padx=10)
description_entry = tk.Entry(frame2, width=20)
description_entry.grid(row=1, column=1)

tk.Label(frame2, text="Unit:", width=15, anchor="w").grid(row=1, column=2, padx=10)
unit_entry = tk.Entry(frame2, width=20)
unit_entry.grid(row=1, column=3)

tk.Label(frame2, text="Quantity:", width=15, anchor="w").grid(row=2, column=0, padx=10)
quantity_entry = tk.Entry(frame2, width=20)
quantity_entry.bind("<FocusOut>", calculate_amount)
quantity_entry.grid(row=2, column=1)

tk.Label(frame2, text="Rate:", width=15, anchor="w").grid(row=2, column=2, padx=10)
rate_entry = tk.Entry(frame2, width=20)
rate_entry.bind("<FocusOut>", calculate_amount)
rate_entry.grid(row=2, column=3)

tk.Label(frame2, text="Amount:", width=15, anchor="w").grid(row=3, column=0, padx=10)
amount_entry = tk.Entry(frame2, width=20)
amount_entry.grid(row=3, column=1)

# Frame 3: Total Order Value
frame3 = tk.Frame(root)
frame3.pack(fill="x", pady=10)

total_label = tk.Label(frame3, text="Total Order Value: 0.00", font=("Arial", 14, "bold"))
total_label.pack()

# Buttons: Add, Edit, Delete
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

add_btn = tk.Button(button_frame, text="Add", width=10, command=add_row)
add_btn.grid(row=0, column=0, padx=10)

edit_btn = tk.Button(button_frame, text="Edit", width=10, command=edit_row)
edit_btn.grid(row=0, column=1, padx=10)

delete_btn = tk.Button(button_frame, text="Delete", width=10, command=delete_row)
delete_btn.grid(row=0, column=2, padx=10)

# Treeview to display the order details
tree = ttk.Treeview(root, columns=("Orderno", "Orderdate", "Supplier", "Sr", "Productitem", "Description", "Unit", "Quantity", "Rate", "Amount"), show="headings")
tree.pack(fill="both", expand=True)

# Define column headings
columns = ["Orderno", "Orderdate", "Supplier", "Sr", "Productitem", "Description", "Unit", "Quantity", "Rate", "Amount"]
for col in columns:
    tree.heading(col, text=col)

# Column widths and alignment
numeric_columns = {"Quantity", "Rate", "Amount"}
for col in columns:
    if col in numeric_columns:
        tree.column(col, anchor="e", width=100)
    else:
        tree.column(col, anchor="center", width=100)

# Run the application
root.mainloop()
