from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QVariant
import re


class EditRowDialog(QDialog):
    def __init__(self, model, row, parent=None):
        super().__init__(parent)
        self.model = model
        self.row = row
        self.fields = []
        self.setWindowTitle("Редагувати рядок")

        layout = QVBoxLayout(self)

        for column in range(model.columnCount()):
            field_layout = QHBoxLayout()

            label = QLabel(model.headerData(column, Qt.Horizontal))
            field_layout.addWidget(label)

            line_edit = QLineEdit(self)
            line_edit.setText(str(model.data(model.index(row, column), Qt.EditRole)))
            self.fields.append(line_edit)
            field_layout.addWidget(line_edit)

            layout.addLayout(field_layout)

        self.save_button = QPushButton("Зберегти зміни", self)
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

    def save_changes(self):
        if self.row >= self.model.rowCount():
            QMessageBox.warning(self, "Помилка", "Рядок більше не існує.")
            self.reject()
            return

        for column, field in enumerate(self.fields):
            value = field.text()
            field_type = self.model.record().field(column).type()

            if not self.validate_value(value, field_type):
                QMessageBox.warning(self, "Помилка",
                                    f"Неправильний тип даних для поля '{self.model.headerData(column, Qt.Horizontal)}'")
                return

            self.model.setData(self.model.index(self.row, column), value)

        if self.model.submitAll():
            self.model.database().commit()
            QMessageBox.information(self, "Успіх", "Зміни в рядку збережено.")
            self.accept()
        else:
            self.model.database().rollback()
            QMessageBox.warning(self, "Помилка", "Не вдалося зберегти зміни.")
            self.reject()

    def validate_value(self, value, field_type):
        if field_type == QVariant.Int and not value.isdigit():
            return False
        if field_type == QVariant.Double:
            try:
                float(value)
            except ValueError:
                return False
        if field_type == QVariant.Char and len(value) != 1:
            return False
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