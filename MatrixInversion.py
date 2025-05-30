import numpy as np
import customtkinter as ctk

# Set default appearance and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create main window
root = ctk.CTk()
root.title("Nodal Analysis Calculator")
root.geometry("600x800")

# Global variables to store dynamic entry fields
matrix_entries = []
vector_entries = []
matrix_frame = None
vector_frame = None
result_label = None

def toggle_theme():
    mode = "dark" if theme_switch.get() else "light"
    ctk.set_appearance_mode(mode)

def solve_linear_system(A, b):
    """
    Solves a system of linear equations Ax = b using a direct solver.

    Args:
        A (numpy.ndarray): The coefficient matrix (square matrix).
        b (numpy.ndarray): The constants vector.

    Returns:
        numpy.ndarray: The solution vector x, or None if the system cannot be solved.
    """
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

def create_input_fields():
    """Create input fields for matrix A and vector b based on user-specified size."""
    global matrix_frame, vector_frame, matrix_entries, vector_entries, result_label
    try:
        n = int(size_entry.get())
        if n < 1:
            result_label.configure(text="Error: Number of equations must be positive.")
            return
    except ValueError:
        result_label.configure(text="Error: Please enter a valid number of equations.")
        return

    try:
        n = int(size_entry.get())
        if n > 4:
            result_label.configure(text="Error: Number of equations must be 4 or less.")
            return
    except ValueError:
        result_label.configure(text="Error: Please enter a valid number of equations.")
        return
    
    # Clear previous input fields
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

def solve_and_display():
    """Solve the system and display results."""
    try:
        n = len(matrix_entries)
        if n == 0:
            result_label.configure(text="Error: Please create input fields first.")
            return

        # Get matrix A
        A = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                A[i, j] = float(matrix_entries[i][j].get())

        # Get vector b
        b = np.array([float(entry.get()) for entry in vector_entries])

        # Solve the system
        x = solve_linear_system(A, b)
        if x is not None:
            result_text = "Solution:\n" + "\n".join(f"I{i+1} = {x[i]:.3g} A" for i in range(n))
            result_label.configure(text=result_text)
        else:
            result_label.configure(text="Error: System cannot be solved (singular matrix).")
    except ValueError:
        result_label.configure(text="Error: Please enter valid numbers.")

# Create GUI elements
# Title
title_label = ctk.CTkLabel(root, text="Nodal Analysis Calculator", font=("Arial", 20))
title_label.pack(pady=10)

# Theme switch
theme_switch = ctk.CTkSwitch(root, text="Dark Mode", command=toggle_theme)
theme_switch.pack(pady=10)

# Result label
result_label = ctk.CTkLabel(root, text="Enter number of equations and click Set Size", font=("Arial", 14))
result_label.pack(pady=10)

# Size input
size_frame = ctk.CTkFrame(root)
size_frame.pack(pady=10)
ctk.CTkLabel(size_frame, text="Number of Equations:").pack(side="left", padx=5)
size_entry = ctk.CTkEntry(size_frame, width=100, placeholder_text="e.g., 3")
size_entry.pack(side="left", padx=5)
size_button = ctk.CTkButton(size_frame, text="Set Size", command=create_input_fields)
size_button.pack(side="left", padx=5)

# Placeholder for matrix and vector frames
matrix_frame = ctk.CTkFrame(root)
matrix_frame.pack(pady=10)
vector_frame = ctk.CTkFrame(root)
vector_frame.pack(pady=10)

# Solve button
solve_button = ctk.CTkButton(root, text="Solve", command=solve_and_display)
solve_button.pack(pady=10)

# Reset Button
solve_button = ctk.CTkButton(root, text="Reset", command=create_input_fields)
solve_button.pack(pady=10)

# Start the main loop
root.mainloop()