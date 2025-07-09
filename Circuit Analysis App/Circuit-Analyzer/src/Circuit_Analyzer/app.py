import os
import re
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

class CircuitAnalyzer(toga.App):
    def startup(self):
        self.precision = "3"
        self.matrix_size = 3
        self.matrix_entries = []
        self.vector_entries = []
        self.scroll_content = toga.Box(style=Pack(direction=COLUMN, margin=10))

        # Decimal Precision Dropdown
        dropdown_row = toga.Box(style=Pack(direction=ROW, margin=(0, 10)))
        dropdown_label = toga.Label("Decimal Precision:", style=Pack(margin_right=10, font_family="sans-serif"))
        self.precision_dropdown = toga.Selection(
            items=["1", "2", "3", "4", "5", "6"],
            value=self.precision,
            style=Pack(width=78)
        )
        self.precision_dropdown.on_select = self.set_precision
        dropdown_row.add(dropdown_label)
        dropdown_row.add(self.precision_dropdown)
        self.scroll_content.add(dropdown_row)

        # Matrix Size Selector
        size_row = toga.Box(style=Pack(direction=ROW, margin=(0, 10)))
        size_label = toga.Label("Number of Equations:", style=Pack(margin_right=10, font_family="sans-serif"))
        self.size_selector = toga.Selection(
            items=["1", "2", "3", "4"],
            value=str(self.matrix_size),
            style=Pack(width=60)
        )
        size_button = toga.Button("Confirm Matrix Size", on_press=self.set_matrix_size, style=Pack(margin_left=10, font_family="sans-serif"))
        size_row.add(size_label)
        size_row.add(self.size_selector)
        size_row.add(size_button)
        self.scroll_content.add(size_row)

        # Labels
        self.result_label = toga.Label("Select number of equations and click Confirm Matrix Size", style=Pack(margin=(10, 5), font_family="sans-serif"))
        self.kvl_label = toga.Label("", style=Pack(font_family="sans-serif"))
        self.scroll_content.add(self.result_label)

        # Action Buttons
        button_row = toga.Box(style=Pack(direction=ROW, margin=10, align_items=CENTER))
        solve_button = toga.Button("Solve", on_press=self.solve_system, style=Pack(margin_right=10, font_family="sans-serif"))
        reset_button = toga.Button("Reset", on_press=self.reset_ui, style=Pack(margin_right=10, font_family="sans-serif"))
        copy_button = toga.Button( "Copy Solution + KVL Equations", on_press=self.copy_solution_and_kvl, style=Pack(margin_right=10, font_family="sans-serif"))
        button_row.add(solve_button)
        button_row.add(reset_button)
        button_row.add(copy_button)
        self.scroll_content.add(button_row)

        self.scroll_content.add(self.kvl_label)

        # Set up scroll view
        self.scroll_container = toga.ScrollContainer(horizontal=True)
        self.scroll_container.content = self.scroll_content

        self.main_window = toga.MainWindow(title="Circuit Analysis Calculator")
        self.main_window.content = self.scroll_container
        self.main_window.show()

    def set_precision(self, widget):
        self.precision = widget.value
        self.result_label.text = f"Decimal precision set to: {self.precision}"

    def set_matrix_size(self, widget):
        self.matrix_size = int(self.size_selector.value)
        self.create_input_fields(self.matrix_size)

    def create_input_fields(self, n):
        while len(self.scroll_content.children) > 5:
            self.scroll_content.remove(self.scroll_content.children[5])

        self.matrix_entries = []
        self.vector_entries = []

        self.scroll_content.add(toga.Label(f"Coefficient Matrix A ({n}x{n}):", style=Pack(margin=(10, 5), font_family="sans-serif")))
        for i in range(n):
            row = toga.Box(style=Pack(direction=ROW, margin=2))
            row_entries = []
            row.add(toga.Label("[", style=Pack(font_family="Courier New", font_size=20, margin_right=5)))
            for j in range(n):
                entry = toga.TextInput(placeholder=f"A{i + 1}{j + 1}", style=Pack(width=60, margin_right=5))
                row.add(entry)
                row_entries.append(entry)
            row.add(toga.Label("]", style=Pack(font_family="Courier New", font_size=20, margin_left=5)))
            self.matrix_entries.append(row_entries)
            self.scroll_content.add(row)

        self.scroll_content.add(toga.Label(f"Constants Vector b ({n}x1):", style=Pack(margin=(10, 5), font_family="sans-serif")))
        for i in range(n):
            row = toga.Box(style=Pack(direction=ROW, margin=2))
            row.add(toga.Label("[", style=Pack(font_family="Courier New", font_size=20, margin_right=5)))
            entry = toga.TextInput(placeholder=f"b{i + 1}", style=Pack(width=60, margin_right=5))
            self.vector_entries.append(entry)
            row.add(entry)
            row.add(toga.Label("]", style=Pack(font_family="Courier New", font_size=20, margin_left=5)))
            self.scroll_content.add(row)

    def parse_complex(self, value: str) -> complex:
        try:
            val = value.lower().replace('i', 'j')  # Replace 'i' with 'j'
            val = re.sub(r'\s+', '', val)  # Remove all whitespace

            # Fix cases where imaginary unit comes first (e.g., j3 → 3j)
            val = re.sub(r'(?<![\d.])j(\d+(\.\d+)?)(?![\d.])', r'\1j', val)

            # Replace standalone j with 1j (e.g., +j, -j, or just j)
            val = re.sub(r'(?<=[\+\-])j(?![\d.])', '1j', val)
            val = re.sub(r'^j$', '1j', val)
            return complex(val)
        except Exception:
            raise ValueError(f"Invalid complex number format: {value}")

    def solve_system(self, widget):
        try:
            n = len(self.matrix_entries)
            if n == 0:
                self.result_label.text = "Error: Please create input fields first."
                return

            A = np.zeros((n, n), dtype=complex)
            b = np.zeros(n, dtype=complex)
            fmt = f".{self.precision}f"

            for i in range(n):
                for j in range(n):
                    A[i, j] = self.parse_complex(self.matrix_entries[i][j].value or "0")
                b[i] = self.parse_complex(self.vector_entries[i].value or "0")

            x = np.linalg.solve(A, b)

            result_lines = []
            for i in range(n):
                real, imag = x[i].real, x[i].imag
                mag = np.abs(x[i])
                angle = np.degrees(np.angle(x[i]))
                mag_str = format(mag, fmt)
                angle_str = format(angle, fmt)
                if abs(imag) < 1e-10:
                    result_lines.append(f"I{i + 1} = {format(real, fmt)} A  ({mag_str}  ∠  {angle_str}° A)")
                elif abs(real) < 1e-10:
                    result_lines.append(f"I{i + 1} = {format(imag, fmt)}j A  ({mag_str}  ∠  {angle_str}° A)")
                else:
                    sign = '+' if imag >= 0 else '-'
                    result_lines.append(
                        f"I{i + 1} = {format(real, fmt)} {sign} {format(abs(imag), fmt)}j A  ({mag_str} ∠ {angle_str}° A)")

            self.result_label.text = "Solution:\n" + "\n".join(result_lines)

            kvl_lines = []
            for i in range(n):
                terms = []
                for j in range(n):
                    coeff = A[i, j]
                    if coeff != 0:
                        if abs(coeff.imag) < 1e-10:
                            term = f"{format(coeff.real, fmt)} Ω * I{j + 1}"
                        elif abs(coeff.real) < 1e-10:
                            term = f"{format(coeff.imag, fmt)}j Ω * I{j + 1}"
                        else:
                            sign = '+' if coeff.imag >= 0 else '-'
                            term = f"({format(coeff.real, fmt)} {sign} {format(abs(coeff.imag), fmt)}j) Ω * I{j + 1}"
                        terms.append(term)

                rhs = b[i]
                if abs(rhs.imag) < 1e-10:
                    rhs_str = format(rhs.real, fmt)
                elif abs(rhs.real) < 1e-10:
                    rhs_str = format(rhs.imag, fmt) + "j"
                else:
                    sign = '+' if rhs.imag >= 0 else '-'
                    rhs_str = f"{format(rhs.real, fmt)} {sign} {format(abs(rhs.imag), fmt)}j"

                kvl_lines.append(" + ".join(terms) + f" = {rhs_str} V")

            self.kvl_label.text  = "KVL Equations:\n" + "\n".join(kvl_lines)

        except Exception as e:
            self.result_label.text = f"Error: Invalid input. {str(e)}"
            self.kvl_label.text = ""

    async def copy_solution_and_kvl(self, widget):
        result_text = self.result_label.text.strip()
        kvl_text = self.kvl_label.text.strip()

        if not result_text.startswith("Solution"):
            self.result_label.text = "Solve the system first before copying."
            return

        full_text = result_text + ("\n\n" + kvl_text if kvl_text else "")

        try:
            await self.clipboard.write_text(full_text)
            self.result_label.text = result_text + "\n\n✔ Copied to clipboard."
        except Exception as e:
            self.result_label.text = f"Error copying to clipboard: {str(e)}"

    def reset_ui(self, widget):
        self.set_matrix_size(widget)
        self.result_label.text = "Select number of equations and click Confirm"
        self.kvl_label.text = ""

def main():
    return CircuitAnalyzer(
        formal_name="Circuit Analyzer",
        app_id="com.codycarterandrohanpatel.circuitanalyzer",
        icon=icon_path
    )
