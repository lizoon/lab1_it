import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QFormLayout
)


class CreateTableDialog(QDialog):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setWindowTitle("Створення таблиці")
        self.layout = QVBoxLayout(self)

        # Виджети для імені таблиці
        self.layout.addWidget(QLabel("Ім'я таблиці:"))
        self.table_name_input = QLineEdit(self)
        self.layout.addWidget(self.table_name_input)

        # Форма для стовпців таблиці
        self.columns_layout = QFormLayout()
        self.layout.addLayout(self.columns_layout)

        # Кнопка для додавання нових стовпців
        self.add_column_button = QPushButton("Додати стовпець", self)
        self.add_column_button.clicked.connect(self.add_column)
        self.layout.addWidget(self.add_column_button)

        # Список стовпців
        self.columns = []

        # Кнопка створення таблиці
        self.create_button = QPushButton("Створити таблицю", self)
        self.create_button.clicked.connect(self.create_table)
        self.layout.addWidget(self.create_button)

    def add_column(self):
        column_name_input = QLineEdit(self)
        column_type_input = QComboBox(self)
        column_type_input.addItems(["integer", "real", "char", "string", "complexInteger", "complexReal"])

        row_layout = QHBoxLayout()
        row_layout.addWidget(column_name_input)
        row_layout.addWidget(column_type_input)
        self.columns_layout.addRow(row_layout)
        self.columns.append((column_name_input, column_type_input))

    def create_table(self):
        table_name = self.table_name_input.text().strip()
        column_definitions = []
        for column_name_input, column_type_input in self.columns:
            column_name = column_name_input.text().strip()
            column_type = column_type_input.currentText()

            if column_type == "complexInteger":
                column_type = "TEXT"
            elif column_type == "complexReal":
                column_type = "TEXT"
            elif column_type == "char":
                column_type = "CHAR"
            elif column_type == "string":
                column_type = "TEXT"
            elif column_type == "integer":
                column_type = "INTEGER"
            elif column_type == "real":
                column_type = "REAL"

            if column_name:
                column_definitions.append(f'"{column_name}" {column_type}')
            else:
                QMessageBox.warning(self, "Помилка", "Імена стовпців не можуть бути пустими.")
                return

        if table_name and column_definitions:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                columns_sql = ", ".join(column_definitions)
                create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
                cursor.execute(create_table_sql)
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Успіх", f"Таблиця '{table_name}' успішно створена.")
                self.accept()
            except sqlite3.OperationalError as e:
                QMessageBox.warning(self, "Помилка", f"Помилка SQL: {e}")
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Помилка при створенні таблиці: {e}")
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть ім'я таблиці та додайте принаймні один стовпець.")
