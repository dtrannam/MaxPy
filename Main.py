# Testing file
import PyQt5.QtWidgets as qtw


class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MaxPr.exe')  # Title
        self.setLayout(qtw.QVBoxLayout())  # Layout

        # Entry fields

        projectLabel = qtw.QLabel('Enter new PR')
        self.layout().addWidget(projectLabel)

        entryLift = qtw.QComboBox(self)
        entryLift.addItem('Bench Press')
        entryLift.addItem('Overhead Press')
        entryLift.addItem('DeadLift')
        entryLift.addItem('Squat')
        self.layout().addWidget(entryLift)

        entryDate = qtw.QLineEdit()
        entryDate.setObjectName('')
        entryDate.setText('[YYYY-MM-DD]')

        self.layout().addWidget(entryDate)
        entryWeight = qtw.QLineEdit()
        entryWeight.setObjectName('')
        entryWeight.setText('[Weight]')
        self.layout().addWidget(entryWeight)

        entryRep = qtw.QLineEdit()
        entryRep.setObjectName('')
        entryRep.setText('[Rep]')
        self.layout().addWidget(entryRep)

        # log button
        log_button = qtw.QPushButton('Log Progress', clicked=lambda: add_entry())
        self.layout().addWidget(log_button)

        self.show()

        def add_entry():
            print(f'Pick: {entryLift.currentText()}')


app = qtw.QApplication([])
mw = mainWindow()

app.exec_()
