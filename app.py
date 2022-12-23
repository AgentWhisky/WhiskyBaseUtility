import sys
from PyQt5.QtCore import QFile, QTextStream, Qt, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication

import convert
from window import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self, parent=None):
        # Do not touch
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.offset = None  # Movement Offset
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove Title Bar
        # Do not touch

        # Set Window Icons
        self.setup_title_bar()

        # Setup Convert
        self.convert_setup()
        self.convert_clearOutput()

    # --- Mouse Events ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

        # Method to setup the title bar

    # --- Window Setup ---
    def setup_title_bar(self):
        # Change Window Name
        self.ui.title_label.setText('Whisky Base Utility')
        # Set Icons
        self.ui.minimize_button.setIcon(QIcon('Resources/Icons/minimize_icon.png'))
        self.ui.maximize_button.setIcon(QIcon('Resources/Icons/maximize_icon.png'))
        self.ui.close_button.setIcon(QIcon('Resources/Icons/close_icon.png'))

        # Set Up Actions
        self.ui.minimize_button.clicked.connect(self.showMinimized)
        self.ui.maximize_button.clicked.connect(self.maximize_window)
        self.ui.close_button.clicked.connect(self.close)

    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # --- Convert Functions ---
    def convert_setup(self):
        # --- Input Validation ---
        self.ui.input_bin.setValidator(QRegExpValidator(QRegExp(convert.input_regex['bin']), self.ui.input_bin))
        self.ui.input_dec.setValidator(QRegExpValidator(QRegExp(convert.input_regex['dec']), self.ui.input_dec))
        self.ui.input_hex.setValidator(QRegExpValidator(QRegExp(convert.input_regex['hex']), self.ui.input_hex))
        self.ui.input_oct.setValidator(QRegExpValidator(QRegExp(convert.input_regex['oct']), self.ui.input_oct))

        # Input Buttons
        self.ui.convert_bin.clicked.connect(lambda: self.convert_output('bin'))
        self.ui.convert_dec.clicked.connect(lambda: self.convert_output('dec'))
        self.ui.convert_hex.clicked.connect(lambda: self.convert_output('hex'))
        self.ui.convert_oct.clicked.connect(lambda: self.convert_output('oct'))
        self.ui.convert_inputClear.clicked.connect(self.convert_clearInput)

        # MinDigits
        self.ui.digits_bin.valueChanged.connect(self.convert_updateDigits)
        self.ui.digits_dec.valueChanged.connect(self.convert_updateDigits)
        self.ui.digits_hex.valueChanged.connect(self.convert_updateDigits)
        self.ui.digits_oct.valueChanged.connect(self.convert_updateDigits)

        # Output Buttons
        self.ui.copy_bin.clicked.connect(lambda: self.convert_copyClipboard('bin'))
        self.ui.copy_dec.clicked.connect(lambda: self.convert_copyClipboard('dec'))
        self.ui.copy_hex.clicked.connect(lambda: self.convert_copyClipboard('hex'))
        self.ui.copy_oct.clicked.connect(lambda: self.convert_copyClipboard('oct'))

        self.ui.convert_outputClear.clicked.connect(self.convert_clearOutput)

        # Radio Buttons
        self.ui.convertRadioUpper.toggled.connect(lambda: self.convert_formatOutput(1))
        self.ui.convertRadioLower.toggled.connect(lambda: self.convert_formatOutput(2))

        # Character Counter
        self.ui.convert_characterInput.textChanged.connect(self.characterCountChange)
        self.ui.characterCounterClear.clicked.connect(self.clearCharacterCount)

    def convert_output(self, inputID):
        # Get Output Digits
        minDigits = [
            self.ui.digits_bin.value(),
            self.ui.digits_dec.value(),
            self.ui.digits_hex.value(),
            self.ui.digits_oct.value()
        ]

        # Get Format
        if self.ui.convertRadioUpper.isChecked():
            f = 1
        elif self.ui.convertRadioLower.isChecked():
            f = 2
        else:
            f = 0

        # Convert ID
        if inputID == 'bin':
            text = self.ui.input_bin.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Binary')
            output = convert.convert_bin(self.ui.input_bin.text(), minDigits, f)

        elif inputID == 'dec':
            text = self.ui.input_dec.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Decimal')
            output = convert.convert_dec(self.ui.input_dec.text(), minDigits, f)

        elif inputID == 'hex':
            text = self.ui.input_hex.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Hexadecimal')
            output = convert.convert_hex(self.ui.input_hex.text(), minDigits, f)

        elif inputID == 'oct':
            text = self.ui.input_oct.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Octal')
            output = convert.convert_oct(self.ui.input_oct.text(), minDigits, f)

        else:
            return

        # Set Outputs
        self.ui.output_bin.setText(output['bin'])
        self.ui.output_dec.setText(output['dec'])
        self.ui.output_hex.setText(output['hex'])
        self.ui.output_oct.setText(output['oct'])

    # Clear Input Section
    def convert_clearInput(self):
        self.ui.input_bin.setText('')
        self.ui.input_dec.setText('')
        self.ui.input_hex.setText('')
        self.ui.input_oct.setText('')

    # Update Leading Digits
    def convert_updateDigits(self):
        if len(self.ui.output_bin.text()) > 0:
            self.ui.output_bin.setText(convert.leadingDigits(self.ui.output_bin.text(), self.ui.digits_bin.value()))
        if len(self.ui.output_dec.text()) > 0:
            self.ui.output_dec.setText(convert.leadingDigits(self.ui.output_dec.text(), self.ui.digits_dec.value()))
        if len(self.ui.output_hex.text()) > 0:
            self.ui.output_hex.setText(convert.leadingDigits(self.ui.output_hex.text(), self.ui.digits_hex.value()))
        if len(self.ui.output_oct.text()) > 0:
            self.ui.output_oct.setText(convert.leadingDigits(self.ui.output_oct.text(), self.ui.digits_oct.value()))

    # Clear Output Section
    def convert_formatOutput(self, f):
        # Set Output Uppercase
        if f == 1:
            self.ui.output_bin.setText(self.ui.output_bin.text().upper())
            self.ui.output_dec.setText(self.ui.output_dec.text().upper())
            self.ui.output_hex.setText(self.ui.output_hex.text().upper())
            self.ui.output_oct.setText(self.ui.output_oct.text().upper())
        # Set Output Lowercase
        if f == 2:
            self.ui.output_bin.setText(self.ui.output_bin.text().lower())
            self.ui.output_dec.setText(self.ui.output_dec.text().lower())
            self.ui.output_hex.setText(self.ui.output_hex.text().lower())
            self.ui.output_oct.setText(self.ui.output_oct.text().lower())

    # Copy to clipboard
    def convert_copyClipboard(self, copyID):
        if copyID == 'bin':
            convert.copyToClipboard(self.ui.output_bin.text())
        if copyID == 'dec':
            convert.copyToClipboard(self.ui.output_dec.text())
        if copyID == 'hex':
            convert.copyToClipboard(self.ui.output_hex.text())
        if copyID == 'oct':
            convert.copyToClipboard(self.ui.output_oct.text())

    # Clear Output
    def convert_clearOutput(self):
        self.ui.output_bin.setText('')
        self.ui.output_dec.setText('')
        self.ui.output_hex.setText('')
        self.ui.output_oct.setText('')

        self.ui.convert_outputType.setText('Output Type: None')

    # Update Character Count
    def characterCountChange(self):
        self.ui.characterCounterLabel.setText('Character Count: {}'.
                                              format(len(self.ui.convert_characterInput.toPlainText())))

    # Clear Character Count
    def clearCharacterCount(self):
        self.ui.convert_characterInput.clear()


# Read StyleSheet of given name
def get_style_sheet(file_name):
    file = QFile(file_name)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    return stream.readAll()


def main():
    app = QApplication(sys.argv)

    # Set Style Sheet
    #app.setStyleSheet(get_style_sheet('Resources/luna.qss'))

    # Run
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
