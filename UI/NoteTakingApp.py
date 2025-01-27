import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

NOTES_FOLDER = "notes"

# Ensure the folder exists
os.makedirs(NOTES_FOLDER, exist_ok=True)

def load_notes():
    """Load notes from the notes folder and sort by creation datetime."""
    notes = {}
    for file in os.listdir(NOTES_FOLDER):
        if file.endswith(".txt"):
            try:
                # Extract timestamp and title more robustly
                timestamp_part, title_part = file.split("_", 1)
                title = title_part.split(".", 1)[0]  # Remove ".txt" extension
                timestamp = datetime.strptime(timestamp_part, "%Y%m%d%H%M%S")
                with open(os.path.join(NOTES_FOLDER, file), "r") as f:
                    content = f.read()
                notes[file] = {"title": title, "content": content, "timestamp": timestamp}
            except (ValueError, IndexError):
                continue  # Skip invalid files
    return dict(sorted(notes.items(), key=lambda item: item[1]["timestamp"]))

def update_note_list():
    """Update the Listbox to display current notes."""
    note_list.delete(0, tk.END)
    for file, data in notes.items():
        note_list.insert(tk.END, f"{data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {data['title']}")

def create_note():
    open_note_window("Create Note")

def read_note():
    selected = get_selected_note()
    if selected:
        content = notes[selected]["content"]
        messagebox.showinfo("Read Note", f"Content:\n{content}")

def edit_note():
    selected = get_selected_note()
    if selected:
        open_note_window("Edit Note", selected)

def delete_note():
    selected = get_selected_note()
    if selected:
        file_path = os.path.join(NOTES_FOLDER, selected)
        os.remove(file_path)
        notes.pop(selected)
        update_note_list()

def open_note_window(title, note_file=None):
    """Open a window to create or edit a note."""
    window = tk.Toplevel(root)
    window.title(title)

    tk.Label(window, text="Title:").pack()
    title_entry = tk.Entry(window, width=40)
    title_entry.pack(pady=5)
    if note_file:
        title_entry.insert(0, notes[note_file]["title"])

    tk.Label(window, text="Content:").pack()
    content_text = tk.Text(window, width=40, height=10)
    content_text.pack(pady=5)
    if note_file:
        content_text.insert(1.0, notes[note_file]["content"])

    def save_note():
        new_title = title_entry.get().strip()
        content = content_text.get(1.0, tk.END).strip()
        if new_title and content:
            if note_file:  # Editing
                os.remove(os.path.join(NOTES_FOLDER, note_file))
                notes.pop(note_file)
            # Generate new filename with date and time
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_file = f"{timestamp}_{new_title}.txt"
            file_path = os.path.join(NOTES_FOLDER, new_file)
            with open(file_path, "w") as f:
                f.write(content)
            notes[new_file] = {"title": new_title, "content": content, "timestamp": datetime.now()}
            update_note_list()
            window.destroy()
        else:
            messagebox.showerror("Error", "Title and content cannot be empty.")

    tk.Button(window, text="Save", command=save_note).pack(pady=10)

def get_selected_note():
    """Get the selected note file from the listbox."""
    try:
        selected_index = note_list.curselection()[0]
        selected_key = list(notes.keys())[selected_index]
        return selected_key
    except (tk.TclError, IndexError):
        messagebox.showerror("Error", "No note selected.")
        return None

# Initialize the app
root = tk.Tk()
root.title("Note Taking App")
notes = load_notes()

# Create a frame to hold the Listbox and Scrollbar
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

# Listbox and Scrollbar
note_list = tk.Listbox(list_frame, width=60, height=15)
note_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=note_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

note_list.config(yscrollcommand=scrollbar.set)

# Button frame
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Create", command=create_note).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Read", command=read_note).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Edit", command=edit_note).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_note).pack(side=tk.LEFT, padx=5)

update_note_list()
root.mainloop()