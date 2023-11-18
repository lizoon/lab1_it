from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox

class DeleteRowDialog(QDialog):
    def __init__(self, model, row, parent=None):
        super().__init__(parent)
        self.model = model
        self.row = row
        self.setWindowTitle("Видалити рядок")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ви впевнені, що хочете видалити цей рядок?"))
        delete_button = QPushButton("Видалити")
        delete_button.clicked.connect(self.delete_row)
        layout.addWidget(delete_button)

    def delete_row(self):
        self.model.removeRow(self.row)
        if self.model.submitAll():
            self.model.database().commit()
            QMessageBox.information(self, "Успіх", "Рядок видалено.")
            self.accept()
        else:
            self.model.database().rollback()
            QMessageBox.warning(self, "Помилка", "Не вдалося видалити рядок.")
            self.reject()
