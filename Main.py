import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import *
from datetime import date, datetime
import sqlite3
import matplotlib.pyplot as graph


class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MaxPr.exe')  # Title
        self.setLayout(qtw.QGridLayout())  # Layout
        self.createTable()
        self.logGUI()
        self.createTable()
        self.logTable()
        self.show()
        # Entry fields

    def logTable(self):
        test = qtw.QTableWidget()
        test.setRowCount(10)
        test.setColumnCount(5)
        test.setItem(0, 0, qtw.QTableWidgetItem("Cell (1,1)"))
        test.setItem(0, 1, qtw.QTableWidgetItem("Cell (1,2)"))
        test.setItem(1, 0, qtw.QTableWidgetItem("Cell (2,1)"))
        test.setItem(1, 1, qtw.QTableWidgetItem("Cell (2,2)"))
        test.setItem(2, 0, qtw.QTableWidgetItem("Cell (3,1)"))
        test.setItem(2, 1, qtw.QTableWidgetItem("Cell (3,2)"))
        test.setItem(3, 0, qtw.QTableWidgetItem("Cell (4,1)"))
        test.setItem(3, 1, qtw.QTableWidgetItem("Cell (4,2)"))
        test.horizontalHeader().setStretchLastSection(True)
        test.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.layout().addWidget(test, 6, 0, 1, 5)

    def logGUI(self):
        projectLabel = qtw.QLabel('Enter new PR')
        projectLabel.setFont(QFont('Arial', 10))
        self.layout().addWidget(projectLabel, 0, 0)
        # Set Icon
        self.setWindowIcon(QIcon('weights.jpg'))
        # Set window size
        self.setGeometry(500, 500, 500, 500)
        # Combo Box for which weights
        entryLift = qtw.QComboBox(self)
        entryLift.addItem('Bench Press')
        entryLift.addItem('Overhead Press')
        entryLift.addItem('DeadLift')
        entryLift.addItem('Squat')
        self.layout().addWidget(entryLift, 1, 0)
        # Date Entry
        entryDate = qtw.QLineEdit()
        entryDate.setObjectName('')
        entryDate.setText('[YYYY-MM-DD]')
        self.layout().addWidget(entryDate, 2, 0)
        # Date Weight
        entryWeight = qtw.QLineEdit()
        entryWeight.setObjectName('')
        entryWeight.setText('[Weight]')
        self.layout().addWidget(entryWeight, 3, 0)
        # Date Rep
        entryRep = qtw.QLineEdit()
        entryRep.setObjectName('')
        entryRep.setText('[Rep]')
        self.layout().addWidget(entryRep, 4, 0)
        # log button
        log_button = qtw.QPushButton('Log Progress', clicked=lambda: self.logProgress(entryLift.currentText(), entryDate.text(), entryWeight.text(), entryRep.text()))
        self.layout().addWidget(log_button)
        # Delete button
        deleteLift = qtw.QComboBox(self)
        deleteLift.addItem('Bench Press')
        deleteLift.addItem('Overhead Press')
        deleteLift.addItem('DeadLift')
        deleteLift.addItem('Squat')
        self.layout().addWidget(deleteLift, 1, 1)
        deleteDate = qtw.QLineEdit()
        deleteDate.setObjectName('')
        deleteDate.setText('[YYYY-MM-DD]')
        self.layout().addWidget(deleteDate, 2, 1)
        delete_button = qtw.QPushButton('Delete Entry [Input Date]', clicked=lambda: self.deleteLog(deleteDate.text(), deleteLift.currentText()))
        self.layout().addWidget(delete_button, 3, 1)
        # Progress Check
        show_table = qtw.QPushButton('Display Table', clicked=lambda: add_entry())
        self.layout().addWidget(show_table, 4, 1)
        show_graph = qtw.QPushButton('Display Graph', clicked=lambda: self.showGraph(deleteLift.currentText()))
        self.layout().addWidget(show_graph, 5, 1)
        # CSV set up
        checkBP = qtw.QCheckBox('Bench Press')
        checkOP = qtw.QCheckBox('Overhead Press')
        checkDL = qtw.QCheckBox('DeadLift')
        checkST = qtw.QCheckBox('Squat')
        self.layout().addWidget(checkBP, 1, 2)
        self.layout().addWidget(checkOP, 2, 2)
        self.layout().addWidget(checkDL, 3, 2)
        self.layout().addWidget(checkST, 4, 2)
        csv_button = qtw.QPushButton('Export to CSV', clicked=lambda: add_entry())
        self.layout().addWidget(csv_button, 5, 2)

        # test function
        def add_entry():
            print(f'Pick: {entryDate.text()} {entryLift.currentText()} {entryRep.text()} {checkBP.checkState()}')

    # everything here is sqlite queries
    def createTable(self):
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute('''Create Table IF NOT EXISTS WeightPR (
                        Lift BLOB,
                        Date BLOB,
                        InputWeight REAL,
                        Rep REAL,
                        EstimatedMax REAL
                        )''')
        db.commit()
        db.close()

    def logProgress(self, lift, day, inputWeight, rep):

        inputWeight = int(inputWeight)
        rep = int(rep)
        estimatedMax = inputWeight * (1 + rep/ 30)     # using Epley formula
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute('INSERT INTO WeightPR values (?, ?, ?, ?, ?) ',(lift, day, inputWeight, rep, estimatedMax))
        cursor.execute('Select * from WeightPR')    # test - delete later
        test = cursor.fetchall()                    # test - delete later
        print(test)                                 # test - delete later
        db.commit()
        db.close()
        self.testSQL()

    def deleteLog(self, day, lift):
        print(f'deleted {lift} fpr {day}')
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute(f"Delete From WeightPR where Date = '{day}' AND Lift = '{lift}'")
        db.commit()
        db.close()
        self.testSQL()

    def showGraph(self, lift):
        conn = sqlite3.connect('Weight.db')
        conn.close()
        dates = []
        numbers = []
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute(f"Select date, EstimatedMax from WeightPR where Lift='{lift}'")
        test = cursor.fetchall()
        for item in test:
            dates.append(item[0])
            numbers.append(item[1])
        print(dates, numbers, lift)
        convertDate = [datetime.strptime(day, '%Y-%m-%d') for day in dates]
        graph.plot(convertDate, numbers, label='Progression', linestyle='dashed', color='red')
        graph.legend()
        graph.title(f'{lift}')
        graph.ylabel('Weight')
        graph.xlabel('Date')
        graph.show()



    # testing functions
    def testSQL(self):
        conn = sqlite3.connect('Weight.db')
        c = conn.cursor()
        c.execute("Select * from WeightPR")
        print(c.fetchall())
        conn.commit()
        conn.close()

    def testPython(self):
        print('This is working I hope')

app = qtw.QApplication([])
mw = mainWindow()
app.exec_()
