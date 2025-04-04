import tkinter as tk
import subprocess
from tkinter import  messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
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

        # Check if the user already exists
        cursor.execute("SELECT password FROM login WHERE username = %s", (userlogin,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Authenticate user
            if existing_user[0] == password:  # Checking password match
                messagebox.showinfo("Login Successful", f"Welcome, {userlogin}!")
                conn.close()
                open_main(userlogin)  #  Open menu.py with username
            else:
                messagebox.showerror("Login Failed", "Incorrect password!")
        else:
            messagebox.showerror("Login Failed", "User not found! Please register first.")

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to open menu.py and pass username
def open_main(username):
    """Opens the Main Application with user data."""
    subprocess.Popen(["python", "menu.py", username])  # Pass username to menu.py

# Function to close the application
def cancel():
    root.quit()

# Function to handle Forgot Password
def forgot_password():
    userlogin = simpledialog.askstring("Forgot Password", "Enter your username :")
    
    if not userlogin:
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT email FROM login WHERE username = %s OR email = %s", (userlogin, userlogin))
        user = cursor.fetchone()

        if user:
            # Normally, you would send a reset link to the user's email.
            # For now, we're just simulating it.
            messagebox.showinfo("Password Reset", "A password reset link has been sent to your email!")
        else:
            messagebox.showerror("Error", "User not found. Please check your username.")

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")    

# Create the main window
root = tk.Tk()
root.title("Login Form")
root.geometry("1600x1200")


 #Load and set the background image
bg_image = Image.open( r"c:\Users\patel\OneDrive\Desktop\passed\pass.jpg")  # Replace with your image path
bg_image = bg_image.resize((1600, 1200), Image.ANTIALIAS)  # Resize to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

 #Create a label to hold the background image
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# Username Label and Entry
#tk.Label(root, text="User login").pack(pady=5)
#entry_username = tk.Entry(root)
#entry_username.pack(pady=5)

# Password Label and Entry
#tk.Label(root, text="Password").pack(pady=5)
#entry_password = tk.Entry(root, show="*")  # Mask password input
#entry_password.pack(pady=5)

# Frame for buttons (side by side)
#button_frame = tk.Frame(root)
#button_frame.pack(pady=10)

# Buttons
#tk.Button(button_frame, text="Submit", command=Submit, width=10).pack(side=tk.LEFT, padx=5)
#tk.Button(button_frame, text="Cancel", command=cancel, width=10).pack(side=tk.LEFT, padx=5)
#root.bind("<Alt-s>", lambda event: Submit())  # Alt + s shortcut
#root.bind("<Alt-c>", lambda event: cancel())  # Alt + c shortcut


# Forgot Password clickable label with blue color and underline
#forgot_password_label = tk.Label(root, text="Forgot Password?", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
#forgot_password_label.pack(pady=10)

# Bind the click event for the "Forgot Password?" label
#forgot_password_label.bind("<Button-1>", lambda event: forgot_password())  # Left mouse click event

#root.bind("<Alt-s>", lambda event: Submit())  # Alt + s shortcut
#root.bind("<Alt-c>", lambda event: cancel())  # Alt + c shortcut

# Create a frame to hold the login form and center it
login_frame = tk.Frame(root, bg='white', bd=10)
login_frame.place(relx=0.5, rely=0.5, anchor='center')

# Username Label and Entry
tk.Label(login_frame, text="User login", font=("Arial", 14)).grid(row=0, column=1, pady=10)
entry_username = tk.Entry(login_frame, font=("Arial", 14))
entry_username.grid(row=2, column=1, pady=10)

# Password Label and Entry
tk.Label(login_frame, text="Password", font=("Arial", 14)).grid(row=3, column=1, pady=10)
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 14))  # Mask password input
entry_password.grid(row=4, column=1, pady=10)

# Frame for buttons (side by side)
button_frame = tk.Frame(login_frame)
button_frame.grid(row=5, columnspan=2, pady=10)

# Buttons
tk.Button(button_frame, text="Submit", command=Submit, width=10, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Cancel", command=cancel, width=10, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)


# Forgot Password clickable label with blue color and underline
forgot_password_label = tk.Label(login_frame, text="Forgot Password?", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
forgot_password_label.grid(row=6, columnspan=2, pady=10)  # Place the label below the buttons

# Bind the click event for the "Forgot Password?" label
forgot_password_label.bind("<Button-1>", lambda event: forgot_password())  # Left mouse click event


# Keyboard shortcut bindings
root.bind("<Alt-s>", lambda event: Submit())  # Alt + s shortcut
root.bind("<Alt-c>", lambda event: cancel())  # Alt + c shortcut
root.mainloop()