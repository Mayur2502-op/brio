import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Company Title - BrioOrder")  # Window title
root.geometry("400x200")  # Window size

# Add the company title
title_label = tk.Label(
    root, 
    text="BrioOrder",  # Company title
    font=("Arial", 24, "bold"),  # Font style
    fg="blue"  # Font color
)
title_label.pack(pady=50)  # Add spacing around the title

# Run the application
root.mainloop()
