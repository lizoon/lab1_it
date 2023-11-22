from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QComboBox, QLabel, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class CompareTablesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Виявлення різниць між таблицями")
        self.db = None

        layout = QVBoxLayout(self)

        self.select_db_button = QPushButton("Виберіть базу даних")
        self.select_db_button.clicked.connect(self.select_database)
        layout.addWidget(self.select_db_button)

        self.table1ComboBox = QComboBox()
        self.table2ComboBox = QComboBox()

        layout.addWidget(QLabel("Виберіть першу таблицю"))
        layout.addWidget(self.table1ComboBox)
        layout.addWidget(QLabel("Виберіть другу таблицю"))
        layout.addWidget(self.table2ComboBox)

        compare_button = QPushButton("Порівняти")
        compare_button.clicked.connect(self.compare_tables)
        layout.addWidget(compare_button)

    def select_database(self):
        options = QFileDialog.Options()
        db_file_name, _ = QFileDialog.getOpenFileName(self, "Відкрити базу даних", "", "All Files (*);;SQLite Files (*.db)", options=options)
        if db_file_name:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_file_name)
            self.db.open()

            self.table1ComboBox.clear()
            self.table2ComboBox.clear()
            self.table1ComboBox.addItems(self.get_tables_list())
            self.table2ComboBox.addItems(self.get_tables_list())

    def get_tables_list(self):
        if self.db and self.db.isOpen():
            return self.db.tables()
        else:
            QMessageBox.warning(self, "Помилка", "База даних не вибрана або не вдалося відкрити.")
            return []

    def compare_tables(self):
        table1 = self.table1ComboBox.currentText()
        table2 = self.table2ComboBox.currentText()

        if table1 and table2:
            differences = self.find_differences(table1, table2)
            self.show_differences(differences)
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, виберіть обидві таблиці для порівняння.")

    def find_differences(self, table1, table2):
        query1 = QSqlQuery(self.db)
        query2 = QSqlQuery(self.db)

        query1_str = f"SELECT * FROM {table1} EXCEPT SELECT * FROM {table2}"
        query2_str = f"SELECT * FROM {table2} EXCEPT SELECT * FROM {table1}"

        if not query1.exec(query1_str):
            QMessageBox.warning(self, "Помилка", f"Помилка при виконанні запиту: {query1.lastError().text()}")
            return []

        if not query2.exec(query2_str):
            QMessageBox.warning(self, "Помилка", f"Помилка при виконанні запиту: {query2.lastError().text()}")
            return []

        differences = {
            'in_table1_not_table2': [],
            'in_table2_not_table1': []
        }

        while query1.next():
            differences['in_table1_not_table2'].append(query1.record())

        while query2.next():
            differences['in_table2_not_table1'].append(query2.record())

        return differences

    def show_differences(self, differences):
        differencesDialog = QDialog(self)
        differencesDialog.setWindowTitle("Різниця таблиць")

        layout = QVBoxLayout(differencesDialog)

        tableWidget = QTableWidget()
        tableWidget.setColumnCount(2)
        tableWidget.setHorizontalHeaderLabels(["В таблиці 1, але не в таблиці 2", "В таблиці 2, але не в таблиці 1"])
        tableWidget.setRowCount(max(len(differences['in_table1_not_table2']), len(differences['in_table2_not_table1'])))

        for i, record in enumerate(differences['in_table1_not_table2']):
            item = QTableWidgetItem(self.record_to_string(record))
            tableWidget.setItem(i, 0, item)

        for i, record in enumerate(differences['in_table2_not_table1']):
            item = QTableWidgetItem(self.record_to_string(record))
            tableWidget.setItem(i, 1, item)

        tableWidget.resizeColumnsToContents()

        layout.addWidget(tableWidget)
        differencesDialog.setLayout(layout)
        differencesDialog.exec_()

    def record_to_string(self, record):
        return " | ".join(f"{record.value(i)}" for i in range(record.count()))
