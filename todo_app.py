import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import csv

TODO_FILE = "todo_list.txt"
selected_task_index = None

def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r", encoding="utf-8") as file:
            return [line.strip().split("|") for line in file.readlines()]
    return []

def save_tasks(tasks):
    with open(TODO_FILE, "w", encoding="utf-8") as file:
        for task in tasks:
            file.write("|".join(task) + "\n")

def get_current_week():
    today = datetime.now()
    year, week, _ = today.isocalendar()
    return f"{year}{week:02d}"

def is_current_task(start_week, end_week):
    current_week = get_current_week()
    return start_week <= current_week <= end_week

def validate_week(week):
    try:
        year = int(week[:4])
        week_num = int(week[4:])
        return 1 <= week_num <= 53 and 2000 <= year <= 9999
    except (ValueError, IndexError):
        return False

def load_plate_data():
    plate_data = {}
    try:
        with open("plate.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    plate_data[row[0]] = row[1]
    except FileNotFoundError:
        messagebox.showerror("Error", "plate.csv not found!")
    return plate_data

def update_plate(i):
    part_num = entries["part"][i].get().strip()
    plate_data = load_plate_data()
    if part_num in plate_data:
        entries["plate"][i].delete(0, tk.END)
        entries["plate"][i].insert(0, plate_data[part_num])
    else:
        entries["plate"][i].delete(0, tk.END)

def show_tasks():
    for item in task_display.get_children():
        task_display.delete(item)
    tasks = load_tasks()
    sorted_tasks = sorted(enumerate(tasks), key=lambda x: x[1][7])
    for display_index, (original_index, task) in enumerate(sorted_tasks, 1):
        try:
            job_num, draw_num, rev_num, item_num, item_desc, part_num, plate, start_week, end_week = task
            status = "In Progress" if is_current_task(start_week, end_week) else ""
            task_display.insert("", "end", iid=str(original_index), 
                                values=(display_index, job_num, draw_num, rev_num, item_num, 
                                        item_desc, part_num, plate, start_week, end_week, status))
        except ValueError:
            messagebox.showerror("Error", f"Task {original_index+1} has incorrect format: {task}")

def generate_preview(*args):
    preview_display.delete(1.0, tk.END)
    job_nums = [entry.get().strip() for entry in entries["job"] if entry.get().strip()]
    draw_num = entries["draw"].get().strip()
    rev_num = entries["rev"].get().strip()
    items = [(entries["item"][i].get().strip(), entries["desc"][i].get().strip(), 
              entries["part"][i].get().strip(), entries["plate"][i].get().strip()) 
             for i in range(10) if entries["item"][i].get().strip() and entries["desc"][i].get().strip()]
    start_week = entries["start"].get().strip()
    end_week = entries["end"].get().strip()
    if not job_nums or not draw_num or not rev_num or not items or not start_week or not end_week:
        return
    if not validate_week(start_week) or not validate_week(end_week) or start_week > end_week:
        preview_display.insert(tk.END, "Invalid week format or start week is after end week.\n")
        return
    preview_display.insert(tk.END, "=== Preview ===\n")
    for job_num in job_nums:
        for item_num, item_desc, part_num, plate in items:
            preview_display.insert(tk.END, f"{job_num}, {draw_num}, {rev_num}, {item_num}, "
                                          f"{item_desc}, {part_num}, {plate}, {start_week}, {end_week}\n")
    preview_display.insert(tk.END, "=================\n")

def add_tasks():
    tasks = load_tasks()
    job_nums = [entry.get().strip() for entry in entries["job"] if entry.get().strip()]
    draw_num = entries["draw"].get().strip()
    rev_num = entries["rev"].get().strip()
    items = [(entries["item"][i].get().strip(), entries["desc"][i].get().strip(), 
              entries["part"][i].get().strip(), entries["plate"][i].get().strip()) 
             for i in range(10) if entries["item"][i].get().strip() and entries["desc"][i].get().strip()]
    start_week = entries["start"].get().strip()
    end_week = entries["end"].get().strip()
    if not job_nums or not draw_num or not rev_num or not items or not start_week or not end_week:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return
    if not validate_week(start_week) or not validate_week(end_week) or start_week > end_week:
        messagebox.showerror("Error", "Invalid week format or start week is after end week.")
        return
    for job_num in job_nums:
        for item_num, item_desc, part_num, plate in items:
            tasks.append([job_num, draw_num, rev_num, item_num, item_desc, part_num, plate, start_week, end_week])
    save_tasks(tasks)
    for entry_list in entries["job"]:
        entry_list.delete(0, tk.END)
    entries["draw"].delete(0, tk.END)
    entries["rev"].delete(0, tk.END)
    for i in range(10):
        entries["item"][i].delete(0, tk.END)
        entries["desc"][i].delete(0, tk.END)
        entries["part"][i].delete(0, tk.END)
        entries["plate"][i].delete(0, tk.END)
    entries["start"].delete(0, tk.END)
    entries["end"].delete(0, tk.END)
    show_tasks()
    generate_preview()
    messagebox.showinfo("Success", "Tasks added successfully!")

def update_task():
    global selected_task_index
    if selected_task_index is None:
        messagebox.showwarning("Warning", "No task selected for update!")
        return
    tasks = load_tasks()
    if 0 <= selected_task_index < len(tasks):
        job_num = entries["job"][0].get().strip()
        draw_num = entries["draw"].get().strip()
        rev_num = entries["rev"].get().strip()
        item_num = entries["item"][0].get().strip()
        item_desc = entries["desc"][0].get().strip()
        part_num = entries["part"][0].get().strip()
        plate = entries["plate"][0].get().strip()
        start_week = entries["start"].get().strip()
        end_week = entries["end"].get().strip()
        if not all([job_num, draw_num, rev_num, item_num, item_desc, part_num, plate, start_week, end_week]):
            messagebox.showwarning("Warning", "Please fill in all fields!")
            return
        if not validate_week(start_week) or not validate_week(end_week) or start_week > end_week:
            messagebox.showerror("Error", "Invalid week format or start week is after end week.")
            return
        tasks[selected_task_index] = [job_num, draw_num, rev_num, item_num, item_desc, part_num, plate, start_week, end_week]
        save_tasks(tasks)
        show_tasks()
        messagebox.showinfo("Success", "Task updated successfully!")
        task_display.selection_remove(task_display.selection())
        selected_task_index = None
        mode_label.config(text="Add New Tasks")
    else:
        messagebox.showerror("Error", "Selected task index out of range.")

def delete_selected_task():
    global selected_task_index
    if selected_task_index is None:
        messagebox.showwarning("Warning", "No task selected for deletion!")
        return
    tasks = load_tasks()
    if 0 <= selected_task_index < len(tasks):
        removed = tasks.pop(selected_task_index)
        save_tasks(tasks)
        show_tasks()
        messagebox.showinfo("Success", f"Deleted task {selected_task_index + 1}: {removed}")
        task_display.selection_remove(task_display.selection())
        selected_task_index = None
        mode_label.config(text="Add New Tasks")
    else:
        messagebox.showerror("Error", "Selected task index out of range.")

def on_task_select(event):
    global selected_task_index
    selected_items = task_display.selection()
    if selected_items:
        selected_item = selected_items[0]
        original_index = int(selected_item)
        selected_task_index = original_index
        mode_label.config(text=f"Editing Task #{original_index + 1}")
        tasks = load_tasks()
        task = tasks[original_index]
        job_num, draw_num, rev_num, item_num, item_desc, part_num, plate, start_week, end_week = task
        for entry in entries["job"]:
            entry.delete(0, tk.END)
        entries["job"][0].insert(0, job_num)
        entries["draw"].delete(0, tk.END)
        entries["draw"].insert(0, draw_num)
        entries["rev"].delete(0, tk.END)
        entries["rev"].insert(0, rev_num)
        for i in range(10):
            entries["item"][i].delete(0, tk.END)
            entries["desc"][i].delete(0, tk.END)
            entries["part"][i].delete(0, tk.END)
            entries["plate"][i].delete(0, tk.END)
        entries["item"][0].insert(0, item_num)
        entries["desc"][0].insert(0, item_desc)
        entries["part"][0].insert(0, part_num)
        entries["plate"][0].insert(0, plate)
        entries["start"].delete(0, tk.END)
        entries["start"].insert(0, start_week)
        entries["end"].delete(0, tk.END)
        entries["end"].insert(0, end_week)
    else:
        selected_task_index = None
        mode_label.config(text="Add New Tasks")
        for entry_list in entries["job"]:
            entry_list.delete(0, tk.END)
        entries["draw"].delete(0, tk.END)
        entries["rev"].delete(0, tk.END)
        for i in range(10):
            entries["item"][i].delete(0, tk.END)
            entries["desc"][i].delete(0, tk.END)
            entries["part"][i].delete(0, tk.END)
            entries["plate"][i].delete(0, tk.END)
        entries["start"].delete(0, tk.END)
        entries["end"].delete(0, tk.END)

root = tk.Tk()
root.title("Job Management App")
root.geometry("1200x800")

left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10)

mode_label = tk.Label(left_frame, text="Add New Tasks", font=("Arial", 10, "bold"))
mode_label.grid(row=0, column=0, columnspan=5, pady=5)

tk.Label(left_frame, text="Job Numbers", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=5)
entries = {"job": [], "draw": None, "rev": None, "item": [], "desc": [], "part": [], "plate": [], "start": None, "end": None}
for i in range(2):
    for j in range(5):
        entry = tk.Entry(left_frame, width=10)
        entry.grid(row=i+2, column=j, padx=5, pady=5)
        entries["job"].append(entry)
        entry.bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="Drawing Number", font=("Arial", 10, "bold")).grid(row=4, column=0)
entries["draw"] = tk.Entry(left_frame, width=15)
entries["draw"].grid(row=5, column=0, padx=5, pady=5)
entries["draw"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="Rev Number", font=("Arial", 10, "bold")).grid(row=4, column=1)
entries["rev"] = tk.Entry(left_frame, width=15)
entries["rev"].grid(row=5, column=1, padx=5, pady=5)
entries["rev"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="Starting Week (yyyyww)", font=("Arial", 10, "bold")).grid(row=4, column=2)
entries["start"] = tk.Entry(left_frame, width=15)
entries["start"].grid(row=5, column=2, padx=5, pady=5)
entries["start"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="End Week (yyyyww)", font=("Arial", 10, "bold")).grid(row=4, column=3)
entries["end"] = tk.Entry(left_frame, width=15)
entries["end"].grid(row=5, column=3, padx=5, pady=5)
entries["end"].bind("<KeyRelease>", generate_preview)

tk.Label(left_frame, text="Item Numbers, Descriptions, Part Numbers, and Plates", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=5)
for i in range(10):
    tk.Label(left_frame, text=f"Item {i+1}").grid(row=7+i, column=0, sticky="e")
    item_entry = tk.Entry(left_frame, width=15)
    item_entry.grid(row=7+i, column=1, padx=5, pady=5)
    entries["item"].append(item_entry)
    item_entry.bind("<KeyRelease>", generate_preview)

    desc_entry = tk.Entry(left_frame, width=25)
    desc_entry.grid(row=7+i, column=2, padx=5, pady=5)
    entries["desc"].append(desc_entry)
    desc_entry.bind("<KeyRelease>", generate_preview)

    part_entry = tk.Entry(left_frame, width=15)
    part_entry.grid(row=7+i, column=3, padx=5, pady=5)
    entries["part"].append(part_entry)
    part_entry.bind("<KeyRelease>", lambda event, idx=i: update_plate(idx))
    part_entry.bind("<KeyRelease>", generate_preview)

    plate_entry = tk.Entry(left_frame, width=15)
    plate_entry.grid(row=7+i, column=4, padx=5, pady=5)
    entries["plate"].append(plate_entry)
    plate_entry.bind("<KeyRelease>", generate_preview)

preview_display = scrolledtext.ScrolledText(left_frame, width=60, height=15, font=("Arial", 10))
preview_display.grid(row=17, column=0, columnspan=5, padx=10, pady=10)

button_frame = tk.Frame(left_frame)
button_frame.grid(row=18, column=0, columnspan=5, pady=10)
tk.Button(button_frame, text="Add", command=add_tasks, width=10).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Task", command=update_task, width=10).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Refresh", command=show_tasks, width=10).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Delete Selected", command=delete_selected_task, width=10).grid(row=0, column=3, padx=5)

delete_frame = tk.Frame(left_frame)
delete_frame.grid(row=19, column=0, columnspan=5, pady=5)
tk.Button(delete_frame, text="Quit", command=root.quit, width=10).grid(row=0, column=0, padx=5)

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # 変更: sticky="nsew"を追加

tk.Label(right_frame, text="Job List", font=("Arial", 12, "bold")).grid(row=0, column=0)
task_display = ttk.Treeview(right_frame, 
                            columns=("Line", "Job", "Drawing", "Rev", "Item", "Description", 
                                     "Part", "Plate", "Start", "End", "Status"), 
                            show="headings")

task_display.heading("Line", text="Line Number")
task_display.heading("Job", text="Job Number")
task_display.heading("Drawing", text="Drawing Number")
task_display.heading("Rev", text="Rev Number")
task_display.heading("Item", text="Item Number")
task_display.heading("Description", text="Item Description")
task_display.heading("Part", text="Part Number")
task_display.heading("Plate", text="Plate")
task_display.heading("Start", text="Starting Week")
task_display.heading("End", text="End Week")
task_display.heading("Status", text="Status")

# 変更: 各カラムの幅と配置を設定
task_display.column("Line", width=50, anchor="center")
task_display.column("Job", width=100, anchor="w")
task_display.column("Drawing", width=80, anchor="w")
task_display.column("Rev", width=50, anchor="center")
task_display.column("Item", width=40, anchor="center")
task_display.column("Description", width=150, anchor="w")
task_display.column("Part", width=100, anchor="w")
task_display.column("Plate", width=80, anchor="w")
task_display.column("Start", width=80, anchor="center")
task_display.column("End", width=100, anchor="center")
task_display.column("Status", width=100, anchor="center")

# 変更: Treeviewがウィンドウサイズに追従するようにsticky="nsew"を追加
task_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# 変更: フレームの行と列を伸縮可能に設定
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

task_display.bind("<<TreeviewSelect>>", on_task_select)

show_tasks()
root.mainloop()