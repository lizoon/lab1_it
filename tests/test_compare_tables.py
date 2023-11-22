import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from core.compare_tables.CompareTablesDialog import CompareTablesDialog

app = QApplication([])


class TestCompareTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = QSqlDatabase.addDatabase('QSQLITE')
        cls.db.setDatabaseName(':memory:')
        cls.db.open()

        query = QSqlQuery()
        query.exec("CREATE TABLE table1 (id INTEGER, value TEXT)")
        query.exec("CREATE TABLE table2 (id INTEGER, value TEXT)")

        query.exec("INSERT INTO table1 (id, value) VALUES (1, 'A')")
        query.exec("INSERT INTO table1 (id, value) VALUES (2, 'B')")
        query.exec("INSERT INTO table2 (id, value) VALUES (2, 'B')")
        query.exec("INSERT INTO table2 (id, value) VALUES (3, 'C')")

    def test_find_differences(self):
        dialog = CompareTablesDialog()
        dialog.db = self.db

        differences = dialog.find_differences('table1', 'table2')

        self.assertTrue(any(record.value('id') == 1 for record in differences['in_table1_not_table2']))
        self.assertTrue(any(record.value('id') == 3 for record in differences['in_table2_not_table1']))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()


if __name__ == '__main__':
    unittest.main()
