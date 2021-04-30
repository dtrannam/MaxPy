import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
import datetime
import sqlite3
import matplotlib.pyplot as graph


class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # my variable
        self._lifts = ['Bench Press', 'Overhead Press', 'DeadLift', 'Squat']
        self._tableHeader = ['Lift', 'Date', 'Input Weight', 'Rep', 'Estimated Max']
        # GUI
        self.setWindowTitle('MaxPr')  # Title
        self.setLayout(qtw.QGridLayout())  # Layout
        self.createTable()
        self.mainGUI()
        self.logGUI()
        self.createTable()
        self.logTable()
        self.show()

    def mainGUI(self):
        # handles title/window/sizing
        projectLabel = qtw.QLabel('Enter new PR')
        projectLabel.setFont(QFont('Arial', 10))
        self.layout().addWidget(projectLabel, 0, 0)
        self.setWindowIcon(QIcon('weights.jpg'))
        self.setGeometry(500, 500, 250, 500)

    def logGUI(self):
        # Combo Box for looping through individual lifts
        entryLift = qtw.QComboBox(self)
        deleteLift = qtw.QComboBox(self)
        for item in self._lifts:
            entryLift.addItem(item)
            deleteLift.addItem(item)
        self.layout().addWidget(entryLift, 1, 0)
        self.layout().addWidget(deleteLift, 1, 1)

        # Date Entry for adding/deleting items
        entryDate = qtw.QLineEdit()
        entryDate.setObjectName('')
        entryDate.setText('[YYYY-MM-DD]')
        self.layout().addWidget(entryDate, 2, 0)
        deleteDate = qtw.QLineEdit()
        deleteDate.setObjectName('')
        deleteDate.setText('[YYYY-MM-DD]')
        self.layout().addWidget(deleteDate, 2, 1)

        # Date Weight/Rep for new weights
        entryWeight = qtw.QLineEdit()
        entryWeight.setObjectName('')
        entryWeight.setText('[Weight]')
        self.layout().addWidget(entryWeight, 3, 0)
        entryRep = qtw.QLineEdit()
        entryRep.setObjectName('')
        entryRep.setText('[Rep]')
        self.layout().addWidget(entryRep, 4, 0)

        # Log Button for adding and deleting dates
        log_button = qtw.QPushButton('Log Progress',
                                     clicked=lambda: self.logProgress(entryLift.currentText(), entryDate.text(),
                                                                      entryWeight.text(), entryRep.text()))
        delete_button = qtw.QPushButton('Delete Entry [Input Date]',
                                        clicked=lambda: self.deleteLog(deleteDate.text(), deleteLift.currentText()))
        self.layout().addWidget(log_button, 5, 0)
        self.layout().addWidget(delete_button, 3, 1)

        # Progress Check buttons
        show_table = qtw.QPushButton('Display Table', clicked=lambda: add_entry())
        show_graph = qtw.QPushButton('Display Graph', clicked=lambda: self.showGraph(deleteLift.currentText()))
        self.layout().addWidget(show_table, 4, 1)
        self.layout().addWidget(show_graph, 5, 1)

        # CSV set up
        checkBP, checkOP, checkDL, checkST = qtw.QCheckBox(self._lifts[0]), qtw.QCheckBox(
            self._lifts[1]), qtw.QCheckBox(self._lifts[2]), qtw.QCheckBox(self._lifts[3])
        self.layout().addWidget(checkBP, 1, 2)
        self.layout().addWidget(checkOP, 2, 2)
        self.layout().addWidget(checkDL, 3, 2)
        self.layout().addWidget(checkST, 4, 2)
        csv_button = qtw.QPushButton('Export to CSV', clicked=lambda: add_entry())
        self.layout().addWidget(csv_button, 5, 2)

        def add_entry(): # used for button testing - do not move
            print(f'Pick: {entryDate.text()} {entryLift.currentText()} {entryRep.text()} {checkBP.checkState()}')

    def logTable(self):
        # table set up
        test = qtw.QTableWidget()
        test.setRowCount(25)
        test.setColumnCount(5)
        col = 0
        row = 0

        # set headers
        for item in self._tableHeader:
            test.setItem(row, col, qtw.QTableWidgetItem(item))
            col += 1
        col = 0
        row += 1

        # default query on start
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute('''Select * FROM WeightPR ORDER BY date LIMIT 15''')
        recentEntry = cursor.fetchall()
        db.close()
        for entry in recentEntry:
            for item in entry:
                test.setItem(row, col, qtw.QTableWidgetItem(str(item)))
                col += 1
            col = 0
            row += 1
        col = 0
        row = 1

        # Table Set up
        test.horizontalHeader().setStretchLastSection(True)
        test.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.layout().addWidget(test, 6, 0, 1, 5)

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
        try:
            datetime.datetime.strptime(day, "%Y-%m-%d")     # Date Validation
            inputWeight = int(inputWeight)
            rep = int(rep)
            estimatedMax = inputWeight * (1 + rep / 30)  # Adjust formula here
            db = sqlite3.connect("Weight.db")
            cursor = db.cursor()
            cursor.execute('INSERT INTO WeightPR values (?, ?, ?, ?, ?) ', (lift, day, inputWeight, rep, estimatedMax))
            cursor.execute('Select * from WeightPR')  # test - delete later
            test = cursor.fetchall()  # test - delete later
            print(test)  # test - delete later
            db.commit()
            db.close()
            self.testSQL()
        except:
            alert = App()

    def deleteLog(self, day, lift):
        print(f'deleted {lift} for {day}')
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute(f"Delete From WeightPR where Date = '{day}' AND Lift = '{lift}'")
        db.commit()
        db.close()
        self.testSQL()

    def showGraph(self, lift):
        # data request and formatting
        dates = []
        numbers = []
        db = sqlite3.connect("Weight.db")
        cursor = db.cursor()
        cursor.execute(f"Select date, EstimatedMax from WeightPR where Lift='{lift}'")
        test = cursor.fetchall()
        for item in test:
            dates.append(item[0])
            numbers.append(item[1])
        print(dates, numbers, lift) # testing function
        convertDate = [datetime.strptime(day, '%Y-%m-%d') for day in dates]
        db.close()

        # graph display and set up
        graph.plot(convertDate, numbers, label='Progression', linestyle='dashed', color='red')
        graph.legend()
        graph.title(f'{lift}')
        graph.ylabel('Weight')
        graph.xlabel('Date')
        graph.show()

    def dateValidation(self):
        pass
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


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Error Alert'
        self.setGeometry(500, 250, 320, 200)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        buttonReply = qtw.QMessageBox.question(self, "Error", "Check input data and try again", qtw.QMessageBox.Close)
        self.show()

app = qtw.QApplication([])
mw = mainWindow()
app.exec_()
