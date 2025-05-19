import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from tkinter import ttk
import polars as pl
import os
import time
import threading  # threading for async execution

# --- Folder selection logic ---

def select_input_folder():
    folder = filedialog.askdirectory(title="Select CSV Folder")
    if folder:
        input_var.set(folder)
        refresh_file_list(folder)

def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_var.set(folder)

# --- File list refresh after selecting folder ---

def refresh_file_list(folder):
    file_listbox.delete(0, tk.END)
    try:
        files = [f for f in os.listdir(folder) if f.endswith(".csv")]
        if not files:
            file_listbox.insert(tk.END, "No CSV files found.")
        else:
            for file in files:
                file_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read folder:\n{str(e)}")

# --- Show CSV preview on file click ---

def show_preview(event):
    selection = file_listbox.curselection()
    if not selection:
        return

    filename = file_listbox.get(selection[0])
    folder = input_var.get()
    file_path = os.path.join(folder, filename)

    try:
        df = pl.read_csv(file_path)
        preview_rows = df.head(5).to_pandas().to_string(index=False)
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, f"Preview of '{filename}':\n\n{preview_rows}")
    except Exception as e:
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, f"Failed to load preview:\n{str(e)}")

# --- Start conversion in a background thread ---

def start_conversion_thread():
    thread = threading.Thread(target=convert_csv_to_parquet)
    thread.start()

# --- CSV to Parquet conversion logic ---

def convert_csv_to_parquet():
    input_folder = input_var.get()
    output_folder = output_var.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders.")
        return

    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    total_files = len(csv_files)

    if total_files == 0:
        messagebox.showwarning("No Files", "No CSV files found in the selected folder.")
        return

    # Helper to safely update UI from the background thread
    def safe_gui_update(func):
        root.after(0, func)

    safe_gui_update(lambda: progress_bar.config(maximum=total_files))
    safe_gui_update(lambda: progress_bar.config(value=0))
    safe_gui_update(root.update_idletasks)

    start_time = time.time()  # start timer

    for index, csv_file in enumerate(csv_files, start=1):
        csv_path = os.path.join(input_folder, csv_file)
        base_name = os.path.splitext(csv_file)[0]
        parquet_path = os.path.join(output_folder, base_name + ".parquet")

        try:
            df = pl.read_csv(csv_path)
            df.write_parquet(parquet_path)
        except Exception as e:
            safe_gui_update(lambda: messagebox.showerror("Conversion Error", f"Failed to convert {csv_file}.\n\n{str(e)}"))
            return

        # Update progress bar and label
        safe_gui_update(lambda i=index: progress_bar.config(value=i))
        safe_gui_update(lambda i=index: progress_label.config(text=f"{i}/{total_files} files converted"))
        safe_gui_update(root.update_idletasks)

    elapsed = round(time.time() - start_time, 2)  # end timer

    safe_gui_update(lambda: messagebox.showinfo("Success", f"All CSV files converted to Parquet in:\n{output_folder}\n\nTotal time: {elapsed} seconds"))
    safe_gui_update(lambda: progress_label.config(text=f"Done! Time taken: {elapsed} sec"))

# --- GUI SETUP ---

root = tk.Tk()
root.title("CSV to Parquet Converter (Threaded)")
root.geometry("700x550")
root.resizable(False, False)

input_var = tk.StringVar()
output_var = tk.StringVar()

# Input folder selection
tk.Label(root, text="CSV Folder:").pack(pady=(10, 0))
tk.Entry(root, textvariable=input_var, width=80).pack(pady=2)
tk.Button(root, text="Select CSV Folder", command=select_input_folder).pack()

# CSV file list display
tk.Label(root, text="CSV Files in Folder:").pack(pady=(10, 0))
frame_list = tk.Frame(root)
frame_list.pack(pady=2)

file_listbox = Listbox(frame_list, height=5, width=60)
file_listbox.pack(side=tk.LEFT, padx=5)
file_listbox.bind("<<ListboxSelect>>", show_preview)

scrollbar = Scrollbar(frame_list, orient="vertical", command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
file_listbox.config(yscrollcommand=scrollbar.set)

# Output folder selection
tk.Label(root, text="Output Parquet Folder:").pack(pady=(10, 0))
tk.Entry(root, textvariable=output_var, width=80).pack(pady=2)
tk.Button(root, text="Select Output Folder", command=select_output_folder).pack()

# Convert button
tk.Button(root, text="Convert All to Parquet", command=start_conversion_thread, bg="#4CAF50", fg="white", height=2).pack(pady=10)

# Progress bar and label
progress_bar = ttk.Progressbar(root, length=600, mode="determinate")
progress_bar.pack(pady=(5, 0))

progress_label = tk.Label(root, text="Progress will be shown here.")
progress_label.pack(pady=(2, 10))

# CSV preview area
tk.Label(root, text="CSV Preview:").pack()
preview_text = tk.Text(root, height=10, width=90)
preview_text.pack(pady=5)

# Start GUI loop
root.mainloop()
