import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class CreateDbDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateDbDialog, self).__init__(parent)
        self.setWindowTitle("Створення бази даних")

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Ім'я бази даних:"))
        self.db_name_input = QLineEdit(self)
        self.layout.addWidget(self.db_name_input)

        self.create_button = QPushButton("Створити базу", self)
        self.create_button.clicked.connect(self.create_database)
        self.layout.addWidget(self.create_button)

    def create_database(self):
        db_name = self.db_name_input.text()
        if db_name:
            try:
                conn = sqlite3.connect(f'{db_name}.db')
                conn.close()
                QMessageBox.information(self, "Успіх", f"База даних '{db_name}.db' успішно створена.")
                self.accept()
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Помилка при створенні бази даних: {e}")
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть ім'я бази даних.")
