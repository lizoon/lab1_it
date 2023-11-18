from PyQt5.QtWidgets import QAction, QFileDialog
from create_delete_table.create_table_dialog import CreateTableDialog
from create_delete_table.delete_table_dialog import DeleteTableDialog


def create_table_menu(window):
    table_menu = window.menuBar().addMenu("Таблиці")

    create_table_action = QAction("Створити таблицю", window)
    create_table_action.triggered.connect(lambda: open_create_table_dialog(window))
    table_menu.addAction(create_table_action)

    delete_table_action = QAction("Видалити таблицю", window)
    delete_table_action.triggered.connect(lambda: open_delete_table_dialog(window))
    table_menu.addAction(delete_table_action)


def open_create_table_dialog(parent):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    db_file_name, _ = QFileDialog.getOpenFileName(parent, "Вибрати базу даних", "", "SQLite Files (*.db)",
                                                  options=options)
    if db_file_name:
        dialog = CreateTableDialog(db_file_name, parent)
        dialog.exec_()

def open_delete_table_dialog(parent):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    db_file_name, _ = QFileDialog.getOpenFileName(parent, "Вибрати базу даних", "", "SQLite Files (*.db)", options=options)
    if db_file_name:
        dialog = DeleteTableDialog(db_file_name, parent)
        dialog.exec_()
