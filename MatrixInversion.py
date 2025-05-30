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

def get_matrix_input():
    print("Enter the number of variables (e.g., 3 for a 3x3 system):")
    while True:
        try:
            n = int(input("Number of variables: "))
            if n <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer.")

    print("\nEnter matrix A row by row, with elements separated by commas. These are the coefficients of each KVL equation.")
    A = []
    for i in range(n):
        while True:
            row_input = input(f"Row {i+1}: ")
            try:
                row = [float(num) for num in row_input.strip().split(',')]
                if len(row) != n:
                    raise ValueError
                A.append(row)
                break
            except ValueError:
                print(f"Please enter exactly {n} numbers separated by commas.")

    print("\nEnter the vector b, with values separated by commas. These are the right-hand side constants of each KVL equation.")
    while True:
        b_input = input("b: ")
        try:
            b = [float(num) for num in b_input.strip().split(',')]
            if len(b) != n:
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {n} numbers separated by commas.")

    return np.array(A), np.array(b)

def display_equations(A, b):
    print("\nKVL Equations:")
    for i in range(len(b)):
        terms = []
        for j in range(len(A[i])):
            coeff = A[i][j]
            if coeff == 0:
                continue
            var = f"I{j+1}"
            if coeff == 1:
                terms.append(f"{var}")
            elif coeff == -1:
                terms.append(f"- {var}")
            else:
                sign = "-" if coeff < 0 else ""
                coeff_str = f"{abs(coeff):.4g}Ω"
                terms.append(f"{sign}{coeff_str} * {var}")
        equation = " + ".join(terms).replace("+ -", "- ")
        print(f"Loop {i+1}: {equation} = {b[i]:.4g}V")

def main():
    A, b = get_matrix_input()
    display_equations(A, b)
    x = solve_linear_system(A, b)

    if x is not None:
        print("\nSolution:")
        for i, val in enumerate(x, start=1):
            print(f"I{i} = {val:.4g} A")

# Run the main function
if __name__ == "__main__":
    main()
