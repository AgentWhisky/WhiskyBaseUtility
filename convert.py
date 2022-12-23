import subprocess

import pyperclip

# Regex for Base Inputs
input_regex = {
    'bin': '[10]+',
    'dec': '[0-9]+',
    'hex': '[0-9A-Fa-f]+',
    'oct': '[0-7]+'
}


# Convert Binary to Decimal, Hex, and Oct
def convert_bin(s, minDigits, f):
    # Convert Bases
    c_bin = leadingDigits(s, minDigits[0])
    c_dec = leadingDigits(str(int(s, 2)), minDigits[1])
    c_hex = leadingDigits(str(hex(int(s, 2)))[2:], minDigits[2])
    c_oct = leadingDigits(str(oct(int(s, 2)))[2:], minDigits[3])

    # Set Strings Uppercase
    if f == 1:
        c_bin = c_bin.upper()
        c_dec = c_dec.upper()
        c_hex = c_hex.upper()
        c_oct = c_oct.upper()

    # Set Strings Lowercase
    if f == 2:
        c_bin = c_bin.lower()
        c_dec = c_dec.lower()
        c_hex = c_hex.lower()
        c_oct = c_oct.lower()

    return {
        'bin': c_bin,
        'dec': c_dec,
        'hex': c_hex,
        'oct': c_oct
    }


# Convert Decimal
def convert_dec(s, minDigits, f):
    c_bin = str(bin(int(s))[2:])
    return convert_bin(c_bin, minDigits, f)


# Convert Hex
def convert_hex(s, minDigits, f):
    c_bin = str(bin(int(s, 16))[2:])
    return convert_bin(c_bin, minDigits, f)


# Convert Oct
def convert_oct(s, minDigits, f):
    c_bin = str(bin(int(s, 8))[2:])
    return convert_bin(c_bin, minDigits, f)


# Add leading 0s
def leadingDigits(s, digits):
    # Remove Leading Zeroes
    while len(s) > digits and s[0] == '0':
        s = s[1:]

    # Add leading zeros until len digits
    while len(s) < digits:
        s = '0' + s

    return s


# Copy string to clipboard
def copyToClipboard(s):
    if s == '':
        return
    pyperclip.copy(s)
