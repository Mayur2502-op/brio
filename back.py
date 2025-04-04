import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Use Pillow for better image handling
import subprocess
import mysql.connector

# Function to connect to MySQL Database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="briodata"  # Database name
    )

# Function to authenticate and save user
def Submit():
    userlogin = entry_username.get().strip()
    password = entry_password.get().strip()

    if not userlogin or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT password FROM login WHERE username = %s", (userlogin,))
        existing_user = cursor.fetchone()

        if existing_user:
            if existing_user[0] == password:
                messagebox.showinfo("Login Successful", f"Welcome, {userlogin}!")
                conn.close()
                open_main(userlogin)
            else:
                messagebox.showerror("Login Failed", "Incorrect password!")
        else:
            messagebox.showerror("Login Failed", "User not found! Please register first.")

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to open menu.py and pass username
def open_main(username):
    subprocess.Popen(["python", "menu.py", username])

# Function to close the application
def cancel():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("1600x1200")

# Load and set the background logo
try:
    background_image = Image.open(r"c:\Users\patel\OneDrive\Desktop\png\brio.jpg")  # Replace 'logo.png' with your image path
    background_image = background_image.resize((700, 700), Image.ANTIALIAS)
    bg_img = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(root, image=bg_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Image Error", f"Error loading background image: {e}")

# Frame for the login form
form_frame = tk.Frame(root, bg="white", padx=20, pady=20)
form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

tk.Label(form_frame, text="User login", font=("Arial", 14), bg="white").pack(pady=5)
entry_username = tk.Entry(form_frame, font=("Arial", 12))
entry_username.pack(pady=5)

tk.Label(form_frame, text="Password", font=("Arial", 14), bg="white").pack(pady=5)
entry_password = tk.Entry(form_frame, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

button_frame = tk.Frame(form_frame, bg="white")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Submit", command=Submit, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Cancel", command=cancel, width=10).pack(side=tk.LEFT, padx=5)

# Keyboard shortcuts
root.bind("<Alt-s>", lambda event: Submit())
root.bind("<Alt-c>", lambda event: cancel())

root.mainloop()





def add_new_row(event=None):
    # Get the current row count (it will increment each time you add a new row)
    row_count = len(product_entries) + 1

    # Create new entry widgets for the next row
    sr_entry_new = tk.Entry(product_frame, width=5, justify="right")
    product_item_entry_new = tk.Entry(product_frame, width=40)
    description_entry_new = tk.Entry(product_frame, width=40)
    unit_entry_new = tk.Entry(product_frame, width=5)
    quantity_entry_new = tk.Entry(product_frame, width=12, justify="right")
    rate_entry_new = tk.Entry(product_frame, width=12, justify="right")
    amount_entry_new = tk.Entry(product_frame, width=12, justify="right")
    
    # Place these widgets in a new row dynamically
    sr_entry_new.grid(row=row_count, column=0, padx=5)
    product_item_entry_new.grid(row=row_count, column=1, padx=5)
    description_entry_new.grid(row=row_count, column=2, padx=5)
    unit_entry_new.grid(row=row_count, column=3, padx=5)
    quantity_entry_new.grid(row=row_count, column=4, padx=5)
    rate_entry_new.grid(row=row_count, column=5, padx=5)
    amount_entry_new.grid(row=row_count, column=6, padx=5)

    # Store the new entry widgets in a list so we can access them later
    product_entries.append([sr_entry_new, product_item_entry_new, description_entry_new, 
                            unit_entry_new, quantity_entry_new, rate_entry_new, amount_entry_new])

    # Bind the new row quantity and rate fields to update the amount
    quantity_entry_new.bind("<KeyRelease>", calculate_amount)
    rate_entry_new.bind("<KeyRelease>", calculate_amount)


# Initialize an empty list to keep track of product rows dynamically
product_entries = []

# Add the initial row (row 1)
add_new_row()

# Bind the Enter key to add a new row
root.bind("<Return>", add_new_row)

