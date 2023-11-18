from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QVBoxLayout, QWidget, QTabWidget, QMessageBox, QPushButton, QToolBar, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from menu import create_menu
from table_menu import create_table_menu
import sys
from add_delete_edit.add_row_dialog import AddRowDialog
from add_delete_edit.delete_row_dialog import DeleteRowDialog
from add_delete_edit.edit_row_dialog import EditRowDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База Даних")
        self.setGeometry(100, 100, 800, 600)

        # Центральний віджет - QTabWidget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Створення основного меню
        self.menu_bar = self.menuBar()

        create_menu(self)
        create_table_menu(self)

        self.toolbar = QToolBar("Дії з таблицею")
        self.addToolBar(self.toolbar)

        add_row_btn = QPushButton("Додати рядок")
        add_row_btn.clicked.connect(self.add_row)
        self.toolbar.addWidget(add_row_btn)

        delete_row_btn = QPushButton("Видалити рядок")
        delete_row_btn.clicked.connect(self.delete_row)
        self.toolbar.addWidget(delete_row_btn)

        edit_row_btn = QPushButton("Редагувати рядок")
        edit_row_btn.clicked.connect(self.edit_row)
        self.toolbar.addWidget(edit_row_btn)

    def display_db_data(self, db_path):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)
        self.db.open()

        self.update_table_tabs()

    def update_table_tabs(self):
        self.tab_widget.clear()

        tables = self.db.tables()

        for table in tables:
            tab = QWidget()
            layout = QVBoxLayout(tab)
            table_view = QTableView()
            model = QSqlTableModel(self, self.db)
            model.setTable(table)
            model.select()
            table_view.setModel(model)
            layout.addWidget(table_view)
            self.tab_widget.addTab(tab, table)

    def refresh_db_data(self):
        if self.db and self.db.isOpen():
            self.update_table_tabs()
        else:
            QMessageBox.warning(self, "Помилка", "Жодної бази даних не відкрито для оновлення.")

    def add_row(self):
        current_model = self.get_current_model()
        if current_model:
            dialog = AddRowDialog(current_model, self)
            dialog.exec_()

    def delete_row(self):
        current_model = self.get_current_model()
        current_index = self.get_current_index()
        if current_model and current_index:
            dialog = DeleteRowDialog(current_model, current_index.row(), self)
            if dialog.exec_() == QDialog.Accepted:
                current_model.select()
    def edit_row(self):
        current_model = self.get_current_model()
        current_index = self.get_current_index()
        if current_model and current_index:
            dialog = EditRowDialog(current_model, current_index.row(), self)
            if dialog.exec_() == QDialog.Accepted:
                current_model.select()

    def get_current_model(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.findChild(QTableView).model()
        return None

    def get_current_index(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.findChild(QTableView).currentIndex()
        return None
def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
