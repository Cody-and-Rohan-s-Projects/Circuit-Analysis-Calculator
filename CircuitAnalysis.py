import numpy as np
import customtkinter as ctk
from tkinter import PhotoImage
import os
import re

# Set default appearance and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create main window
root = ctk.CTk()
root.title("Circuit Analysis Calculator")
root.geometry("550x850")

# Set custom window icon
icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
if os.path.exists(icon_path):
    try:
        root.iconbitmap(icon_path)
    except Exception:
        icon = PhotoImage(file=icon_path)
        root.iconphoto(True, icon)

# Global variables to store dynamic entry fields
matrix_entries = []
vector_entries = []
matrix_frame = None
vector_frame = None
result_label = None
kvl_label = None

def toggle_always_on_top():
    root.attributes("-topmost", topmost_switch.get())

def toggle_theme():
    mode = "dark" if theme_switch.get() else "light"
    ctk.set_appearance_mode(mode)

def solve_linear_system(A, b):
    """Solves a system of linear equations Ax = b."""
    try:
        x = np.linalg.solve(A, b)
        return x
    except np.linalg.LinAlgError:
        return None

def clear_previous_inputs():
    """Clear previous matrix and vector input frames."""
    global matrix_frame, vector_frame, matrix_entries, vector_entries
    if matrix_frame is not None:
        matrix_frame.destroy()
    if vector_frame is not None:
        vector_frame.destroy()
    matrix_entries = []
    vector_entries = []
    result_label.configure(text="Enter coefficient values (real or complex rectangular) into the matrices and click Solve")
    kvl_label.configure(text="")

def create_input_fields():
    """Create input fields for matrix A and vector b based on user-specified size."""
    global matrix_frame, vector_frame, matrix_entries, vector_entries
    try:
        n = int(size_dropdown.get())
        if n < 1 or n > 4:
            result_label.configure(text="Error: Number of equations must be between 1 and 4.")
            return
    except ValueError:
        result_label.configure(text="Error: Please select a valid number of equations.")
        return

    clear_previous_inputs()

    # Create new frames
    matrix_frame = ctk.CTkFrame(root)
    matrix_frame.pack(pady=10)
    vector_frame = ctk.CTkFrame(root)
    vector_frame.pack(pady=10)

    # Matrix A label and inputs
    ctk.CTkLabel(matrix_frame, text=f"Coefficient Matrix A ({n}x{n}):").grid(row=0, column=0, columnspan=n, pady=5)
    matrix_entries = []
    for i in range(n):
        row_entries = []
        for j in range(n):
            entry = ctk.CTkEntry(matrix_frame, width=60, placeholder_text=f"A{i+1}{j+1}")
            entry.grid(row=i+1, column=j, padx=5, pady=5)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

    # Vector b label and inputs
    ctk.CTkLabel(vector_frame, text=f"Constants Vector b ({n}x1):").grid(row=0, column=0, pady=5)
    vector_entries = []
    for i in range(n):
        entry = ctk.CTkEntry(vector_frame, width=60, placeholder_text=f"b{i+1}")
        entry.grid(row=i+1, column=0, padx=5, pady=5)
        vector_entries.append(entry)

def parse_complex(value: str) -> complex:
    """
    Parses a string representing a complex number where 'j' or 'i' can be before or after the coefficient.
    """
    try:
        val = value.replace(" ", "").lower().replace("i", "j")

        # Handle cases like 'j4' or 'j4+3' → convert to '4j+3'
        val = re.sub(r'\bj(\d+)', r'\1j', val)
        val = re.sub(r'\b(\d+)j\b', r'\1j', val)  # already valid, keep as-is
        val = re.sub(r'\bj\b', '1j', val)  # lone 'j'

        # Handle cases like '4+j5' or '4+j' → convert to '4+5j' or '4+1j'
        val = re.sub(r'([+\-])j(\d*)', lambda m: f"{m.group(1)}{m.group(2) if m.group(2) else '1'}j", val)

        return complex(val)
    except Exception:
        raise ValueError(f"Invalid complex number format: {value}")

def solve_and_display():
    """Solve the system and display results and KVL equations (supports complex numbers)."""
    try:
        n = len(matrix_entries)
        if n == 0:
            result_label.configure(text="Error: Please create input fields first.")
            return

        # Initialize A and b as complex arrays
        A = np.zeros((n, n), dtype=complex)
        b = np.zeros(n, dtype=complex)

        # Fill A
        for i in range(n):
            for j in range(n):
                val = matrix_entries[i][j].get()
                A[i, j] = parse_complex(val) if val else 0

        # Fill b
        for i in range(n):
            val = vector_entries[i].get()
            b[i] = parse_complex(val) if val else 0

        # Solve system
        x = solve_linear_system(A, b)
        if x is not None:
            result_lines = [f"I{i+1} = {x[i].real:.3f} + {x[i].imag:.3f}j A" for i in range(n)]
            result_text = "Solution:\n" + "\n".join(result_lines)
            result_label.configure(text=result_text)

            # Generate KVL equations
            kvl_equations = []
            for i in range(n):
                terms = []
                for j in range(n):
                    coeff = A[i, j]
                    if coeff != 0:
                        term = f"({coeff.real:.2f}{'+' if coeff.imag >= 0 else '-'}{abs(coeff.imag):.2f}j) Ohms * I{j+1}"
                        terms.append(term)
                rhs = f"{b[i].real:.2f}{'+' if b[i].imag >= 0 else '-'}{abs(b[i].imag):.2f}j"
                equation = " + ".join(terms) + f" = {rhs} Volts"
                kvl_equations.append(equation)
            kvl_label.configure(text="KVL Equations:\n" + "\n".join(kvl_equations))
        else:
            result_label.configure(text="Error: Solution does not exist. (Singular matrix).")
            kvl_label.configure(text="")

    except Exception as e:
        result_label.configure(text="Error: Invalid input. Type a real or complex number such as 3+4j or -5.")
        kvl_label.configure(text="")

# ------------------------- GUI ELEMENTS --------------------------

# Title
title_label = ctk.CTkLabel(root, text="AC and DC Circuit Analysis Calculator", font=("Franklin Gothic Medium", 20))
title_label.pack(pady=10)

# Subtitle
subtitle_label = ctk.CTkLabel(root, text="by Cody Carter and Rohan Patel", font=("Franklin Gothic Medium", 14))
subtitle_label.pack(pady=(0, 5))

# Switches frame (Theme and Always on Top)
switch_frame = ctk.CTkFrame(root)
switch_frame.pack(pady=10)

theme_switch = ctk.CTkSwitch(switch_frame, text="Dark Mode", command=toggle_theme)
theme_switch.pack(side="left", padx=10)

topmost_switch = ctk.CTkSwitch(switch_frame, text="Always on Top", command=toggle_always_on_top)
topmost_switch.pack(side="left", padx=10)

# Result label
result_label = ctk.CTkLabel(root, text="Select number of equations and click Set Size", font=("Franklin Gothic Medium", 14))
result_label.pack(pady=10)

# KVL equations label
kvl_label = ctk.CTkLabel(root, text="", font=("Franklin Gothic Medium", 12), wraplength=580, justify="left")
kvl_label.pack(pady=10)

# Size input with dropdown
size_frame = ctk.CTkFrame(root)
size_frame.pack(pady=10)

ctk.CTkLabel(size_frame, text="Number of Equations:").pack(side="left", padx=5)
size_dropdown = ctk.CTkOptionMenu(size_frame, values=["1", "2", "3", "4"])
size_dropdown.set("3")  # Default
size_dropdown.pack(side="left", padx=5)
size_button = ctk.CTkButton(size_frame, text="Set Size", command=create_input_fields)
size_button.pack(side="left", padx=5)

# Placeholder for matrix and vector frames
matrix_frame = ctk.CTkFrame(root)
matrix_frame.pack(pady=10)
vector_frame = ctk.CTkFrame(root)
vector_frame.pack(pady=10)

# Solve and Reset buttons
solve_button = ctk.CTkButton(root, text="Solve", command=solve_and_display)
solve_button.pack(pady=10)

reset_button = ctk.CTkButton(root, text="Reset", command=create_input_fields)
reset_button.pack(pady=10)

# Start the main loop
root.mainloop()