# Testing file
import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import *


class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MaxPr.exe')  # Title
        self.setLayout(qtw.QVBoxLayout())  # Layout
        self.logGUI()

        # Entry fields

    def logGUI(self):
        projectLabel = qtw.QLabel('Enter new PR')
        projectLabel.setFont(QFont('Arial', 15))
        self.layout().addWidget(projectLabel)
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
        self.layout().addWidget(entryLift)
        # Date Entry
        entryDate = qtw.QLineEdit()
        entryDate.setObjectName('')
        entryDate.setText('[YYYY-MM-DD]')
        self.layout().addWidget(entryDate)
        # Date Weight
        entryWeight = qtw.QLineEdit()
        entryWeight.setObjectName('')
        entryWeight.setText('[Weight]')
        self.layout().addWidget(entryWeight)
        # Date Rep
        entryRep = qtw.QLineEdit()
        entryRep.setObjectName('')
        entryRep.setText('[Rep]')
        self.layout().addWidget(entryRep)
        # log button
        log_button = qtw.QPushButton('Log Progress', clicked=lambda: add_entry())
        self.layout().addWidget(log_button)

        self.show()

        def add_entry():  # function used to add entry
            print(f'Pick: {entryLift.currentText()} {entryRep.text()}')


app = qtw.QApplication([])
mw = mainWindow()

app.exec_()
