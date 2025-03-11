# -*- coding: utf-8 -*-
from Npp import editor
import os
import re
import configparser
from typing import Any, Union
import locale
from decimal import Decimal


SCRIPT_NAME = "ConvertTextNumbersToNumbers"


# Wim Gielis
# Mar. 2025
#
# ConvertTextNumbersToNumbers script (Alt-l):
#       - The selection is in a tabular format with a clear separator
#       - Provide a field separator and column(s) to convert to numbers and number locales.
#       - Transformations:
#         * trim spaces
#         * minus sign taken from the back
#         * brackets are negative
#         * interpretation of separators for decimals and thousands through locales
#       - The chosen settings will be stored/retrieved from an ini configuration file


def convert_text_to_number(value: str, number_locale) -> Union[float|int]:

    # No whitespace
    text_number = value.strip()

    # Currency logic
    currency = 0
    currency_items_to_check = ['€', '$', '£', 'EUR', 'USD', 'GBP']
    pattern = '|'.join(map(re.escape, currency_items_to_check))
    match = re.search(pattern, value)
    if match:
        value = re.sub(pattern, '', value)
        currency_designation = match.group()
        currency = 1


    if text_number in ['', '-']:
        return 0

    # Remove surrounding double quotes
    if text_number.startswith('"') and text_number.endswith('"'):
        text_number = text_number[1:-1]

    # Minus sign at the end or brackets: take it out
    factor = 1

    if text_number[-1] == '-':
        factor = -1
        text_number = text_number[:-1]
    elif text_number.startswith('(') and text_number.endswith(')'):
        factor = -1
        text_number = text_number[1:-1]

    if text_number[-1] == '%':
        factor *= 0.01
        text_number = text_number[:-1]

    # Try the conversion to a number
    try:
        locale.setlocale(locale.LC_ALL, number_locale)  # Set the chosen locale
        numeric_number = factor * float(locale.atof(text_number))
        if isinstance(numeric_number, float) and numeric_number.is_integer():
            return int(numeric_number)
        else:
            return numeric_number
    except ValueError:
        return value

def format_number(value, number_locale) -> str:
    try:
        locale.setlocale(locale.LC_ALL, number_locale)
        return str(Decimal(value))
    except:
        return value


# Get script directory (same as script location) for the configuration file
script_path = notepad.getPluginConfigDir()
ini_file = os.path.join(script_path, "config.ini")

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the INI file if it exists
if os.path.exists(ini_file):
    config.read(ini_file)

# Define the section for this script
script_section = SCRIPT_NAME


continue_script = True

if continue_script:
    # Ask for a field separator, but try to get if from the configuration file
    field_separator = config.get(script_section, "field_separator", fallback=None)[1:-1]
    field_separator = notepad.prompt("Please provide the field separator:", "Search string", field_separator)
    if not field_separator:
        notepad.messageBox( "Error: No field separator provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        field_separator = field_separator.strip().encode().decode('unicode_escape')

if continue_script:
    # Ask for the columns to convert, but try to get if from the configuration file
    columns_to_convert = config.get(script_section, "columns_to_convert", fallback=None)[1:-1]
    columns_to_convert = notepad.prompt("Which columns do you want to convert (comma-separated, 1-based indices):", "Columns to convert", columns_to_convert)
    if not columns_to_convert:
        notepad.messageBox( "Error: No column numbers provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False

if continue_script:
    # Ask for the input locale, but try to get if from the configuration file
    input_locale = config.get(script_section, "input_locale", fallback=None)[1:-1]
    input_locale = notepad.prompt("Please provide the field separator:", "Input locale", input_locale)
    if not input_locale:
        notepad.messageBox( "Error: No input locale provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        input_locale = input_locale.strip()

if continue_script:
    # Ask for the output locale, but try to get if from the configuration file
    output_locale = config.get(script_section, "output_locale", fallback=None)[1:-1]
    output_locale = notepad.prompt("Please provide the field separator:", "Output locale", output_locale)
    if not output_locale:
        notepad.messageBox( "Error: No output locale provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        output_locale = output_locale.strip()

if continue_script:
    # Ask for the output custom format, but try to get if from the configuration file
    output_custom_format = config.get(script_section, "output_custom_format", fallback=None)[1:-1]
    output_custom_format = notepad.prompt("Please provide the field separator:", "Output custom format", output_custom_format)
    if not output_custom_format:
        notepad.messageBox( "Error: No output locale provided!", "Invalid entry", MESSAGEBOXFLAGS.OK + MESSAGEBOXFLAGS.ICONSTOP )
        continue_script = False
    else:
        output_custom_format = output_custom_format.strip()


if continue_script:
    selected_text = editor.getSelText()
    if not selected_text.strip():
        editor.messageBox("No text selected!", "Error", 0)
    else:
        lines = selected_text.split("\n")
        processed_lines = []

        for line in lines:
            if not line.strip():
                processed_lines.append(line)
                continue

            fields = line.split(field_separator)
            for col in columns_to_convert.split(','):
                col_2 = int(col) - 1
                if col_2 < len(fields):
                    fields[col_2] = format_number(convert_text_to_number(fields[col_2], input_locale), output_locale)
            processed_lines.append(field_separator.join(fields))

        if processed_lines:
            new_text = "\n".join(processed_lines)
            editor.replaceSel(new_text)