# Docucolor Decode

A Python tool to decode yellow tracking dots (Machine Identification Code / MIC) patterns found in color laser printer output. Also known as printer steganography, printer tracking dots, or yellow dots decoder.

Based on EFF's research on printer tracking dots: https://www.eff.org/issues/printers

![Docucolor Decode Interface](https://raw.githubusercontent.com/AyWiZz/docucolor-decode/main/images/interface.png)

## What it does
Helps detect and decode the yellow dots pattern that many color laser printers add to each page. These tiny yellow dots contain:
- Printer serial number
- Date and time of printing
- Other tracking information

## Features
- Interactive grid to visualize and decode dot patterns
- Real-time decoding of date, time and printer serial number
- Parity checking for error detection
- Dark theme for better visibility

## Usage
1. Run `docucolor_decoder.py`
2. Click dots to toggle them (yellow = active, blue = inactive)
3. The decoded information updates automatically

## Grid Layout
- Dark blue dots: Inactive (clickable)
- Yellow dots: Active (clicked)
- Parity row: Used for error detection

## CTF Tips
Useful for challenges involving printer steganography or document forensics.

## Keywords
docucolor, yellow dots, printer tracking, MIC decoder, printer forensics, printer steganography, document tracking, Xerox tracking, printer dots decoder

## License
MIT License
