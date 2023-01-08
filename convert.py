# PyQt5
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

# Other
import pyperclip

# Regex for Base Inputs
base_regex = {
    'bin': '[10]+',
    'dec': '[0-9]+',
    'hex': '[0-9A-Fa-f]+',
    'oct': '[0-7]+'
}


# Convert Binary String to Other Bases
def convert_bin(binString):
    return {
        'bin': binString,
        'dec': str(int(binString, 2)),
        'hex': str(hex(int(binString, 2)))[2:],
        'oct': str(oct(int(binString, 2)))[2:]
    }


# Convert Decimal String to Other Bases
def convert_dec(decString):
    binString = str(bin(int(decString))[2:])
    return convert_bin(binString)


# Convert Hex String to Other Bases
def convert_hex(hexString):
    binString = str(bin(int(hexString, 16))[2:])
    return convert_bin(binString)


# Convert Oct String to Other Bases
def convert_oct(octString):
    binString = str(bin(int(octString, 8))[2:])
    return convert_bin(binString)


# Set Digit Length of String
def set_digits(s, digits):
    if len(s) < 1 or len(s) == digits:
        return s

    # Remove Extra Digits
    while len(s) > digits and s[0] == '0':
        s = s[1:]

    # Add Leading Digits
    while len(s) < digits:
        s = '0' + s

    return s


# Copy string to clipboard
def copy_to_clipboard(s):
    if s == '':
        return
    pyperclip.copy(s)


# Get Regex Validator for given type
def input_validator(inputType):
    return QRegExpValidator(QRegExp(base_regex[inputType]))


def performOperation(a, b, op_code):
    if op_code == '+':
        return a + b
    elif op_code == '-':
        return a - b
    elif op_code == '*':
        return a * b
    elif op_code == '//':
        return a // b
    elif op_code == '%':
        return a % b
    elif op_code == '|':
        return a | b
    elif op_code == '<<':
        return a << b
    elif op_code == '>>':
        return a >> b
