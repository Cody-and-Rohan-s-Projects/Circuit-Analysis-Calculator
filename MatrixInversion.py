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

"""
    2 Ohms * I1 -  I2 + I3 = 5 Volts
    I1 + I3 = 6 Volts
    3 Ohms * I1 + 2 Ohms * I2 + 4 Ohms * I3 = 10 Volts
"""



A = np.array([[2, -1, 1],
              [1,  0, 1],
              [3,  2, 4]])  # A non-singular matrix
b = np.array([5, 6, 10])

x = solve_linear_system(A, b)

if x is not None:
    x = np.linalg.solve(A, b)
    print("Solution:")
    print(f"I1 = {x[0]:.3g} A")
    print(f"I2 = {x[1]:.3g} A")
    print(f"I3 = {x[2]:.3g} A")
