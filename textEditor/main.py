# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QStatusBar
from PySide6.QtGui import QAction
from editor import Editor
from utils import FindReplaceDialog

class NotepadClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad Clone")
        self.resize(800, 600)

        self.editor = Editor()
        self.setCentralWidget(self.editor)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.create_menu()
        self.update_cursor_position()

        self.editor.cursorPositionChanged.connect(self.update_cursor_position)

    def create_menu(self):
        menubar = self.menuBar()

        # File
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions([open_action, save_action, save_as_action, exit_action])

        # Edit
        edit_menu = menubar.addMenu("Edit")
        find_action = QAction("Find/Replace", self)
        find_action.triggered.connect(self.find_replace)
        word_wrap_action = QAction("Toggle Word Wrap", self)
        word_wrap_action.triggered.connect(self.toggle_word_wrap)

        edit_menu.addActions([find_action, word_wrap_action])

        # Format
        format_menu = menubar.addMenu("Format")
        font_action = QAction("Choose Font", self)
        font_action.triggered.connect(self.editor.choose_font)
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)

        format_menu.addActions([font_action, theme_action])

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())

    def save_file(self):
        if hasattr(self, 'current_file') and self.current_file:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
        else:
            self.save_file_as()

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if file_name:
            self.current_file = file_name
            self.save_file()

    def find_replace(self):
        dialog = FindReplaceDialog(self.editor)
        dialog.exec()

    def toggle_word_wrap(self):
        mode = self.editor.lineWrapMode()
        if mode == self.editor.NoWrap:
            self.editor.setLineWrapMode(self.editor.WidgetWidth)
        else:
            self.editor.setLineWrapMode(self.editor.NoWrap)

    def toggle_theme(self):
        current_bg = self.editor.palette().color(self.editor.backgroundRole()).name()
        if current_bg == "#212121":
            self.editor.setStyleSheet("background-color: white; color: black;")
        else:
            self.editor.setStyleSheet("background-color: #212121; color: #ECEFF1;")

    def update_cursor_position(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.statusbar.showMessage(f"Line: {line} | Column: {col}")

    def closeEvent(self, event):
        action = self.editor.confirm_unsaved_changes()
        if action == "save":
            self.save_file()
            event.accept()
        elif action == "discard":
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotepadClone()
    window.show()
    sys.exit(app.exec())
