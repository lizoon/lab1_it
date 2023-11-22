import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
)


class DeleteTableDialog(QDialog):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setWindowTitle("Видалення таблиці")
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Оберіть таблицю для видалення:"))
        self.table_combo_box = QComboBox(self)
        self.layout.addWidget(self.table_combo_box)

        self.load_tables()

        delete_button = QPushButton("Видалити таблицю", self)
        delete_button.clicked.connect(self.delete_table)
        self.layout.addWidget(delete_button)

    def load_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            self.table_combo_box.addItem(table[0])
        conn.close()

    def delete_table(self):
        table_name = self.table_combo_box.currentText()
        if table_name:
            reply = QMessageBox.question(
                self, 'Підтвердження',
                f"Ви впевнені, що хочете видалити таблицю '{table_name}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute(f"DROP TABLE {table_name}")
                    conn.commit()
                    conn.close()
                    QMessageBox.information(self, "Успіх", f"Таблицю '{table_name}' успішно видалено.")
                    self.accept()
                except Exception as e:
                    QMessageBox.warning(self, "Помилка", f"Помилка при видаленні таблиці: {e}")
