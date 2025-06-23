import os
import re
import sys
from tkinter import PhotoImage
import customtkinter as ctk
import numpy as np

# Configure CTk appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.attributes("-topmost", True)
root.title("Circuit Analysis Calculator")
root.geometry("600x900+0+0")

# Set icon
icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception:
        icon = PhotoImage(file=icon_path)
        root.iconphoto(True, icon)

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)

# Globals
matrix_entries, vector_entries = [], []
matrix_frame = vector_frame = result_label = kvl_label = None
precision_var = ctk.StringVar(value="3")

scrollable_frame = ctk.CTkScrollableFrame(root, width=530, height=880)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

def toggle_always_on_top():
    root.attributes("-topmost", topmost_switch.get())

def toggle_theme():
    mode = "dark" if theme_switch.get() else "light"
    ctk.set_appearance_mode(mode)

def solve_linear_system(A, b):
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None

def clear_previous_inputs():
    global matrix_frame, vector_frame, matrix_entries, vector_entries
    for frame in [matrix_frame, vector_frame]:
        if frame: frame.destroy()
    matrix_entries, vector_entries = [], []
    result_label.configure(text="Enter values (real/complex) in matrices and click Solve.")
    kvl_label.configure(text="")

def create_entry(parent, text, row, col):
    entry = ctk.CTkEntry(parent, width=60, placeholder_text=text, justify="center")
    entry.grid(row=row, column=col, padx=5, pady=2)
    return entry

def create_input_fields():
    global matrix_frame, vector_frame, matrix_entries, vector_entries
    try:
        n = int(size_dropdown.get())
        if not 1 <= n <= 4:
            result_label.configure(text="Error: Equations must be 1-4.")
            return
    except ValueError:
        result_label.configure(text="Error: Invalid number.")
        return

    clear_previous_inputs()

    matrix_frame = ctk.CTkFrame(scrollable_frame)
    matrix_frame.pack(pady=10)
    vector_frame = ctk.CTkFrame(scrollable_frame)
    vector_frame.pack(pady=10)

    ctk.CTkLabel(matrix_frame, text=f"Coefficient Matrix A ({n}x{n}):").grid(row=0, column=0, columnspan=n+2, pady=5)
    for i in range(n):
        row_entries = []
        ctk.CTkLabel(matrix_frame, text="[", font=("Courier", 25, "bold"), width=10).grid(row=i+1, column=0)
        for j in range(n):
            row_entries.append(create_entry(matrix_frame, f"A{i+1}{j+1}", i+1, j+1))
        ctk.CTkLabel(matrix_frame, text="]", font=("Courier", 25, "bold"), width=10).grid(row=i+1, column=n+1)
        matrix_entries.append(row_entries)

    ctk.CTkLabel(vector_frame, text=f"Constants Vector b ({n}x1):").grid(row=0, column=0, columnspan=3, pady=5)
    for i in range(n):
        ctk.CTkLabel(vector_frame, text="[", font=("Courier", 25, "bold"), width=10).grid(row=i+1, column=0)
        vector_entries.append(create_entry(vector_frame, f"b{i+1}", i+1, 1))
        ctk.CTkLabel(vector_frame, text="]", font=("Courier", 25, "bold"), width=10).grid(row=i+1, column=2)

def parse_complex(value):
    try:
        val = re.sub(r'\s+', '', value.lower().replace('i', 'j'))
        val = re.sub(r'\bj(\d+)', r'\1j', val)
        val = re.sub(r'\bj\b', '1j', val)
        val = re.sub(r'([+\-])j(\d*)', lambda m: f"{m.group(1)}{m.group(2) or '1'}j", val)
        return complex(val)
    except Exception:
        raise ValueError(f"Invalid complex: {value}")

def solve_and_display():
    try:
        n = len(matrix_entries)
        if n == 0:
            result_label.configure(text="Error: Create input fields first.")
            return

        precision = int(precision_var.get())
        fmt = f".{precision}f"

        A = np.zeros((n, n), dtype=complex)
        b = np.zeros(n, dtype=complex)

        for i in range(n):
            for j in range(n):
                val = matrix_entries[i][j].get()
                A[i, j] = parse_complex(val) if val else 0

        for i in range(n):
            val = vector_entries[i].get()
            b[i] = parse_complex(val) if val else 0

        x = solve_linear_system(A, b)
        if x is None:
            result_label.configure(text="Error: The system has no solution.\n(singular matrix or invalid inputs)")
            kvl_label.configure(text="")
            return

        result_lines = [f"I{i+1} = {x[i].real:.{precision}f} + {x[i].imag:.{precision}f}j A ({np.abs(x[i]):.{precision}f} ∠ {np.degrees(np.angle(x[i])):.{precision}f}° A)" for i in range(n)]
        result_label.configure(text="Solution:\n" + "\n".join(result_lines))

        kvl_lines = []
        for i in range(n):
            terms = []
            for j in range(n):
                coeff = A[i, j]
                if coeff != 0:
                    real, imag = coeff.real, coeff.imag
                    if abs(imag) < 1e-10:
                        term = f"{real:{fmt}} Ω * I{j+1}"
                    elif abs(real) < 1e-10:
                        term = f"{imag:{fmt}}j Ω * I{j+1}"
                    else:
                        term = f"({real:{fmt}} {'+' if imag >= 0 else '-'} {abs(imag):{fmt}}j) Ω * I{j+1}"
                    terms.append(term)
            rhs = b[i]
            rhs_str = f"{rhs.real:{fmt}} {'+' if rhs.imag >= 0 else '-'} {abs(rhs.imag):{fmt}}j" if abs(rhs.imag) >= 1e-10 else f"{rhs.real:{fmt}}"
            kvl_lines.append(" + ".join(terms) + f" = {rhs_str} V")
        kvl_label.configure(text="KVL Equations:\n" + "\n".join(kvl_lines))

    except Exception:
        result_label.configure(text="Error: Invalid input format.")
        kvl_label.configure(text="")

def copy_result_to_clipboard():
    result_text = result_label.cget("text").strip()
    error_indicators = ["Select number", "Error:", "No solution", "Enter values"]
    if not result_text or any(k in result_text for k in error_indicators):
        result_label.configure(text="Error: No solution to copy.")
        return
    kvl_text = kvl_label.cget("text").strip()
    full_text = result_text + ("\n\n" + kvl_text if kvl_text else "")
    root.clipboard_clear()
    root.clipboard_append(full_text)
    root.update()
    result_label.configure(text=result_text + "\n\n✔ Copied to clipboard.")
    root.after(2000, clear_copy_feedback)

def clear_copy_feedback():
    if result_label and "✔ Copied to clipboard." in result_label.cget("text"):
        result_label.configure(text=result_label.cget("text").replace("\n\n✔ Copied to clipboard.", ""))

# GUI Elements
title_label = ctk.CTkLabel(scrollable_frame, text="AC and DC Circuit Analysis Calculator", font=("Franklin Gothic Medium", 20))
title_label.pack(pady=10)

subtitle_label = ctk.CTkLabel(scrollable_frame, text="by Cody Carter and Rohan Patel", font=("Franklin Gothic Medium", 14))
subtitle_label.pack(pady=(0, 5))

switch_frame = ctk.CTkFrame(scrollable_frame)
switch_frame.pack(pady=10)

theme_switch = ctk.CTkSwitch(switch_frame, text="Dark Mode (D)", command=toggle_theme)
theme_switch.pack(side="left", padx=10)
theme_switch.select()

topmost_switch = ctk.CTkSwitch(switch_frame, text="Always on Top (A)", command=toggle_always_on_top)
topmost_switch.pack(side="left", padx=10)
topmost_switch.select()

result_label = ctk.CTkLabel(scrollable_frame, text="Select number of equations and click Set Size", font=("Franklin Gothic Medium", 14))
result_label.pack(pady=10)

kvl_label = ctk.CTkLabel(scrollable_frame, text="", font=("Franklin Gothic Medium", 12), wraplength=500, justify="left")
kvl_label.pack(pady=10)

size_frame = ctk.CTkFrame(scrollable_frame)
size_frame.pack(pady=10)

size_row1 = ctk.CTkFrame(size_frame)
size_row1.pack(pady=5, fill="x")
ctk.CTkLabel(size_row1, text="Number of Equations:", width=150).pack(side="left", padx=(5, 0))
size_dropdown = ctk.CTkOptionMenu(size_row1, values=["1", "2", "3", "4"], width=100)
size_dropdown.set("3")
size_dropdown.pack(side="left", padx=(5, 0))
ctk.CTkButton(size_row1, text="Confirm Matrix Size (R)", command=create_input_fields).pack(side="left", padx=(15, 0))

size_row2 = ctk.CTkFrame(size_frame)
size_row2.pack(pady=5, fill="x")
ctk.CTkLabel(size_row2, text="Decimal Precision:", width=150).pack(side="left", padx=(5, 0))
precision_dropdown = ctk.CTkOptionMenu(size_row2, values=["0", "1", "2", "3", "4", "5", "6"], variable=precision_var, width=100)
precision_dropdown.set("2")
precision_dropdown.pack(side="left", padx=(5, 0))
ctk.CTkButton(size_row2, text="Copy Result to Clipboard (C)", command=copy_result_to_clipboard).pack(side="left", padx=(15, 0))

matrix_frame = ctk.CTkFrame(scrollable_frame)
matrix_frame.pack(pady=10)
vector_frame = ctk.CTkFrame(scrollable_frame)
vector_frame.pack(pady=10)

ctk.CTkButton(scrollable_frame, text="Solve (Enter)", command=solve_and_display).pack(pady=10)
ctk.CTkButton(scrollable_frame, text="Reset (R)", command=create_input_fields).pack(pady=10)

def on_key_press(event):
    match event.keysym.lower():
        case "return" | "kp_enter": solve_and_display()
        case "r" | "R": create_input_fields()
        case "a" | "A": topmost_switch.toggle(); toggle_always_on_top()
        case "d" | "D": theme_switch.toggle(); toggle_theme()
        case "c" | "C": copy_result_to_clipboard()
root.bind("<Key>", on_key_press)

root.mainloop()
