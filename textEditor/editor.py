# editor.py

from PySide6.QtWidgets import QPlainTextEdit, QFontDialog, QMessageBox
from PySide6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PySide6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#FFEB3B"))
        self.keyword_format.setFontWeight(QFont.Bold)

        self.keywords = [
            "def", "class", "if", "elif", "else", "try", "except",
            "finally", "while", "for", "in", "import", "from", "as",
            "return", "with", "yield", "True", "False", "None", "pass",
            "break", "continue", "and", "or", "not", "is", "lambda"
        ]

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#9E9E9E"))
        self.comment_pattern = QRegularExpression("#[^\n]*")

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#8BC34A"))
        self.string_pattern = QRegularExpression("\".*\"|'.*'")

    def highlightBlock(self, text):
        for word in self.keywords:
            pattern = QRegularExpression(r"\b" + word + r"\b")
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        it = self.comment_pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        it = self.string_pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

class Editor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 12))
        self.setStyleSheet("background-color: #212121; color: #ECEFF1;")
        self.highlighter = PythonHighlighter(self.document())

    def choose_font(self):
        font, ok = QFontDialog.getFont(self.font(), self)
        if ok:
            self.setFont(font)

    def confirm_unsaved_changes(self):
        if self.document().isModified():
            reply = QMessageBox.question(self, "Unsaved Changes", "You have unsaved changes. Save before closing?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                return "save"
            elif reply == QMessageBox.No:
                return "discard"
            else:
                return "cancel"
        return "none"
