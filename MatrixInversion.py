import numpy as np

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
    except np.linalg.LinAlgError as e:
        print("Error:", e)
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
