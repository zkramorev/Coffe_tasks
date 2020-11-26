import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from main_f import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow2


class First(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.pushButton_add.clicked.connect(self.window)
        self.do()

    def window(self):
        self.twoWindow = Second()
        self.twoWindow.show()

    def do(self):
        self.tableWidget.clear()
        result = self.cur.execute("""SELECT * FROM data""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Название сорта', 'Степень обжарки',
                                                    'молотый/в зернах', 'Вкус', 'Цена (руб)',
                                                    'Объем упаковки (мл)'])
        self.tableWidget.setRowCount(0)
        for i in range(len(result)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        self.tableWidget.resizeColumnsToContents()

    def app(self, *args):
        if args[-1] == 'add':
            self.cur.execute('''INSERT INTO data(title, level, type, smell, price, num) VALUES (?, ?, ?, ?, ?, ?)''',
                             (args[0], args[1], args[2], args[3], args[4], args[5]))
        else:
            self.cur.execute(f"""UPDATE data
                         SET title='{args[1]}', level='{args[2]}', type='{args[3]}', smell='{args[4]}', 
                                price={args[5]}, num={args[6]} WHERE id={args[0]}""")
        self.con.commit()


class Second(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.currentTextChanged.connect(self.change)
        self.pushButton_ready.clicked.connect(self.do)

    def change(self):
        if self.comboBox.currentText() == 'Редактировать данные':
            self.lineEdit_id.setEnabled(True)
        else:
            self.lineEdit_id.setEnabled(False)

    def do(self):
        self.label_error.setText('')
        self.send = First()
        try:
            if self.comboBox.currentText() == 'Добавить данные':
                self.send.app(self.lineEdit_name.text(), self.comboBox_level.currentText(),
                              self.comboBox_type.currentText(),
                              self.comboBox_smell.currentText(), float(self.lineEdit_price.text()),
                              int(self.lineEdit_num.text()), 'add')
            else:
                self.send.app(int(self.lineEdit_id.text()), self.lineEdit_name.text(),
                              self.comboBox_level.currentText(),
                              self.comboBox_type.currentText(),
                              self.comboBox_smell.currentText(),
                              float(self.lineEdit_price.text()),
                              int(self.lineEdit_num.text()))
            ex.do()
            self.close()
        except BaseException:
            self.label_error.setText('error')


app = QApplication(sys.argv)
ex = First()
ex.show()
sys.exit(app.exec())
