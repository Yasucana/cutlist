import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

TODO_FILE = "todo_list.txt"

# Load tasks from file
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r", encoding="utf-8") as file:
            return [line.strip().split("|") for line in file.readlines()]
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TODO_FILE, "w", encoding="utf-8") as file:
        for task in tasks:
            file.write("|".join(task) + "\n")

# Get current week (e.g., 202342)
def get_current_week():
    today = datetime.now()
    year, week, _ = today.isocalendar()
    return f"{year}{week:02d}"

# Check if the task is currently in progress
def is_current_task(start_week, end_week):
    current_week = get_current_week()
    return start_week <= current_week <= end_week

# Validate week format (yyyyww format)
def validate_week(week):
    try:
        year = int(week[:4])
        week_num = int(week[4:])
        return 1 <= week_num <= 53 and 2000 <= year <= 9999
    except (ValueError, IndexError):
        return False

# Display task list
def show_tasks():
    task_display.delete(1.0, tk.END)
    tasks = load_tasks()
    if not tasks:
        task_display.insert(tk.END, "No tasks yet.\n")
    else:
        task_display.insert(tk.END, "=== Job List ===\n")
        for i, task in enumerate(tasks, 1):
            try:
                job_num, draw_num, rev_num, item_num, item_desc, start_week, end_week = task
                current = " [In Progress]" if is_current_task(start_week, end_week) else ""
                task_display.insert(tk.END, f"{i}. {job_num}, {draw_num}, {rev_num}, {item_num}, {item_desc}, {start_week}, {end_week}{current}\n")
            except ValueError:
                task_display.insert(tk.END, f"Error: Task {i} has incorrect format: {task}\n")
        task_display.insert(tk.END, "====================\n")

# Generate preview
def generate_preview(*args):
    preview_display.delete(1.0, tk.END)
    job_nums = [entry.get().strip() for entry in entries["job"] if entry.get().strip()]
    draw_num = entries["draw"].get().strip()
    rev_num = entries["rev"].get().strip()
    items = [(entries["item"][i].get().strip(), entries["desc"][i].get().strip()) for i in range(10) if entries["item"][i].get().strip() and entries["desc"][i].get().strip()]
    start_week = entries["start"].get().strip()
    end_week = entries["end"].get().strip()

    if not job_nums or not draw_num or not rev_num or not items or not start_week or not end_week:
        return

    if not validate_week(start_week) or not validate_week(end_week) or start_week > end_week:
        preview_display.insert(tk.END, "Invalid week format or start week is after end week.\n")
        return

    preview_display.insert(tk.END, "=== Preview ===\n")
    for job_num in job_nums:
        for item_num, item_desc in items:
            preview_display.insert(tk.END, f"{job_num}, {draw_num}, {rev_num}, {item_num}, {item_desc}, {start_week}, {end_week}\n")
    preview_display.insert(tk.END, "=================\n")

# Add tasks
def add_tasks():
    tasks = load_tasks()
    job_nums = [entry.get().strip() for entry in entries["job"] if entry.get().strip()]
    draw_num = entries["draw"].get().strip()
    rev_num = entries["rev"].get().strip()
    items = [(entries["item"][i].get().strip(), entries["desc"][i].get().strip()) for i in range(10) if entries["item"][i].get().strip() and entries["desc"][i].get().strip()]
    start_week = entries["start"].get().strip()
    end_week = entries["end"].get().strip()

    if not job_nums or not draw_num or not rev_num or not items or not start_week or not end_week:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return

    if not validate_week(start_week) or not validate_week(end_week) or start_week > end_week:
        messagebox.showerror("Error", "Invalid week format or start week is after end week.")
        return

    for job_num in job_nums:
        for item_num, item_desc in items:
            tasks.append([job_num, draw_num, rev_num, item_num, item_desc, start_week, end_week])

    save_tasks(tasks)
    # Clear input fields
    for entry_list in entries["job"]:
        entry_list.delete(0, tk.END)
    entries["draw"].delete(0, tk.END)
    entries["rev"].delete(0, tk.END)
    for i in range(10):
        entries["item"][i].delete(0, tk.END)
        entries["desc"][i].delete(0, tk.END)
    entries["start"].delete(0, tk.END)
    entries["end"].delete(0, tk.END)
    show_tasks()
    generate_preview()  # Clear preview
    messagebox.showinfo("Success", "Tasks added successfully!")

# Delete task
def delete_task():
    try:
        num = int(delete_entry.get()) - 1
        tasks = load_tasks()
        if 0 <= num < len(tasks):
            removed = tasks.pop(num)
            save_tasks(tasks)
            delete_entry.delete(0, tk.END)
            show_tasks()
            messagebox.showinfo("Success", f"Deleted '{removed[0]}'.")
        else:
            messagebox.showerror("Error", "That number does not exist.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number!")

# GUI setup
root = tk.Tk()
root.title("Job Management App")
root.geometry("1200x800")

# Left frame (Input section)
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Job Numbers (5 columns, 2 rows)
tk.Label(left_frame, text="Job Numbers", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=5)
entries = {"job": [], "draw": None, "rev": None, "item": [], "desc": [], "start": None, "end": None}
for i in range(2):
    for j in range(5):
        entry = tk.Entry(left_frame, width=10)
        entry.grid(row=i+1, column=j, padx=5, pady=5)
        entries["job"].append(entry)
        entry.bind("<KeyRelease>", generate_preview)

# Drawing Number and Rev Number (below Job Numbers)
tk.Label(left_frame, text="Drawing Number", font=("Arial", 10, "bold")).grid(row=3, column=0)
entries["draw"] = tk.Entry(left_frame, width=15)
entries["draw"].grid(row=4, column=0, padx=5, pady=5)
entries["draw"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="Rev Number", font=("Arial", 10, "bold")).grid(row=3, column=1)
entries["rev"] = tk.Entry(left_frame, width=15)
entries["rev"].grid(row=4, column=1, padx=5, pady=5)
entries["rev"].bind("<KeyRelease>", generate_preview)

# Starting Week and End Week (to the right of Drawing Number and Rev Number)
tk.Label(left_frame, text="Starting Week (yyyyww)", font=("Arial", 10, "bold")).grid(row=3, column=2)
entries["start"] = tk.Entry(left_frame, width=15)
entries["start"].grid(row=4, column=2, padx=5, pady=5)
entries["start"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="End Week (yyyyww)", font=("Arial", 10, "bold")).grid(row=3, column=3)
entries["end"] = tk.Entry(left_frame, width=15)
entries["end"].grid(row=4, column=3, padx=5, pady=5)
entries["end"].bind("<KeyRelease>", generate_preview)

# Item Numbers and Descriptions (below Drawing Number and Rev Number, 10 items each)
tk.Label(left_frame, text="Item Numbers and Descriptions", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=5)
for i in range(10):
    tk.Label(left_frame, text=f"Item {i+1}").grid(row=6+i, column=0, sticky="e")
    item_entry = tk.Entry(left_frame, width=15)
    item_entry.grid(row=6+i, column=1, padx=5, pady=5)
    entries["item"].append(item_entry)
    item_entry.bind("<KeyRelease>", generate_preview)

    desc_entry = tk.Entry(left_frame, width=25)
    desc_entry.grid(row=6+i, column=2, columnspan=3, padx=5, pady=5)
    entries["desc"].append(desc_entry)
    desc_entry.bind("<KeyRelease>", generate_preview)

# Preview display area (below Item Numbers and Descriptions)
preview_display = scrolledtext.ScrolledText(left_frame, width=60, height=15, font=("Arial", 10))
preview_display.grid(row=16, column=0, columnspan=5, padx=10, pady=10)

# Button area
button_frame = tk.Frame(left_frame)
button_frame.grid(row=17, column=0, columnspan=5, pady=10)
tk.Button(button_frame, text="Add", command=add_tasks, width=10).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update", command=show_tasks, width=10).grid(row=0, column=1, padx=5)

# Delete area
delete_frame = tk.Frame(left_frame)
delete_frame.grid(row=18, column=0, columnspan=5, pady=5)
tk.Label(delete_frame, text="Job number to delete:").grid(row=0, column=0, padx=5)
delete_entry = tk.Entry(delete_frame, width=10)
delete_entry.grid(row=0, column=1, padx=5)
tk.Button(delete_frame, text="Delete", command=delete_task, width=10).grid(row=0, column=2, padx=5)
tk.Button(delete_frame, text="Quit", command=root.quit, width=10).grid(row=0, column=3, padx=5)

# Right frame (Job List, placed to the right of Number and Description)
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

tk.Label(right_frame, text="Job List", font=("Arial", 12, "bold")).grid(row=0, column=0)
task_display = scrolledtext.ScrolledText(right_frame, width=80, height=40, font=("Arial", 10))
task_display.grid(row=1, column=0, padx=10, pady=10)

# Initial display
show_tasks()

root.mainloop()