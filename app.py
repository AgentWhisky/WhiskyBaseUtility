import sys
from PyQt5.QtCore import QFile, QTextStream, Qt, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication

import convert
from window import Ui_MainWindow

# Base Strings
type_binary = 'bin'
type_decimal = 'dec'
type_hex = 'hex'
type_oct = 'oct'

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
        self.convert_clear_output()



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

    # Toggle Window Maximize
    def maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # --- Convert Functions ---
    def convert_setup(self):
        # Input Validation
        self.ui.input_bin.setValidator(convert.input_validator(type_binary))
        self.ui.input_dec.setValidator(convert.input_validator(type_decimal))
        self.ui.input_hex.setValidator(convert.input_validator(type_hex))
        self.ui.input_oct.setValidator(convert.input_validator(type_oct))

        # Input Convert Buttons
        self.ui.convert_bin.clicked.connect(lambda: self.convert_output(type_binary))
        self.ui.convert_dec.clicked.connect(lambda: self.convert_output(type_decimal))
        self.ui.convert_hex.clicked.connect(lambda: self.convert_output(type_hex))
        self.ui.convert_oct.clicked.connect(lambda: self.convert_output(type_oct))

        # Input Clear
        self.ui.convert_inputClear.clicked.connect(self.convert_clear_input)

        # Output Minimum Digits Selection
        self.ui.digits_bin.valueChanged.connect(self.convert_update_digits)
        self.ui.digits_dec.valueChanged.connect(self.convert_update_digits)
        self.ui.digits_hex.valueChanged.connect(self.convert_update_digits)
        self.ui.digits_oct.valueChanged.connect(self.convert_update_digits)

        # Output Copy Buttons
        self.ui.copy_bin.clicked.connect(lambda: self.convert_copy_clipboard(type_binary))
        self.ui.copy_dec.clicked.connect(lambda: self.convert_copy_clipboard(type_decimal))
        self.ui.copy_hex.clicked.connect(lambda: self.convert_copy_clipboard(type_hex))
        self.ui.copy_oct.clicked.connect(lambda: self.convert_copy_clipboard(type_oct))

        # Output Clear
        self.ui.convert_outputClear.clicked.connect(self.convert_clear_output)

        # Output Format Radio Buttons
        self.ui.convertRadioUpper.toggled.connect(lambda: self.convert_format_output(0))
        self.ui.convertRadioLower.toggled.connect(lambda: self.convert_format_output(1))

        # Character Counter
        self.ui.convert_characterInput.textChanged.connect(self.characterCountChange)
        self.ui.characterCounterClear.clicked.connect(self.clearCharacterCount)

    # Update Output
    def convert_output(self, convertID):
        # Get Output Minimum Digits
        min_digits = [
            self.ui.digits_bin.value(),
            self.ui.digits_dec.value(),
            self.ui.digits_hex.value(),
            self.ui.digits_oct.value()
        ]

        # Get Format
        output_format = 0
        if self.ui.convertRadioUpper.isChecked():
            output_format = 0
        elif self.ui.convertRadioLower.isChecked():
            output_format = 1

        # Convert Binary
        if convertID == type_binary:
            text = self.ui.input_bin.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Binary')
            output = convert.convert_bin(self.ui.input_bin.text())

        # Convert Decimal
        elif convertID == type_decimal:
            text = self.ui.input_dec.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Decimal')
            output = convert.convert_dec(self.ui.input_dec.text())

        # Convert Hex
        elif convertID == 'hex':
            text = self.ui.input_hex.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Hexadecimal')
            output = convert.convert_hex(self.ui.input_hex.text())

        # Convert Oct
        elif convertID == 'oct':
            text = self.ui.input_oct.text()
            if text == '':
                return
            self.ui.convert_outputType.setText('Output Type: Octal')
            output = convert.convert_oct(self.ui.input_oct.text())

        # Invalid Type Return
        else:
            return

        # Set Minimum Digits
        output_bin = convert.set_digits(output[type_binary], min_digits[0])
        output_dec = convert.set_digits(output[type_decimal], min_digits[1])
        output_hex = convert.set_digits(output[type_hex], min_digits[2])
        output_oct = convert.set_digits(output[type_oct], min_digits[3])

        # Update Character Format Cases
        if output_format == 1:
            output_hex = output_hex.lower()
        else:
            output_hex = output_hex.upper()

        # Set Outputs
        self.ui.output_bin.setText(output_bin)
        self.ui.output_dec.setText(output_dec)
        self.ui.output_hex.setText(output_hex)
        self.ui.output_oct.setText(output_oct)

    # Clear Input Section
    def convert_clear_input(self):
        self.ui.input_bin.setText('')
        self.ui.input_dec.setText('')
        self.ui.input_hex.setText('')
        self.ui.input_oct.setText('')

    # Update Leading Digits
    def convert_update_digits(self):
        if len(self.ui.output_bin.text()) > 0:
            self.ui.output_bin.setText(convert.set_digits(self.ui.output_bin.text(), self.ui.digits_bin.value()))
        if len(self.ui.output_dec.text()) > 0:
            self.ui.output_dec.setText(convert.set_digits(self.ui.output_dec.text(), self.ui.digits_dec.value()))
        if len(self.ui.output_hex.text()) > 0:
            self.ui.output_hex.setText(convert.set_digits(self.ui.output_hex.text(), self.ui.digits_hex.value()))
        if len(self.ui.output_oct.text()) > 0:
            self.ui.output_oct.setText(convert.set_digits(self.ui.output_oct.text(), self.ui.digits_oct.value()))

    # Clear Output Section
    def convert_format_output(self, f):
        # Set Output Uppercase
        if f == 0:
            self.ui.output_hex.setText(self.ui.output_hex.text().upper())
        # Set Output Lowercase
        if f == 1:
            self.ui.output_hex.setText(self.ui.output_hex.text().lower())

    # Copy to clipboard
    def convert_copy_clipboard(self, copyID):
        if copyID == type_binary:
            convert.copy_to_clipboard(self.ui.output_bin.text())
        if copyID == type_decimal:
            convert.copy_to_clipboard(self.ui.output_dec.text())
        if copyID == type_hex:
            convert.copy_to_clipboard(self.ui.output_hex.text())
        if copyID == type_oct:
            convert.copy_to_clipboard(self.ui.output_oct.text())

    # Clear Output
    def convert_clear_output(self):
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
