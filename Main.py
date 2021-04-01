# Testing file
import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import *


class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MaxPr.exe')  # Title
        self.setLayout(qtw.QGridLayout())  # Layout
        self.logGUI()
        self.show()
        # Entry fields

    def logGUI(self):
        projectLabel = qtw.QLabel('Enter new PR')
        projectLabel.setFont(QFont('Arial', 10))
        self.layout().addWidget(projectLabel, 0, 0)
        # Set Icon
        self.setWindowIcon(QIcon('weights.jpg'))
        # Set window size
        self.setGeometry(300, 300, 300, 150)
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
        log_button = qtw.QPushButton('Log Progress', clicked=lambda: add_entry())
        self.layout().addWidget(log_button)
        # Delete button
        delete_button = qtw.QPushButton('Delete Item', clicked=lambda: add_entry())
        self.layout().addWidget(delete_button, 5, 1)
        # Graph set up
        checkBP = qtw.QCheckBox('Bench Press')
        checkOP = qtw.QCheckBox('Overhead Press')
        checkDL = qtw.QCheckBox('DeadLift')
        checkST = qtw.QCheckBox('Squat')
        self.layout().addWidget(checkBP, 1, 2)
        self.layout().addWidget(checkOP, 2, 2)
        self.layout().addWidget(checkDL, 3, 2)
        self.layout().addWidget(checkST, 4, 2)
        delete_button = qtw.QPushButton('Graph Progress', clicked=lambda: add_entry())
        self.layout().addWidget(delete_button, 5, 2)

        # test function
        def add_entry():
            print(f'Pick: {entryLift.currentText()} {entryRep.text()} {checkBP.checkState()}')


app = qtw.QApplication([])
mw = mainWindow()

app.exec_()
