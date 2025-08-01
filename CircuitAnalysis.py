import os
import re
import sys
import webbrowser
from tkinter import PhotoImage

import customtkinter as ctk
import numpy as np
from PIL import Image

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)
    
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.attributes("-topmost", True)
root.title("Circuit Analysis Calculator v1.3")
root.geometry("560x900+0+0")

icon_path = "icon.png"
if os.path.exists(icon_path):
    try:
        root.iconbitmap(f"@{icon_path}")
    except Exception as e:
        print(f"Window icon load failed: {e}")

try:
    github_icon_path = resource_path("icon.png")
    print(f"Trying to load GitHub icon from: {github_icon_path}")
    
    github_icon_image = ctk.CTkImage(
        dark_image=Image.open(github_icon_path),
        light_image=Image.open(github_icon_path),
        size=(20, 20)
    )
except Exception as e:
    print(f"Failed to load GitHub icon: {e}")
    github_icon_image = None

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)


matrix_entries, vector_entries = [], []
matrix_frame = vector_frame = None
precision_var = ctk.StringVar(value="3")

scrollable_frame = ctk.CTkScrollableFrame(root, width=530, height=880)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)


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
        if frame: frame.destroy()
    matrix_entries, vector_entries = [], []
    output_textbox.configure(state="normal")
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", "Enter values (real/complex rectangular) in matrices and click Solve.")
    output_textbox.configure(state="disabled")


def create_entry(parent, text, row, col):
    entry = ctk.CTkEntry(parent, width=100, placeholder_text=text, justify="center")
    entry.grid(row=row, column=col, padx=5, pady=2)
    return entry


def create_input_fields():
    global matrix_frame, vector_frame, matrix_entries, vector_entries
    try:
        n = int(size_dropdown.get())
        if not 1 <= n <= 4:
            show_output("Error: Equations must be 1-4.")
            root.bell()
            return
    except ValueError:
        show_output("Error: Invalid number.")
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
        val = val.replace(',', "")
        val = re.sub(r'\s+', '', val)
        val = re.sub(r'(?<![\d.])j(\d+(\.\d+)?)(?![\d.])', r'\1j', val)
        val = re.sub(r'(?<=[\+\-])j(?![\d.])', '1j', val)
        val = re.sub(r'^j$', '1j', val)
        return complex(val)
    except Exception:
        raise ValueError(f"Invalid complex number format: {value}")


def show_output(message):
    output_textbox.configure(state="normal")
    output_textbox.delete("1.0", "end")
    output_textbox.insert("1.0", message)
    output_textbox.configure(state="disabled")


def solve_and_display():
    try:
        n = len(matrix_entries)
        if n == 0:
            show_output("Error: Create input fields first.")
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
            show_output("Error: The system has no solution.\n(singular matrix or invalid inputs)")
            root.bell()
            return

        result_lines = [
            f"I{i + 1} = {x[i].real:.{precision}f} + {x[i].imag:.{precision}f}j A       [ {np.abs(x[i]):.{precision}f} ∠ {np.degrees(np.angle(x[i])):.{precision}f}° A ]"
            for i in range(n)]

        kvl_lines = []
        for i in range(n):
            terms = []
            for j in range(n):
                coeff = A[i, j]
                if coeff != 0:
                    real, imag = coeff.real, coeff.imag
                    if abs(imag) < 1e-10:
                        term = f"{real:{fmt}} Ω * I{j + 1}"
                    elif abs(real) < 1e-10:
                        term = f"{imag:{fmt}}j Ω * I{j + 1}"
                    else:
                        term = f"({real:{fmt}} {'+' if imag >= 0 else '-'} {abs(imag):{fmt}}j) Ω * I{j + 1}"
                    terms.append(term)
            rhs = b[i]
            rhs_str = f"{rhs.real:{fmt}} {'+' if rhs.imag >= 0 else '-'} {abs(rhs.imag):{fmt}}j" if abs(
                rhs.imag) >= 1e-10 else f"{rhs.real:{fmt}}"
            kvl_lines.append(" + ".join(terms) + f" = {rhs_str} V")

        output_textbox.configure(state="normal")
        output_textbox.delete("1.0", "end")
        output_textbox.insert("end", "Solution:\n" + "\n".join(result_lines) + "\n\n")
        output_textbox.insert("end", "KVL Equations:\n" + "\n".join(kvl_lines))
        output_textbox.configure(state="disabled")

    except Exception:
        show_output("Error: Invalid input format.")
        root.bell()


def copy_result_to_clipboard():
    result_text = output_textbox.get("1.0", "end").strip()
    if not result_text or "Error:" in result_text or "Enter values" in result_text:
        show_output("Error: No solution to copy.")
        root.bell()
        return
    root.clipboard_clear()
    root.clipboard_append(result_text)
    root.update()
    output_textbox.configure(state="normal")
    output_textbox.insert("end", "\n\nCopied results to clipboard.")
    output_textbox.configure(state="disabled")
    root.after(1000)


# GUI Elements
ctk.CTkLabel(scrollable_frame, text="AC and DC Circuit Analysis Calculator\n(System of Equations Solver)",
             font=("Franklin Gothic Medium", 20)).pack(pady=10)

ctk.CTkLabel(scrollable_frame, text="by Cody Carter and Rohan Patel",
             font=("Franklin Gothic Medium", 14)).pack(pady=(0, 5))

ctk.CTkButton(scrollable_frame, text="View On GitHub", image=github_icon_image, compound="left",
              command=open_github).pack(pady=5)

switch_frame = ctk.CTkFrame(scrollable_frame)
switch_frame.pack(pady=10)

theme_switch = ctk.CTkSwitch(switch_frame, text="Dark Mode (D)", command=toggle_theme)
theme_switch.pack(side="left", padx=10)
theme_switch.select()

topmost_switch = ctk.CTkSwitch(switch_frame, text="Always on Top (A)", command=toggle_always_on_top)
topmost_switch.pack(side="left", padx=10)
topmost_switch.select()

output_textbox = ctk.CTkTextbox(scrollable_frame, border_width=5, width=500, height=200,
                                font=("Franklin Gothic Medium", 12), wrap="word")
output_textbox.pack(pady=10)
output_textbox.insert("1.0", "Select number of equations and click Confirm Matrix Size.")
output_textbox.configure(state="disabled")

size_frame = ctk.CTkFrame(scrollable_frame)
size_frame.pack(pady=10)

size_row1 = ctk.CTkFrame(size_frame)
size_row1.pack(pady=5, fill="x")
ctk.CTkLabel(size_row1, text="Number of Equations:", width=150).pack(side="left", padx=(5, 0))
size_dropdown = ctk.CTkOptionMenu(size_row1, values=["1", "2", "3", "4"], width=100)
size_dropdown.set("3")
size_dropdown.pack(side="left", padx=(5, 0))
ctk.CTkButton(size_row1, text="    Confirm Matrix Size (R)    ", command=create_input_fields).pack(side="left",
                                                                                                   padx=(15, 0))

size_row2 = ctk.CTkFrame(size_frame)
size_row2.pack(pady=5, fill="x")
ctk.CTkLabel(size_row2, text="Decimal Precision:", width=150).pack(side="left", padx=(5, 0))
precision_dropdown = ctk.CTkOptionMenu(size_row2, values=["0", "1", "2", "3", "4", "5", "6"], variable=precision_var,
                                       width=100)
precision_dropdown.set("2")
precision_dropdown.pack(side="left", padx=(5, 0))
ctk.CTkButton(size_row2, text="Copy Result to Clipboard (C)", command=copy_result_to_clipboard).pack(side="left",
                                                                                                     padx=(15, 0))

matrix_frame = ctk.CTkFrame(scrollable_frame)
matrix_frame.pack(pady=10)
vector_frame = ctk.CTkFrame(scrollable_frame)
vector_frame.pack(pady=10)

button_row = ctk.CTkFrame(scrollable_frame)
button_row.pack(pady=10)

ctk.CTkButton(button_row, text="Solve (Enter)", command=solve_and_display).pack(side="left", padx=10)
ctk.CTkButton(button_row, text="Reset (R)", command=create_input_fields).pack(side="left", padx=10)


def on_key_press(event):
    match event.keysym.lower():
        case "return" | "kp_enter":
            solve_and_display()
        case "r" | "R":
            create_input_fields()
        case "a" | "A":
            topmost_switch.toggle();
            toggle_always_on_top()
        case "d" | "D":
            theme_switch.toggle();
            toggle_theme()
        case "c" | "C":
            copy_result_to_clipboard()


root.bind("<Key>", on_key_press)

root.mainloop()
