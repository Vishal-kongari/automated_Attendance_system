import tkinter as tk
from tkinter import messagebox, Toplevel
from tkinter import font
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("C:/Users/Rammohan/projects/face_attendance_system/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://bus-safety-automation-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

# Function to show a custom success dialog
def show_success_message():
    # Create a new window for the success message
    success_window = Toplevel(root)
    success_window.title("Success")
    success_window.geometry("300x150")
    success_window.configure(bg='#dff0d8')  # Light green background

    # Add a label with the success message
    success_label = tk.Label(success_window, text="Data added successfully!", font=("Arial", 16, "bold"), fg="#3c763d",
                             bg='#dff0d8')
    success_label.pack(pady=20)

    # Add a button to close the dialog
    close_button = tk.Button(success_window, text="OK", font=("Arial", 14), bg="#5cb85c", fg="white",
                             command=success_window.destroy)
    close_button.pack(pady=10)

# Function to add data to Firebase
def add_student():
    student_id = student_id_entry.get()
    name = name_entry.get()
    branch = branch_entry.get()
    mobile = mobile_entry.get()
    last_attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if student_id and name and branch and mobile:
        data = {
            student_id: {
                "name": name,
                "branch": branch,
                "mobile": mobile,
                "last_attendance_time": last_attendance_time
            }
        }
        try:
            ref.child(student_id).set(data[student_id])
            show_success_message()
            student_id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            branch_entry.delete(0, tk.END)
            mobile_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Firebase Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please fill all fields!")

# Create the GUI
root = tk.Tk()
root.title("Student Data Entry")

# Set window size and background color
root.geometry("600x400")
root.configure(bg='#f9f9f9')

# Fonts
label_font = font.Font(family="Arial", size=14, weight="bold")
entry_font = font.Font(family="Arial", size=14)
button_font = font.Font(family="Arial", size=16, weight="bold")

# Student ID
tk.Label(root, text="Student ID", font=label_font, bg='#f9f9f9').grid(row=0, column=0, pady=15, padx=15, sticky='w')
student_id_entry = tk.Entry(root, font=entry_font, width=30)
student_id_entry.grid(row=0, column=1, pady=15, padx=15)

# Name
tk.Label(root, text="Name", font=label_font, bg='#f9f9f9').grid(row=1, column=0, pady=15, padx=15, sticky='w')
name_entry = tk.Entry(root, font=entry_font, width=30)
name_entry.grid(row=1, column=1, pady=15, padx=15)

# Branch
tk.Label(root, text="Branch", font=label_font, bg='#f9f9f9').grid(row=2, column=0, pady=15, padx=15, sticky='w')
branch_entry = tk.Entry(root, font=entry_font, width=30)
branch_entry.grid(row=2, column=1, pady=15, padx=15)

# Mobile Number
tk.Label(root, text="Mobile Number", font=label_font, bg='#f9f9f9').grid(row=3, column=0, pady=15, padx=15, sticky='w')
mobile_entry = tk.Entry(root, font=entry_font, width=30)
mobile_entry.grid(row=3, column=1, pady=15, padx=15)

# Submit Button
submit_button = tk.Button(root, text="Add Student", font=button_font, bg='#5cb85c', fg='white', command=add_student)
submit_button.grid(row=4, columnspan=2, pady=30)

# Center all content
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()
