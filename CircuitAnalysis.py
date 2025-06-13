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
root.geometry("600x900")

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
precision_var = ctk.StringVar(value="3")  # Default precision

# Create a scrollable frame as the main container
scrollable_frame = ctk.CTkScrollableFrame(root, width=530, height=880)  # Adjust size to fit window
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

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
    result_label.configure(text="Enter values (can be either real or complex rectangular)\ninto the matrices and click Solve or press the Enter key.")
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

    # Create new frames inside scrollable_frame
    matrix_frame = ctk.CTkFrame(scrollable_frame)
    matrix_frame.pack(pady=10)
    vector_frame = ctk.CTkFrame(scrollable_frame)
    vector_frame.pack(pady=10)

    # Matrix A label and inputs
    ctk.CTkLabel(matrix_frame, text=f"Coefficient Matrix A ({n}x{n}):").grid(row=0, column=0, columnspan=n + 2, pady=5)
    matrix_entries = []
    for i in range(n):
        row_entries = []
        # Left bracket
        ctk.CTkLabel(matrix_frame, text="[", font=("Courier", 25,"bold"), width=10).grid(row=i + 1, column=0, padx=(5, 0))
        # Matrix entries
        for j in range(n):
            entry = ctk.CTkEntry(matrix_frame, width=60, placeholder_text=f"A{i + 1}{j + 1}", justify="center")
            entry.grid(row=i + 1, column=j + 1, padx=5, pady=2)
            row_entries.append(entry)
        # Right bracket
        ctk.CTkLabel(matrix_frame, text="]", font=("Courier", 25,"bold"), width=10).grid(row=i + 1, column=n + 1, padx=(0, 5))
        matrix_entries.append(row_entries)

    # Vector b label and inputs with brackets
    ctk.CTkLabel(vector_frame, text=f"Constants Vector b ({n}x1):").grid(row=0, column=0, columnspan=3, pady=5)
    vector_entries = []
    for i in range(n):
        # Left bracket
        ctk.CTkLabel(vector_frame, text="[", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=0,
                                                                                          padx=(0, 0))
        # Vector entry
        entry = ctk.CTkEntry(vector_frame, width=60, placeholder_text=f"b{i + 1}", justify="center")
        entry.grid(row=i + 1, column=1, padx=5, pady=5)
        vector_entries.append(entry)
        # Right bracket
        ctk.CTkLabel(vector_frame, text="]", font=("Courier", 25, "bold"), width=10).grid(row=i + 1, column=2,
                                                                                          padx=(0, 0))

def parse_complex(value: str) -> complex:
    """Parses a string representing a complex number."""
    try:
        val = value.replace(" ", "").lower().replace("i", "j")
        val = re.sub(r'\bj(\d+)', r'\1j', val)
        val = re.sub(r'\bj\b', '1j', val)
        val = re.sub(r'([+\-])j(\d*)', lambda m: f"{m.group(1)}{m.group(2) if m.group(2) else '1'}j", val)
        return complex(val)
    except Exception:
        raise ValueError(f"Invalid complex number format: {value}")

def solve_and_display():
    """Solve the system and display results and KVL equations."""
    try:
        n = len(matrix_entries)
        if n == 0:
            result_label.configure(text="Error: Please create input fields first.")
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
        if x is not None:
            result_lines = []
            for i in range(n):
                real_part = x[i].real
                imag_part = x[i].imag

                magnitude = np.abs(x[i])
                angle_deg = np.degrees(np.angle(x[i]))

                mag_str = format(magnitude, fmt)
                angle_str = format(angle_deg, fmt)

                if abs(imag_part) < 1e-10:
                    result_lines.append(f"I{i + 1} = {format(real_part, fmt)} Amps  ({mag_str} ∠ {angle_str}° Amps)")
                elif abs(real_part) < 1e-10:
                    result_lines.append(f"I{i + 1} = {format(imag_part, fmt)}j Amps  ({mag_str} ∠ {angle_str}° Amps)")
                else:
                    result_lines.append(
                        f"I{i + 1} = {format(real_part, fmt)} + {format(imag_part, fmt)}j Amps  ({mag_str} ∠ {angle_str}° Amps)")

            result_text = "Solution:\n" + "\n".join(result_lines)
            result_label.configure(text=result_text)

            kvl_equations = []
            for i in range(n):
                terms = []
                for j in range(n):
                    coeff = A[i, j]
                    if coeff != 0:
                        if abs(coeff.imag) < 1e-10:
                            term = f"{format(coeff.real, fmt)} Ohms * I{j + 1}"
                        elif abs(coeff.real) < 1e-10:
                            term = f"{format(coeff.imag, fmt)}j Ohms * I{j + 1}"
                        else:
                            sign = '+' if coeff.imag >= 0 else '-'
                            term = f"({format(coeff.real, fmt)} {sign} {format(abs(coeff.imag), fmt)}j) Ohms * I{j + 1}"
                        terms.append(term)

                rhs_real = b[i].real
                rhs_imag = b[i].imag

                if abs(rhs_imag) < 1e-10:
                    rhs = f"{format(rhs_real, fmt)}"
                elif abs(rhs_real) < 1e-10:
                    rhs = f"{format(rhs_imag, fmt)}j"
                else:
                    sign = '+' if rhs_imag >= 0 else '-'
                    rhs = f"{format(rhs_real, fmt)} {sign} {format(abs(rhs_imag), fmt)}j"

                equation = " + ".join(terms) + f" = {rhs} Volts"
                kvl_equations.append(equation)

            kvl_label.configure(text="KVL Equations:\n" + "\n".join(kvl_equations))
        else:
            result_label.configure(text="Error: Solution does not exist.\n(Either invalid inputs or the determinant is zero).")
            kvl_label.configure(text="")

    except Exception:
        result_label.configure(text="Error: Invalid input.\nType a real or complex number such as 3+4j or -5.")
        kvl_label.configure(text="")

# ------------------------- GUI ELEMENTS --------------------------

# Title
title_label = ctk.CTkLabel(scrollable_frame, text="AC and DC Circuit Analysis Calculator", font=("Franklin Gothic Medium", 20))
title_label.pack(pady=10)

# Subtitle
subtitle_label = ctk.CTkLabel(scrollable_frame, text="by Cody Carter and Rohan Patel", font=("Franklin Gothic Medium", 14))
subtitle_label.pack(pady=(0, 5))

# Switches frame (Theme and Always on Top)
switch_frame = ctk.CTkFrame(scrollable_frame)
switch_frame.pack(pady=10)

theme_switch = ctk.CTkSwitch(switch_frame, text="Dark Mode", command=toggle_theme)
theme_switch.pack(side="left", padx=10)

topmost_switch = ctk.CTkSwitch(switch_frame, text="Always on Top", command=toggle_always_on_top)
topmost_switch.pack(side="left", padx=10)

# Result label
result_label = ctk.CTkLabel(scrollable_frame, text="Select number of equations and click Set Size", font=("Franklin Gothic Medium", 14))
result_label.pack(pady=10)

# KVL equations label
kvl_label = ctk.CTkLabel(scrollable_frame, text="", font=("Franklin Gothic Medium", 12), wraplength=500, justify="left")
kvl_label.pack(pady=10)

# Size input with dropdown
size_frame = ctk.CTkFrame(scrollable_frame)
size_frame.pack(pady=10)

# Row 1: Number of Equations and Set Size button
size_row1 = ctk.CTkFrame(size_frame)
size_row1.pack(pady=5, fill="x")

ctk.CTkLabel(size_row1, text="Number of Equations:").pack(side="left", padx=5)
size_dropdown = ctk.CTkOptionMenu(size_row1, values=["1", "2", "3", "4"])
size_dropdown.set("3")  # Default
size_dropdown.pack(side="left", padx=5)

size_button = ctk.CTkButton(size_row1, text="Set Size", command=create_input_fields)
size_button.pack(side="left", padx=5)

# Row 2: Decimal Precision dropdown
size_row2 = ctk.CTkFrame(size_frame)
size_row2.pack(pady=5, fill="x")

ctk.CTkLabel(size_row2, text="Decimal Precision:").pack(side="left", padx=5)
precision_dropdown = ctk.CTkOptionMenu(size_row2, values=["0", "1", "2", "3", "4", "5", "6"], variable=precision_var)
precision_dropdown.set("3")
precision_dropdown.pack(side="left", padx=23)

# Placeholder for matrix and vector frames
matrix_frame = ctk.CTkFrame(scrollable_frame)
matrix_frame.pack(pady=10)
vector_frame = ctk.CTkFrame(scrollable_frame)
vector_frame.pack(pady=10)

# Solve and Reset buttons
solve_button = ctk.CTkButton(scrollable_frame, text="Solve (Enter)", command=solve_and_display)
solve_button.pack(pady=10)

reset_button = ctk.CTkButton(scrollable_frame, text="Reset (R)", command=create_input_fields)
reset_button.pack(pady=10)

def on_key_press(event):
    if event.keysym in ("Return","KP_Enter"):
        solve_and_display()
    elif event.keysym in ("r"):
        create_input_fields()

root.bind("<Key>", on_key_press)


# Start the main loop
root.mainloop()