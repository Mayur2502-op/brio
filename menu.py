import tkinter as tk
import subprocess 
from PIL import Image ,ImageTk
    
def open_company():
    """Opens the Company Form."""
    subprocess.Popen(["python", "abb.py"])  # Ensure abb.py is in the same directory or use the full path.
    
def open_supplier():
    """Opens the supplier Form."""
    subprocess.Popen(["python", "list.py"])  # Ensure abb.py is in the same directory or use the full path.
    
def open_product():
    """Opens the product Form."""
    subprocess.Popen(["python", "prolist.py"])  # Ensure abb.py is in the same directory or use the full path.
    
def open_sales_order():
    """Opens the Sales Order Form."""
    subprocess.Popen(["python", "orlist.py"])  # Ensure order.py is in the same directory or use the full path.
    
def open_report():
    """Opens the Report Order Form."""
    subprocess.Popen(["python", "report.py"])  # Ensure order.py is in the same directory or use the full path.
   
def exit_app():
    """Exits the application."""
    root.destroy()

# Main Application Window
root = tk.Tk()
root.title("Main Menu")
root.geometry("1600x1200")

# Header Frame to hold title and image side by side
header_frame = tk.Frame(root)
header_frame.pack(pady=20)

# Title
title_label = tk.Label(header_frame, text="Briosoft", font=("Cambria", 30, "bold"), fg="blue")
title_label.pack(side="right",pady=20)

image_path = r"c:\Users\patel\OneDrive\Desktop\png\brio.jpg"

try:
    # Load and resize the image
    image = Image.open(image_path)
    image = image.resize((200, 150), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    
    # Display image on the right side
    image_label = tk.Label(header_frame, image=photo)
    image_label.pack(side="left")
except Exception as e:
    # Display error message on the right side
    error_label = tk.Label(header_frame, text=f"Error loading image: {e}", fg="red")
    error_label.pack(side="right")
    
# Buttons Frame
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

# Company Form Button
btn_company = tk.Button(buttons_frame, text="Company", font=("Arial", 14), width=20, command=open_company)
btn_company.grid(row=0, column=0, pady=10)
root.bind("<Alt-c>", lambda event: open_company())  # Alt + C shortcut

# Supplier Form Button
btn_supplier = tk.Button(buttons_frame, text="Supplier", font=("Arial", 14), width=20, command=open_supplier)
btn_supplier.grid(row=1, column=0, pady=10)
root.bind("<Alt-s>", lambda event: open_supplier())  # Alt + S shortcut

# product Form Button
btn_product = tk.Button(buttons_frame, text="Product Item", font=("Arial", 14), width=20, command=open_product)
btn_product.grid(row=2, column=0, pady=10)
root.bind("<Alt-p>", lambda event: open_product())  # Alt + P shortcut

# Sales Order Form Button
btn_sales_order = tk.Button(buttons_frame, text="Sales Order", font=("Arial", 14), width=20, command=open_sales_order)
btn_sales_order.grid(row=3, column=0, pady=10)
root.bind("<Alt-o>", lambda event: open_sales_order())  # Alt + O shortcut

# Report Form Button
btn_report = tk.Button(buttons_frame, text="Report", font=("Arial", 14), width=20, command=open_report)
btn_report.grid(row=4, column=0, pady=10)
root.bind("<Alt-r>", lambda event: open_report())  # Alt + R shortcut

# Exit Button
btn_exit = tk.Button(root, text="Exit", font=("Arial", 12,"bold"), width=10, command=exit_app)
btn_exit.pack(pady=20)
root.bind("<Alt-x>", lambda event: exit_app())  # Alt + X shortcut

# Run the Application
root.mainloop()