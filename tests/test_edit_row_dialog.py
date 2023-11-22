import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlTableModel, QSqlRecord, QSqlField
from PyQt5.QtCore import QVariant
from core.add_delete_edit.edit_row_dialog import EditRowDialog

app = QApplication([])


class TestEditRowDialog(unittest.TestCase):

    def setUp(self):
        self.record = QSqlRecord()
        self.record.append(QSqlField("test_field1", QVariant.String))
        self.record.append(QSqlField("test_field2", QVariant.Int))

        self.model = MagicMock(spec=QSqlTableModel)
        self.model.record.return_value = self.record
        self.model.rowCount.return_value = 1
        self.model.data.return_value = "test data"
        self.model.index.return_value = MagicMock()

        self.model.headerData.side_effect = lambda column, orientation: f"Column {column}"
        self.model.data.side_effect = lambda index, role: f"Data {index.row()}, {index.column()}"

    def test_edit_row_success(self):
        """Тестуємо успішне редагування рядка."""
        dialog = EditRowDialog(self.model, 0)

        for field in dialog.fields:
            field.setText("updated data")

        with patch('PyQt5.QtWidgets.QMessageBox') as mock_msgbox:
            dialog.save_button.click()

            self.assertTrue(self.model.submitAll.called)
            self.assertTrue(self.model.database().commit.called)

    def test_edit_row_failure(self):
        """Тестуємо випадок, коли рядок більше не існує."""
        dialog = EditRowDialog(self.model, 1)

        with patch('PyQt5.QtWidgets.QMessageBox') as mock_msgbox:
            dialog.save_button.click()

            mock_msgbox.warning.assert_called_once()


if __name__ == '__main__':
    unittest.main()
