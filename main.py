import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)


class AddEditCoffeeForm(QWidget):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent_window = parent
        self.coffee_id = coffee_id

        if self.coffee_id is not None:
            self.setWindowTitle('Редактировать запись о кофе')
            self.load_coffee_data()
        else:
            self.setWindowTitle('Добавить запись о кофе')

        self.saveButton.clicked.connect(self.save_data)

    def load_coffee_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT title, roast_degree, ground_or_beans, taste_description, price, package_volume '
            'FROM coffee WHERE id = ?',
            (self.coffee_id,)
        ).fetchone()
        conn.close()

        if row:
            self.titleEdit.setText(row[0])
            self.roastEdit.setText(row[1])
            self.typeCombo.setCurrentText(row[2])
            self.tasteEdit.setText(row[3] if row[3] else '')
            self.priceEdit.setText(str(row[4]))
            self.volumeEdit.setText(str(row[5]))

    def save_data(self):
        title = self.titleEdit.text().strip()
        roast = self.roastEdit.text().strip()
        ground_or_beans = self.typeCombo.currentText()
        taste = self.tasteEdit.text().strip()
        price_text = self.priceEdit.text().strip().replace(',', '.')
        volume_text = self.volumeEdit.text().strip()

        if not title or not roast or not price_text or not volume_text:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля!')
            return

        try:
            price = float(price_text)
            volume = int(volume_text)
            if price <= 0 or volume <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self,
                'Ошибка',
                'Цена должна быть положительным числом, а объем — целым положительным числом!'
            )
            return

        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()

        if self.coffee_id is None:
            cursor.execute(
                '''
                INSERT INTO coffee (title, roast_degree, ground_or_beans, taste_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (title, roast, ground_or_beans, taste, price, volume)
            )
        else:
            cursor.execute(
                '''
                UPDATE coffee
                SET title = ?, roast_degree = ?, ground_or_beans = ?,
                    taste_description = ?, price = ?, package_volume = ?
                WHERE id = ?
                ''',
                (title, roast, ground_or_beans, taste, price, volume, self.coffee_id)
            )

        conn.commit()
        conn.close()

        if self.parent_window:
            self.parent_window.load_data()
        self.close()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.form = None
        self.load_data()

        self.addButton.clicked.connect(self.open_add_form)
        self.editButton.clicked.connect(self.open_edit_form)

    def load_data(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        rows = cursor.execute('SELECT * FROM coffee').fetchall()
        conn.close()

        headers = [
            'ID',
            'Название сорта',
            'Степень обжарки',
            'Молотый/в зернах',
            'Описание вкуса',
            'Цена',
            'Объем упаковки'
        ]

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.tableWidget.resizeColumnsToContents()

    def open_add_form(self):
        self.form = AddEditCoffeeForm(self)
        self.form.show()

    def open_edit_form(self):
        current_row = self.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для редактирования!')
            return

        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        self.form = AddEditCoffeeForm(self, coffee_id)
        self.form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
