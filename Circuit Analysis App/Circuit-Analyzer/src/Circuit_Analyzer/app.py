import os
import re
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

LIGHT_THEME = {
    "background_color": "white",
    "text_color": "black",
    "input_background": "white",
    "input_color": "black",
    "button_background": "#0078D7",
    "button_color": "white",
    "label_font_family": "sans-serif",
}

DARK_THEME = {
    "background_color": "#121212",
    "text_color": "white",
    "input_background": "#222222",
    "input_color": "white",
    "button_background": "#0A84FF",
    "button_color": "white",
    "label_font_family": "sans-serif",
}

PRECISION_OPTIONS = [str(i) for i in range(1, 7)]
MATRIX_SIZE_OPTIONS = [str(i) for i in range(1, 5)]

class CircuitAnalyzer(toga.App):
    def startup(self):
        self.precision = "3"
        self.matrix_size = 3
        self.matrix_entries = []
        self.vector_entries = []
        self.current_theme = LIGHT_THEME

        self.scroll_content = toga.Box(style=Pack(direction=COLUMN, margin=10, flex=1))

        # Theme toggle button
        theme_row = toga.Box(style=Pack(direction=ROW, justify_content="end", margin=(0, 10)))
        self.theme_toggle = toga.Button(
            "Toggle Dark Theme",
            on_press=self.toggle_theme,
            style=Pack(margin=5),
        )
        theme_row.add(self.theme_toggle)
        self.scroll_content.add(theme_row)

        # Decimal Precision Dropdown
        dropdown_row = toga.Box(style=Pack(direction=ROW, margin=(0, 10), align_items=CENTER))
        dropdown_label = toga.Label(
            "Decimal Precision:",
            style=Pack(margin_right=10, font_family=self.current_theme["label_font_family"],
                       color=self.current_theme["text_color"])
        )
        self.precision_dropdown = toga.Selection(
            items=PRECISION_OPTIONS,
            value=self.precision,
            style=Pack(width=100, background_color=self.current_theme["input_background"],
                       color=self.current_theme["input_color"]),
        )
        self.precision_dropdown.on_select = self.set_precision

        dropdown_row.add(dropdown_label)
        dropdown_row.add(self.precision_dropdown)
        self.scroll_content.add(dropdown_row)

        # Matrix Size Selector
        size_row = toga.Box(style=Pack(direction=ROW, margin=(0, 5), align_items=CENTER))
        size_label = toga.Label(
            "Number of Equations:",
            style=Pack(margin_right=10, font_family=self.current_theme["label_font_family"],
                       color=self.current_theme["text_color"])
        )
        self.size_selector = toga.Selection(
            items=MATRIX_SIZE_OPTIONS,
            value=str(self.matrix_size),
            style=Pack(width=100, background_color=self.current_theme["input_background"],
                       color=self.current_theme["input_color"])
        )
        size_row.add(size_label)
        size_row.add(self.size_selector)
        self.scroll_content.add(size_row)

        # Confirm Matrix Size Button
        size_button = toga.Button(
            "Confirm Matrix Size",
            on_press=self.set_matrix_size,
            style=Pack(margin=(5, 5, 10, 0))  # top, right, bottom, left
        )
        self.scroll_content.add(size_button)

        self.dynamic_input_area = toga.Box(style=Pack(direction=COLUMN, margin=(10, 5)))
        self.scroll_content.add(self.dynamic_input_area)

        # Result display
        self.result_label = toga.MultilineTextInput(
            readonly=False,
            placeholder= "Select number of equations and click Confirm Matrix Size",
            style=Pack(
                margin=(10, 5),
                font_family=self.current_theme["label_font_family"],
                color=self.current_theme["text_color"],
                background_color=self.current_theme["input_background"],
                flex=1,
                width=450,
                height=370,
            ),
        )
        self.scroll_content.add(self.result_label)

        # Buttons row
        button_row = toga.Box(style=Pack(direction=ROW, margin=10, align_items=CENTER))
        solve_button = toga.Button(
            "Solve",
            on_press=self.solve_system,
            style=Pack(margin_right=10, margin=8, background_color=self.current_theme["button_background"],
                       color=self.current_theme["button_color"]),
        )
        reset_button = toga.Button(
            "Reset",
            on_press=self.reset_ui,
            style=Pack(margin_right=10, margin=8, background_color=self.current_theme["button_background"],
                       color=self.current_theme["button_color"]),
        )
        button_row.add(solve_button)
        button_row.add(reset_button)
        self.scroll_content.add(button_row)

        self.scroll_container = toga.ScrollContainer(horizontal=True, vertical=True)
        self.scroll_container.content = self.scroll_content

        self.main_window = toga.MainWindow(title="Circuit Analysis Calculator")
        self.main_window.content = self.scroll_container
        self.main_window.size = (450, 1000)
        self.main_window.position = (0, 0)
        self.main_window.show()

        self.apply_theme()

    def toggle_theme(self, widget):
        if self.current_theme == LIGHT_THEME:
            self.current_theme = DARK_THEME
            self.apply_theme()
        else:
            self.current_theme = LIGHT_THEME
            self.apply_theme()

    def apply_theme(self):
        theme = self.current_theme

        self.main_window.background_color = theme["background_color"]
        self.scroll_content.style.background_color = theme["background_color"]

        def style_widget(w):
            if isinstance(w, toga.Label):
                w.style.color = theme["text_color"]
                w.style.font_family = theme["label_font_family"]
            elif isinstance(w, toga.Button):
                w.style.color = theme["button_color"]
                w.style.background_color = theme["button_background"]
            elif isinstance(w, (toga.TextInput, toga.MultilineTextInput, toga.Selection)):
                w.style.color = theme["input_color"]
                w.style.background_color = theme["input_background"]
            if hasattr(w, "children"):
                for child in w.children:
                    style_widget(child)

        # Apply style recursively to entire scroll_content tree
        style_widget(self.scroll_content)

        # Update dropdown values explicitly to ensure sync
        self.precision_dropdown.items = PRECISION_OPTIONS
        self.precision_dropdown.value = self.precision
        self.size_selector.items = MATRIX_SIZE_OPTIONS
        self.size_selector.value = str(self.matrix_size)

    def set_precision(self, widget):
        self.precision = widget.value
        self.result_label.value = f"Decimal precision set to: {self.precision}"

    def set_matrix_size(self, widget):
        try:
            self.matrix_size = int(self.size_selector.value)
            self.create_input_fields(self.matrix_size)
            self.result_label.value = "Input fields created."
        except Exception as e:
            self.result_label.value = f"Error setting matrix size: {e}"

    def create_input_fields(self, n):
        self.dynamic_input_area.children.clear()

        self.matrix_entries = []
        self.vector_entries = []

        self.dynamic_input_area.add(toga.Label(
            f"Coefficient Matrix A ({n}x{n}):",
            style=Pack(margin=(10, 5),
                       font_family=self.current_theme["label_font_family"],
                       color=self.current_theme["text_color"])
        ))

        for i in range(n):
            row = toga.Box(style=Pack(direction=ROW, margin=2, justify_content="start"))
            row_entries = []
            row.add(toga.Label("[",
                               style=Pack(font_family="Courier New", font_size=20, margin_right=5,
                                          color=self.current_theme["text_color"])))
            for j in range(n):
                entry = toga.TextInput(
                    placeholder=f"A{i + 1}{j + 1}",
                    style=Pack(
                        width=50,
                        margin_right=5,
                        background_color=self.current_theme["input_background"],
                        color=self.current_theme["input_color"],
                        font_family=self.current_theme["label_font_family"],
                        margin=2,
                    ),
                )
                row.add(entry)
                row_entries.append(entry)
            row.add(toga.Label("]",
                               style=Pack(font_family="Courier New", font_size=20, margin_left=5,
                                          color=self.current_theme["text_color"])))
            self.matrix_entries.append(row_entries)
            self.dynamic_input_area.add(row)

        self.dynamic_input_area.add(toga.Label(
            f"Constants Vector b ({n}x1):",
            style=Pack(margin=(10, 5),
                       font_family=self.current_theme["label_font_family"],
                       color=self.current_theme["text_color"])
        ))

        for i in range(n):
            row = toga.Box(style=Pack(direction=ROW, margin=2))
            row.add(toga.Label("[",
                               style=Pack(font_family="Courier New", font_size=20, margin_right=5,
                                          color=self.current_theme["text_color"])))
            entry = toga.TextInput(
                placeholder=f"b{i + 1}",
                style=Pack(
                    width=50,
                    margin_right=5,
                    background_color=self.current_theme["input_background"],
                    color=self.current_theme["input_color"],
                    font_family=self.current_theme["label_font_family"],
                    margin=2,
                ),
            )
            self.vector_entries.append(entry)
            row.add(entry)
            row.add(toga.Label("]",
                               style=Pack(font_family="Courier New", font_size=20, margin_left=5,
                                          color=self.current_theme["text_color"])))
            self.dynamic_input_area.add(row)

    def parse_complex(self, value: str) -> complex:
        try:
            val = value.replace(',', " ")  # Remove commas
            val = val.lower().replace('i', 'j')  # Replace 'i' with 'j'
            val = re.sub(r'\s+', '', val)  # Remove whitespace
            val = re.sub(r'(?<![\d.])j(\d+(\.\d+)?)(?![\d.])', r'\1j', val)
            val = re.sub(r'(?<=[\+\-])j(?![\d.])', '1j', val)
            val = re.sub(r'^j$', '1j', val)
            return complex(val)
        except Exception:
            raise ValueError(f"Invalid complex number format: {value}")

    def solve_system(self, widget):
        try:
            n = len(self.matrix_entries)
            if n == 0:
                self.result_label.value = "Error: Please create input fields first."
                return

            A = np.zeros((n, n), dtype=complex)
            b = np.zeros(n, dtype=complex)
            precision_int = int(self.precision_dropdown.value)
            self.precision = self.precision_dropdown.value  # Keep it in sync
            fmt = f".{precision_int}f"

            for i in range(n):
                for j in range(n):
                    A[i, j] = self.parse_complex(self.matrix_entries[i][j].value or "0")
                b[i] = self.parse_complex(self.vector_entries[i].value or "0")

            x = np.linalg.solve(A, b)

            result_lines = []
            for i, val in enumerate(x, start=1):
                real, imag = val.real, val.imag
                mag = np.abs(val)
                angle = np.degrees(np.angle(val))
                mag_str = format(mag, fmt)
                angle_str = format(angle, fmt)
                if abs(imag) < 1e-10:
                    result_lines.append(f"I{i} = {format(real, fmt)} A  [ {mag_str} ∠ {angle_str}° A ]")
                elif abs(real) < 1e-10:
                    result_lines.append(f"I{i} = {format(imag, fmt)}j A  [ {mag_str} ∠ {angle_str}° A ]")
                else:
                    sign = '+' if imag >= 0 else '-'
                    result_lines.append(
                        f"I{i} = {format(real, fmt)} {sign} {format(abs(imag), fmt)}j A  [ {mag_str} ∠ {angle_str}° A ]")

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

            self.result_label.value = "Solution:\n" + "\n".join(result_lines) + "\n\nKVL Equations:\n" + "\n".join(kvl_lines)

        except Exception as e:
            self.result_label.value = f"Error: Invalid input. {e}"

    def reset_ui(self, widget):
        self.set_matrix_size(widget)
        self.result_label.value = "Select number of equations and click Confirm Matrix Size"

def main():
    return CircuitAnalyzer(
        formal_name="Circuit Analyzer",
        app_id="com.codycarterandrohanpatel.circuitanalyzer",
        icon=icon_path,
    )
