import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")

cursor.execute("DELETE FROM students")

cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")

conn.commit()


def add_student():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if not name or not age or not course:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a valid number.")
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()

    messagebox.showinfo("Success", "Student added successfully.")
    clear_fields()
    display_students()


def display_students():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:
        tree.insert("", tk.END, values=student)


def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student to update.")
        return

    student_id = tree.item(selected[0])["values"][0]

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if not name or not age or not course:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a valid number.")
        return

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    messagebox.showinfo("Success", "Student updated successfully.")
    clear_fields()
    display_students()


def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student to delete.")
        return

    student_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully.")
        clear_fields()
        display_students()


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


def select_student(event):
    selected = tree.selection()

    if selected:
        student = tree.item(selected[0])["values"]

        clear_fields()
        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])


root = tk.Tk()
root.configure(bg="#102E4A")
root.title("Student Management System")
root.geometry("600x450")
root.resizable(False, False)

frame_form = tk.Frame(root)
frame = tk.Frame(root, bg="green")
frame_form.pack(pady=15)

tk.Label(frame_form, text="Name:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(frame_form, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Age:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
age_entry = tk.Entry(frame_form, width=30)
age_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Course:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
course_entry = tk.Entry(frame_form, width=30)
course_entry.grid(row=2, column=1, padx=10, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add", command=add_student, width=10, bg="#A0C4FF", fg="#1B1B1B").grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update", command=update_student, width=10, bg="#A0C4FF", fg="#1B1B1B").grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete", command=delete_student, width=10, bg="#A0C4FF", fg="#1B1B1B").grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear", command=clear_fields, width=10, bg="#A0C4FF", fg="#1B1B1B").grid(row=0, column=3, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Age", "Course"), show="headings", height=8)
                
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", 
    background="#EE9B00", 
    fieldbackground="#808080", 
    foreground="#1B1B1B"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column("ID", width=50, anchor="center")
tree.column("Name", width=180)
tree.column("Age", width=70, anchor="center")
tree.column("Course", width=180)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", select_student)

display_students()

root.mainloop()

conn.close()
