import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ----------------

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


# ---------------- FUNCTIONS ----------------

def add_student():
    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    branch = branch_entry.get().strip()
    marks = marks_entry.get().strip()
    phone = phone_entry.get().strip()

    if name == "" or roll_no == "" or branch == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter Name, Roll No and Branch."
        )
        return

    cursor.execute("""
        INSERT INTO students
        (name, roll_no, branch, marks, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (name, roll_no, branch, marks, phone))

    conn.commit()

    clear_fields()
    show_students()

    messagebox.showinfo(
        "Success",
        "Student record added successfully!"
    )


def show_students():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM students")

    records = cursor.fetchall()

    for student in records:
        table.insert("", tk.END, values=student)

    count_label.config(
        text=f"Total Students: {len(records)}"
    )


def search_student():
    search_text = search_entry.get().strip()

    if search_text == "":
        show_students()
        return

    for item in table.get_children():
        table.delete(item)

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
        OR branch LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    records = cursor.fetchall()

    for student in records:
        table.insert("", tk.END, values=student)

    count_label.config(
        text=f"Search Results: {len(records)}"
    )


def delete_student():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table."
        )
        return

    student = table.item(selected[0])["values"]

    student_id = student[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        show_students()

        messagebox.showinfo(
            "Deleted",
            "Student record deleted successfully!"
        )


def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def on_close():
    conn.close()
    root.destroy()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Student Record Management System")
root.geometry("1050x650")
root.minsize(900, 550)

root.configure(bg="#f4f6f8")


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg="#1f2937",
    height=80
)

header.pack(fill="x")

title_label = tk.Label(
    header,
    text="Student Record Management System",
    font=("Arial", 24, "bold"),
    bg="#1f2937",
    fg="white"
)

title_label.pack(pady=(15, 0))

subtitle_label = tk.Label(
    header,
    text="Manage student information easily",
    font=("Arial", 11),
    bg="#1f2937",
    fg="#d1d5db"
)

subtitle_label.pack()


# ---------------- INPUT FRAME ----------------

form_frame = tk.LabelFrame(
    root,
    text=" Student Information ",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    padx=15,
    pady=15
)

form_frame.pack(
    fill="x",
    padx=25,
    pady=20
)


# Name

tk.Label(
    form_frame,
    text="Student Name",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# Roll Number

tk.Label(
    form_frame,
    text="Roll Number",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
).grid(row=0, column=2, padx=10, pady=8, sticky="w")

roll_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

roll_entry.grid(
    row=0,
    column=3,
    padx=10,
    pady=8
)


# Branch

tk.Label(
    form_frame,
    text="Branch",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

branch_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

branch_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# Marks

tk.Label(
    form_frame,
    text="Marks",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
).grid(row=1, column=2, padx=10, pady=8, sticky="w")

marks_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

marks_entry.grid(
    row=1,
    column=3,
    padx=10,
    pady=8
)


# Phone

tk.Label(
    form_frame,
    text="Phone",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    width=25,
    font=("Arial", 11)
)

phone_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# Add Button

add_button = tk.Button(
    form_frame,
    text="＋ Add Student",
    command=add_student,
    font=("Arial", 10, "bold"),
    width=18,
    cursor="hand2"
)

add_button.grid(
    row=2,
    column=3,
    padx=10,
    pady=8
)


# ---------------- SEARCH FRAME ----------------

search_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

search_frame.pack(
    fill="x",
    padx=25,
    pady=5
)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 11, "bold"),
    bg="#f4f6f8"
).pack(side="left")


search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11)
)

search_entry.pack(
    side="left",
    padx=10
)


tk.Button(
    search_frame,
    text="🔍 Search",
    command=search_student,
    width=12,
    cursor="hand2"
).pack(side="left", padx=5)


tk.Button(
    search_frame,
    text="Show All",
    command=show_students,
    width=12,
    cursor="hand2"
).pack(side="left", padx=5)


tk.Button(
    search_frame,
    text="Clear",
    command=clear_fields,
    width=10,
    cursor="hand2"
).pack(side="left", padx=5)


# ---------------- TABLE ----------------

table_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


columns = (
    "ID",
    "Name",
    "Roll No",
    "Branch",
    "Marks",
    "Phone"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=150,
        anchor="center"
    )


table.column(
    "ID",
    width=60
)


table.pack(
    fill="both",
    expand=True
)


# ---------------- DELETE BUTTON ----------------

delete_button = tk.Button(
    root,
    text="🗑 Delete Selected Student",
    command=delete_student,
    font=("Arial", 10, "bold"),
    width=25,
    cursor="hand2"
)

delete_button.pack(
    pady=5
)


# ---------------- FOOTER ----------------

count_label = tk.Label(
    root,
    text="Total Students: 0",
    font=("Arial", 10, "bold"),
    bg="#f4f6f8"
)

count_label.pack(
    pady=(5, 12)
)


# ---------------- START ----------------

show_students()

root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)

root.mainloop()