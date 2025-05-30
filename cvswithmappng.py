import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

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
        output_dir = os.path.dirname(input_path)
        output_path = os.path.join(output_dir, "output.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        # Create a data map PNG
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.axis('off')
        for i, (src, dst) in enumerate(mapping.items()):
            ax.annotate(
                '', 
                xy=(0.7, 1 - i*0.3), 
                xytext=(0.3, 1 - i*0.3), 
                arrowprops=dict(arrowstyle="->", lw=2)
            )
            ax.text(0.25, 1 - i*0.3, src, va='center', ha='right', fontsize=12, fontweight='bold')
            ax.text(0.75, 1 - i*0.3, dst, va='center', ha='left', fontsize=12, color='blue')
        plt.tight_layout()
        png_path = os.path.join(output_dir, "output_datamap.png")
        plt.savefig(png_path, bbox_inches='tight')
        plt.close(fig)

        messagebox.showinfo("Success", f"Mapped data saved to {output_path}\nData map saved to {png_path}")
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
