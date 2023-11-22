import re
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, QVariant


class AddRowDialog(QDialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("Додати новий рядок")
        self.layout = QVBoxLayout(self)
        self.fields = []
        self.labels = []

        for i in range(model.columnCount()):
            field_layout = QHBoxLayout()
            label = QLabel(model.headerData(i, Qt.Horizontal))
            line_edit = QLineEdit(self)
            field_layout.addWidget(label)
            field_layout.addWidget(line_edit)
            self.layout.addLayout(field_layout)
            self.fields.append(line_edit)
            self.labels.append(label)

        self.save_button = QPushButton("Зберегти")
        self.save_button.clicked.connect(self.save_row)
        self.layout.addWidget(self.save_button)

    def save_row(self):
        new_record = []
        for i, field in enumerate(self.fields):
            value = field.text().strip().replace(" ", "")
            column_label = self.labels[i].text()

            field_type = self.model.record().field(i).type()

            if column_label == 'complexInt':
                field_type = 'complexInteger'
            if column_label == 'complexReal':
                field_type = 'complexReal'

            if not self.validate_value(value, field_type):
                QMessageBox.warning(self, "Помилка", f"Неправильний тип даних для поля '{column_label}'")
                return

            new_record.append(value)

        row = self.model.rowCount()
        self.model.insertRow(row)
        for i, value in enumerate(new_record):
            self.model.setData(self.model.index(row, i), value)

        if self.model.submitAll():
            self.model.database().commit()
            QMessageBox.information(self, "Успіх", "Новий рядок додано.")
            self.accept()
        else:
            error = self.model.lastError()
            print("SQL Query:", self.model.query().lastQuery())
            print("Bind Values:", self.model.query().boundValues())
            self.model.database().rollback()
            QMessageBox.warning(self, "Помилка", f"Не вдалося додати рядок: {error.text()}")
            self.reject()

    def validate_value(self, value, field_type):
        if field_type == QVariant.Int and not value.isdigit():
            return False
        if field_type == QVariant.Double:
            try:
                float(value)
            except ValueError:
                return False

        # check for char (1 symbol)

        if field_type == "complexInteger":
            return self.validate_complex_integer(value)
        if field_type == "complexReal":
            return self.validate_complex_real(value)
        return True

    def validate_complex_integer(self, value):
        pattern = r'^([-+]?\d+)([-+]\d+)i$'
        return bool(re.match(pattern, value.strip()))

    def validate_complex_real(self, value):
        pattern = r'^([-+]?\d+(\.\d+)?\s*[-+]\s*\d+(\.\d+)?)i$'
        return bool(re.match(pattern, value.strip()))

