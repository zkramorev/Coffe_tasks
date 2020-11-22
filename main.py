import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from main_f import Ui_MainWindow


class First(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.do()

    def do(self):
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


app = QApplication(sys.argv)
ex = First()
ex.show()
sys.exit(app.exec())
