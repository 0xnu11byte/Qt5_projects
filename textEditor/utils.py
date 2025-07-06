# utils.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout

class FindReplaceDialog(QDialog):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Find and Replace")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.find_input = QLineEdit()
        self.replace_input = QLineEdit()

        layout.addWidget(QLabel("Find:"))
        layout.addWidget(self.find_input)
        layout.addWidget(QLabel("Replace with:"))
        layout.addWidget(self.replace_input)

        btn_layout = QHBoxLayout()
        find_btn = QPushButton("Find")
        replace_btn = QPushButton("Replace")
        replace_all_btn = QPushButton("Replace All")

        find_btn.clicked.connect(self.find)
        replace_btn.clicked.connect(self.replace)
        replace_all_btn.clicked.connect(self.replace_all)

        btn_layout.addWidget(find_btn)
        btn_layout.addWidget(replace_btn)
        btn_layout.addWidget(replace_all_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def find(self):
        text = self.find_input.text()
        cursor = self.editor.textCursor()
        document = self.editor.document()
        found = document.find(text, cursor)
        if found.isNull():
            cursor.movePosition(cursor.Start)
            found = document.find(text, cursor)
        if not found.isNull():
            self.editor.setTextCursor(found)

    def replace(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
        self.find()

    def replace_all(self):
        text = self.find_input.text()
        replacement = self.replace_input.text()
        cursor = self.editor.textCursor()
        cursor.movePosition(cursor.Start)
        count = 0
        while True:
            found = self.editor.document().find(text, cursor)
            if found.isNull():
                break
            found.insertText(replacement)
            cursor = found
            count += 1
