import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
import os

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def process_file():
    input_path = entry_file.get()
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", "Invalid file path.")
        return

    try:
        df = pd.read_csv(input_path)
        mapping = {
            'First Name': 'firstName',
            'Last Name': 'lastName',
            'Email Address': 'email'
        }
        mapped_df = df.rename(columns=mapping)
        json_data = mapped_df.to_dict(orient='records')
        output_path = os.path.join(os.path.dirname(input_path), "output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        messagebox.showinfo("Success", f"Mapped data saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("CSV Mapper")

tk.Label(root, text="CSV File:").grid(row=0, column=0, padx=5, pady=5)
entry_file = tk.Entry(root, width=40)
entry_file.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text="Process", command=process_file).grid(row=1, column=1, pady=10)

root.mainloop()
