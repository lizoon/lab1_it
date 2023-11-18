from PyQt5.QtWidgets import QAction, QFileDialog, QMessageBox
from create_db.create_db_dialog import CreateDbDialog
from CompareTablesDialog import CompareTablesDialog
def create_menu(window):

    file_menu = window.menu_bar.addMenu("Файл")

    create_db_action = QAction("Створити базу", window)
    create_db_action.triggered.connect(lambda: open_create_db_dialog(window))
    file_menu.addAction(create_db_action)

    open_db_action = QAction("Відкрити", window)
    open_db_action.triggered.connect(lambda: open_db(window))
    file_menu.addAction(open_db_action)

    refresh_db_action = QAction("Оновити БД", window)
    refresh_db_action.triggered.connect(lambda: refresh_db(window))
    file_menu.addAction(refresh_db_action)

    compare_tables_action = QAction("Різниця таблиць", window)
    compare_tables_action.triggered.connect(lambda: open_compare_tables_dialog(window))
    file_menu.addAction(compare_tables_action)

    exit_action = QAction("Вихід", window)
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)

def open_create_db_dialog(parent):
    dialog = CreateDbDialog(parent)
    dialog.exec_()

def open_db(parent):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    db_file_name, _ = QFileDialog.getOpenFileName(parent, "Відкрити базу даних", "", "SQLite Files (*.db)", options=options)
    if db_file_name:
        try:
            parent.display_db_data(db_file_name)
            parent.current_db_path = db_file_name
            print(f"База даних '{db_file_name}' успішно відкрита.")
        except Exception as e:
            QMessageBox.warning(parent, "Помилка", f"Помилка при відкритті бази даних: {e}")

def refresh_db(window):
    if hasattr(window, 'current_db_path') and window.current_db_path:
        try:
            window.refresh_db_data()
            print(f"База даних '{window.current_db_path}' оновлена.")
        except Exception as e:
            QMessageBox.warning(window, "Помилка", f"Помилка при оновленні бази даних: {e}")
    else:
        QMessageBox.warning(window, "Помилка", "Жодної бази даних не відкрито для оновлення.")

def open_compare_tables_dialog(parent):
    dialog = CompareTablesDialog(parent)
    dialog.exec_()
