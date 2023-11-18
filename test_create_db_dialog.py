import sys
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from create_db.create_db_dialog import CreateDbDialog

app = QApplication(sys.argv)

class TestCreateDbDialog(unittest.TestCase):

    @patch('create_db.create_db_dialog.sqlite3')
    def test_create_database_success(self, mock_sqlite):
        """Тестуємо успішне створення бази даних."""
        dialog = CreateDbDialog()
        test_db_name = 'test_database'
        dialog.db_name_input.setText(test_db_name)

        with patch('create_db.create_db_dialog.QMessageBox') as mock_msgbox:
            dialog.create_button.click()
            mock_sqlite.connect.assert_called_with(f'{test_db_name}.db')
            mock_msgbox.information.assert_called_once()

    def test_create_database_failure(self):
        """Тестуємо випадок, коли ім'я бази даних не введено."""
        dialog = CreateDbDialog()
        dialog.db_name_input.setText('')

        with patch('create_db.create_db_dialog.QMessageBox') as mock_msgbox:
            dialog.create_button.click()
            mock_msgbox.warning.assert_called_once()

if __name__ == '__main__':
    unittest.main()
