import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    branch TEXT NOT NULL,
    marks TEXT,
    phone TEXT
)
""")
conn.commit()


# Add student
def add_student():
    name = name_entry.get()
    roll = roll_entry.get()
    branch = branch_entry.get()
    marks = marks_entry.get()
    phone = phone_entry.get()

    if name == "" or roll == "" or branch == "":
        messagebox.showwarning("Warning", "Please enter Name, Roll No and Branch")
        return

    cursor.execute(
        "INSERT INTO students (name, roll_no, branch, marks, phone) VALUES (?, ?, ?, ?, ?)",
        (name, roll, branch, marks, phone)
    )
    conn.commit()

    clear_fields()
    show_students()
    messagebox.showinfo("Success", "Student added successfully!")


# Show students
def show_students():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM students")
    for student in cursor.fetchall():
        table.insert("", tk.END, values=student)


# Search student
def search_student():
    search = search_entry.get()

    for item in table.get_children():
        table.delete(item)

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ?",
        ('%' + search + '%', '%' + search + '%')
    )

    for student in cursor.fetchall():
        table.insert("", tk.END, values=student)


# Delete student
def delete_student():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a student first")
        return

    student = table.item(selected[0])["values"]
    student_id = student[0]

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    show_students()
    messagebox.showinfo("Success", "Student deleted successfully!")


# Clear fields
def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


# Main window
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("900x600")

title = tk.Label(
    root,
    text="Student Record Management System",
    font=("Arial", 22, "bold")
)
title.pack(pady=15)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Roll No").grid(row=0, column=2, padx=5, pady=5)
roll_entry = tk.Entry(input_frame, width=20)
roll_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Branch").grid(row=1, column=0, padx=5, pady=5)
branch_entry = tk.Entry(input_frame, width=20)
branch_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Marks").grid(row=1, column=2, padx=5, pady=5)
marks_entry = tk.Entry(input_frame, width=20)
marks_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Phone").grid(row=2, column=0, padx=5, pady=5)
phone_entry = tk.Entry(input_frame, width=20)
phone_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(
    input_frame,
    text="Add Student",
    command=add_student,
    width=15
).grid(row=2, column=3, pady=10)

# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_student
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=show_students
).pack(side=tk.LEFT, padx=5)

# Table
columns = ("ID", "Name", "Roll No", "Branch", "Marks", "Phone")

table = ttk.Treeview(root, columns=columns, show="headings")

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=130)

table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Delete button
tk.Button(
    root,
    text="Delete Selected Student",
    command=delete_student,
    width=25
).pack(pady=10)

show_students()

root.mainloop()