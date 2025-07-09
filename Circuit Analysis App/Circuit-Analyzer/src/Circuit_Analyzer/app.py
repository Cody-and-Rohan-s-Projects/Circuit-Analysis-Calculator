import os
import re
import numpy as np
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

#light and dark theme styles
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

class CircuitAnalyzer(toga.App):
    def startup(self):
        self.precision = "3"
        self.matrix_size = 3
        self.matrix_entries = []
        self.vector_entries = []
        self.current_theme = LIGHT_THEME

        self.scroll_content = toga.Box(style=Pack(direction=COLUMN, margin=10))

        # Theme toggle button row
        theme_row = toga.Box(style=Pack(direction=ROW, justify_content="end", margin=(0, 10)))
        self.theme_toggle = toga.Button(
            "Switch to Dark Theme",
            on_press=self.toggle_theme,
            style=Pack(margin=5)
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
            items=["1", "2", "3", "4", "5", "6"],
            value=self.precision,
            style=Pack(width=70),
        )
        self.precision_dropdown.on_select = self.set_precision
        dropdown_row.add(dropdown_label)
        dropdown_row.add(self.precision_dropdown)
        self.scroll_content.add(dropdown_row)

        # Matrix Size Selector
        size_row = toga.Box(style=Pack(direction=ROW, margin=(0, 10), align_items=CENTER))
        size_label = toga.Label(
            "Number of Equations:",
            style=Pack(margin_right=10, font_family=self.current_theme["label_font_family"],
                       color=self.current_theme["text_color"])
        )
        self.size_selector = toga.Selection(
            items=["1", "2", "3", "4"],
            value=str(self.matrix_size),
            style=Pack(width=55),
        )
        size_button = toga.Button(
            "Confirm Matrix Size",
            on_press=self.set_matrix_size,
            style=Pack(margin_left=10, margin=6)
        )
        size_row.add(size_label)
        size_row.add(self.size_selector)
        size_row.add(size_button)
        self.scroll_content.add(size_row)

        # Single multiline text input to show both solution and KVL equations
        self.result_label = toga.MultilineTextInput(
            readonly=True,
            style=Pack(
                margin=(10, 5),
                font_family=self.current_theme["label_font_family"],
                color=self.current_theme["text_color"],
                background_color=self.current_theme["input_background"],
                width=360,
                height=200,
            ),
        )
        self.result_label.value = "Select number of equations and click Confirm Matrix Size"
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
        self.main_window.size = (450, 800)
        self.main_window.position = (0,0)
        self.main_window.show()

        self.apply_theme()

    def toggle_theme(self, widget):
        if self.current_theme == LIGHT_THEME:
            self.current_theme = DARK_THEME
            self.theme_toggle.label = "Switch to Light Theme"
        else:
            self.current_theme = LIGHT_THEME
            self.theme_toggle.label = "Switch to Dark Theme"
        self.apply_theme()

    def apply_theme(self):
        bg = self.current_theme["background_color"]
        fg = self.current_theme["text_color"]
        input_bg = self.current_theme["input_background"]
        input_fg = self.current_theme["input_color"]
        btn_bg = self.current_theme["button_background"]
        btn_fg = self.current_theme["button_color"]
        label_font = self.current_theme["label_font_family"]

        self.main_window.background_color = bg
        self.scroll_content.style.update(background_color=bg)

        for child in self.scroll_content.children:
            if isinstance(child, toga.Label):
                child.style.color = fg
                child.style.font_family = label_font
            if isinstance(child, toga.Box):
                for item in child.children:
                    if isinstance(item, toga.Label):
                        item.style.color = fg
                        item.style.font_family = label_font
                    elif isinstance(item, (toga.TextInput, toga.MultilineTextInput)):
                        item.style.background_color = input_bg
                        item.style.color = input_fg

        self.precision_dropdown.style.background_color = input_bg
        self.precision_dropdown.style.color = input_fg
        self.size_selector.style.background_color = input_bg
        self.size_selector.style.color = input_fg

        self.result_label.style.background_color = input_bg
        self.result_label.style.color = input_fg

        for row in self.scroll_content.children:
            if isinstance(row, toga.Box):
                for widget in row.children:
                    if isinstance(widget, toga.Button):
                        widget.style.background_color = btn_bg
                        widget.style.color = btn_fg

        for row_entries in self.matrix_entries:
            for entry in row_entries:
                entry.style.background_color = input_bg
                entry.style.color = input_fg
        for entry in self.vector_entries:
            entry.style.background_color = input_bg
            entry.style.color = input_fg

    def set_precision(self, widget):
        self.precision = widget.value
        self.result_label.value = f"Decimal precision set to: {self.precision}"

    def set_matrix_size(self, widget):
        self.matrix_size = int(self.size_selector.value)
        self.create_input_fields(self.matrix_size)

    def create_input_fields(self, n):
        while len(self.scroll_content.children) > 5:
            self.scroll_content.remove(self.scroll_content.children[5])

        self.matrix_entries = []
        self.vector_entries = []

        self.scroll_content.add(toga.Label(
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
                        padding=2,
                    ),
                )
                row.add(entry)
                row_entries.append(entry)
            row.add(toga.Label("]",
                               style=Pack(font_family="Courier New", font_size=20, margin_left=5,
                                          color=self.current_theme["text_color"])))
            self.matrix_entries.append(row_entries)
            self.scroll_content.add(row)

        self.scroll_content.add(toga.Label(
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
                    padding=2,
                ),
            )
            self.vector_entries.append(entry)
            row.add(entry)
            row.add(toga.Label("]",
                               style=Pack(font_family="Courier New", font_size=20, margin_left=5,
                                          color=self.current_theme["text_color"])))
            self.scroll_content.add(row)

    def parse_complex(self, value: str) -> complex:
        try:
            val = value.replace(',', '')  # Remove commas
            val = val.lower().replace('i', 'j')  # Replace 'i' with 'j'
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
                self.result_label.value = "Error: Please create input fields first."
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

            combined_text = "Solution:\n" + "\n".join(result_lines) + "\n\nKVL Equations:\n" + "\n".join(kvl_lines)
            self.result_label.value = combined_text

        except Exception as e:
            self.result_label.value = f"Error: Invalid input. {str(e)}"

    def reset_ui(self, widget):
        self.set_matrix_size(widget)
        self.result_label.value = "Select number of equations and click Confirm"

def main():
    return CircuitAnalyzer(
        formal_name="Circuit Analyzer",
        app_id="com.codycarterandrohanpatel.circuitanalyzer",
        icon=icon_path
    )
