import os
import re
import sys
import webbrowser
import traceback
from tkinter import PhotoImage
from PIL import Image

import customtkinter as ctk
import numpy as np

# ------------------ UTILITIES ------------------
def resource_path(relative_path):
    try:
        # For PyInstaller temporary folder
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        # For running directly
        return os.path.join(os.path.abspath("."), relative_path)

# ------------------ CONFIGURE GUI ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.attributes("-topmost", True)
root.title("Circuit Analysis Calculator v1.2")
root.geometry("560x800+0+0")

# ------------------ ICON SETUP ------------------
icon_png_path = resource_path("icon.png")
print(f"Loading icon for title bar from: {icon_png_path}")
if os.path.exists(icon_png_path):
    try:
        icon = PhotoImage(file=icon_png_path)
        root.iconphoto(True, icon)
        print("Window icon loaded.")
    except Exception as e:
        print(f"Failed to load window icon: {e}")

# ------------------ GITHUB BUTTON IMAGE ------------------
try:
    github_icon_image = ctk.CTkImage(
        dark_image=Image.open(icon_png_path),
        light_image=Image.open(icon_png_path),
        size=(20, 20)
    )
    print("GitHub button icon loaded successfully.")
except Exception as e:
    github_icon_image = None
    print(f"Failed to load GitHub icon: {e}")

# ------------------ GLOBALS ------------------
matrix_entries, vector_entries = [], []
matrix_frame = vector_frame = result_label = kvl_label = None
precision_var = ctk.StringVar(value="3")

scrollable_frame = ctk.CTkScrollableFrame(root, width=530, height=880)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

# ------------------ FUNCTIONS ------------------
def open_github():
    webbrowser.open_new("https://github.com/Cody-and-Rohan-s-Projects/Circuit-Analyser")

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
        if frame:
            frame.destroy()
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
            root.bell()
            return
    except ValueError:
        result_label.configure(text="Error: Invalid number.")
        root.bell()
        return

    clear_previous_inputs()

    matrix_frame = ctk.CTkFrame(scrollable_frame)
    matrix_frame.pack(pady=10)
    vector_frame = ctk.CTkFrame(scrollable_frame)
    vector_frame.pack(pady=10)

    ctk.CTkLabel(matrix_frame, text=f"Coefficient Matrix A ({n}x{n}):").grid(row=0, column=0, columnspan=n + 2, pady=5)
    for i in range(n):
        row_entries = []
        ctk.CTkLabel(matrix_frame, text="[", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=0)
        for j in range(n):
            row_entries.append(create_entry(matrix_frame, f"A{i + 1}{j + 1}", i + 1, j + 1))
        ctk.CTkLabel(matrix_frame, text="]", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=n + 1)
        matrix_entries.append(row_entries)

    ctk.CTkLabel(vector_frame, text=f"Constants Vector b ({n}x1):").grid(row=0, column=0, columnspan=3, pady=5)
    for i in range(n):
        ctk.CTkLabel(vector_frame, text="[", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=0)
        vector_entries.append(create_entry(vector_frame, f"b{i + 1}", i + 1, 1))
        ctk.CTkLabel(vector_frame, text="]", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=2)

def parse_complex(value):
    try:
        val = value.lower().replace('i', 'j')
        val = re.sub(r'\s+', '', val)
        val = re.sub(r'(?<![\d.])j(\d+(\.\d+)?)(?![\d.])', r'\1j', val)
        val = re.sub(r'(?<=[\+\-])j(?![\d.])', '1j', val)
        val = re.sub(r'^j$', '1j', val)
        return complex(val)
    except Exception:
        raise ValueError(f"Invalid complex number format: {value}")

def solve_and_display():
    try:
        n = len(matrix_entries)
        if n == 0:
            result_label.configure(text="Error: Create input fields first.")
            root.bell()
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
            root.bell()
            kvl_label.configure(text="")
            return

        result_lines = [
            f"I{i + 1} = {x[i].real:.{precision}f} + {x[i].imag:.{precision}f}j A       [ {np.abs(x[i]):.{precision}f} ∠ {np.degrees(np.angle(x[i])):.{precision}f}° A ]"
            for i in range(n)]
        result_label.configure(text="Solution:\n" + "\n".join(result_lines))

    except Exception:
        result_label.configure(text="Error: Invalid input format.")
        root.bell()

def copy_result_to_clipboard():
    result_text = result_label.cget("text").strip()
    if not result_text or "Error:" in result_text:
        result_label.configure(text="Error: No solution to copy.")
        root.bell()
        return
    root.clipboard_clear()
    root.clipboard_append(result_text)
    root.update()
    result_label.configure(text=result_text + "\n\nCopied results to clipboard.")
    root.after(1000)

# ------------------ GUI ELEMENTS ------------------
title_label = ctk.CTkLabel(scrollable_frame, text="AC and DC Circuit Analysis Calculator\n(System of Equations Solver)", font=("Franklin Gothic Medium", 20))
title_label.pack(pady=10)

subtitle_label = ctk.CTkLabel(scrollable_frame, text="by Cody Carter and Rohan Patel", font=("Franklin Gothic Medium", 14))
subtitle_label.pack(pady=(0, 5))

github_button = ctk.CTkButton(scrollable_frame, text="View On GitHub", image=github_icon_image, compound="left", command=open_github)
github_button.pack(pady=5)

switch_frame = ctk.CTkFrame(scrollable_frame)
switch_frame.pack(pady=10)

theme_switch = ctk.CTkSwitch(switch_frame, text="Dark Mode (D)", command=toggle_theme)
theme_switch.pack(side="left", padx=10)
theme_switch.select()

topmost_switch = ctk.CTkSwitch(switch_frame, text="Always on Top (A)", command=toggle_always_on_top)
topmost_switch.pack(side="left", padx=10)
topmost_switch.select()

result_label = ctk.CTkLabel(scrollable_frame, text="Select number of equations and click Set Size.", font=("Franklin Gothic Medium", 14))
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
ctk.CTkButton(size_row1, text="    Confirm Matrix Size (R)    ", command=create_input_fields).pack(side="left", padx=(15, 0))

ctk.CTkButton(scrollable_frame, text="Solve (Enter)", command=solve_and_display).pack(pady=10)
ctk.CTkButton(scrollable_frame, text="Copy Result to Clipboard (C)", command=copy_result_to_clipboard).pack(pady=5)

# ------------------ KEY BINDINGS ------------------
def on_key_press(event):
    match event.keysym.lower():
        case "return" | "kp_enter":
            solve_and_display()
        case "r":
            create_input_fields()
        case "a":
            topmost_switch.toggle()
            toggle_always_on_top()
        case "d":
            theme_switch.toggle()
            toggle_theme()
        case "c":
            copy_result_to_clipboard()

root.bind("<Key>", on_key_press)

root.mainloop()
