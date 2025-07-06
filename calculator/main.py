# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from calculator_ui import Ui_MainWindow  # your provided UI

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Align display and make it read-only
        self.ui.lineEdit.setAlignment(Qt.AlignRight)
        self.ui.lineEdit.setReadOnly(True)

        # Connect digit buttons
        self.ui.pushButton.clicked.connect(lambda: self.append_text("1"))
        self.ui.pushButton_2.clicked.connect(lambda: self.append_text("2"))
        self.ui.pushButton_3.clicked.connect(lambda: self.append_text("3"))
        self.ui.pushButton_4.clicked.connect(lambda: self.append_text("4"))
        self.ui.pushButton_5.clicked.connect(lambda: self.append_text("5"))
        self.ui.pushButton_6.clicked.connect(lambda: self.append_text("6"))
        self.ui.pushButton_7.clicked.connect(lambda: self.append_text("7"))
        self.ui.pushButton_8.clicked.connect(lambda: self.append_text("8"))
        self.ui.pushButton_9.clicked.connect(lambda: self.append_text("9"))
        self.ui.pushButton_10.clicked.connect(lambda: self.append_text("0"))
        self.ui.pushButton_11.clicked.connect(lambda: self.append_text("."))

        # Operators
        self.ui.pushButton_14.clicked.connect(lambda: self.append_text("/"))
        self.ui.pushButton_15.clicked.connect(lambda: self.append_text("*"))
        self.ui.pushButton_16.clicked.connect(lambda: self.append_text("-"))
        self.ui.pushButton_17.clicked.connect(lambda: self.append_text("+"))

        # Equals
        self.ui.pushButton_13.clicked.connect(self.calculate_result)

        # Square
        self.ui.pushButton_12.clicked.connect(self.square_value)

        # Square Root
        self.ui.pushButton_18.clicked.connect(self.sqrt_value)

        # CE (Clear Entry)
        self.ui.pushButton_19.clicked.connect(self.clear_entry)

        # Delete (Backspace)
        self.ui.pushButton_20.clicked.connect(self.backspace)

    def append_text(self, text):
        current = self.ui.lineEdit.text()
        self.ui.lineEdit.setText(current + text)

    def clear_entry(self):
        self.ui.lineEdit.clear()

    def backspace(self):
        current = self.ui.lineEdit.text()
        self.ui.lineEdit.setText(current[:-1])

    def square_value(self):
        try:
            value = float(self.ui.lineEdit.text())
            self.ui.lineEdit.setText(str(value ** 2))
        except Exception:
            self.show_error("Invalid input for square.")

    def sqrt_value(self):
        try:
            value = float(self.ui.lineEdit.text())
            if value < 0:
                self.show_error("Cannot take square root of negative number.")
                return
            self.ui.lineEdit.setText(str(value ** 0.5))
        except Exception:
            self.show_error("Invalid input for square root.")

    def calculate_result(self):
        expression = self.ui.lineEdit.text()
        try:
            # Replace ^ with ** for exponentiation
            expression = expression.replace("^", "**")

            # Evaluate safely
            allowed_chars = "0123456789+-*/.() **"
            if all(char in allowed_chars or char == "*" for char in expression):
                result = str(eval(expression))
                self.ui.lineEdit.setText(result)
            else:
                self.show_error("Invalid characters in expression.")
        except Exception:
            self.show_error("Error evaluating expression.")

    def show_error(self, message):
        self.ui.lineEdit.setText("Error")
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.setWindowTitle("Advanced Calculator")
    window.resize(320, 450)
    window.show()
    sys.exit(app.exec())
